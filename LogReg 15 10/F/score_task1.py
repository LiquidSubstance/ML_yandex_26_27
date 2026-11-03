"""Score modified embeddings with freshly fitted logistic probes."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

LABELS = ['topic_1', 'topic_2', 'topic_3', 'topic_4', 'source']


def fingerprint(paths):
    h = hashlib.sha256()
    for p in paths:
        data = Path(p).read_bytes()
        h.update(len(data).to_bytes(8, 'big')); h.update(data)
    return h.hexdigest()


def read_data(embedding_path, label_path):
    with np.load(embedding_path, allow_pickle=False) as a:
        if set(a.files) != {'X', 'ids'}: raise ValueError('Expected X and ids in dataset')
        X, ids = a['X'].astype(float), a['ids'].astype(str)
    if X.ndim != 2 or X.shape[1] != 32 or len(X) != len(ids) or not np.isfinite(X).all():
        raise ValueError('Invalid embedding dataset')
    table = pd.read_csv(label_path, dtype={'id': str})
    if list(table.columns) != ['id']+LABELS or table.id.duplicated().any() or len(set(ids)) != len(ids):
        raise ValueError('Invalid label schema or duplicate IDs')
    if set(table.id) != set(ids): raise ValueError('Labels and embeddings have different IDs')
    y = table.set_index('id').loc[ids, LABELS].to_numpy()
    if not all(set(y[:,j]) == {0,1} for j in range(5)): raise ValueError('Both binary classes are required')
    return X, y


def read_submission(path, fit_path, eval_path):
    if Path(path).stat().st_size > 32_000_000:
        raise ValueError('Submission exceeds 32 MB')
    keys = {'train_embeddings', 'train_ids', 'eval_embeddings', 'eval_ids'}
    with zipfile.ZipFile(path) as z:
        if len(z.infolist()) != 4 or set(z.namelist()) != {k+'.npy' for k in keys}:
            raise ValueError('Expected exactly four submission arrays')
        if sum(i.file_size for i in z.infolist()) > 32_000_000:
            raise ValueError('Uncompressed submission exceeds 32 MB')
    arrays = []
    with np.load(path, allow_pickle=False) as a:
        for prefix, original_path in [('train', fit_path), ('eval', eval_path)]:
            values, ids = a[prefix+'_embeddings'], a[prefix+'_ids']
            with np.load(original_path, allow_pickle=False) as original:
                expected_ids = original['ids'].astype(str)
                expected_shape = original['X'].shape
            if values.shape != expected_shape or values.dtype.kind not in 'fiu':
                raise ValueError('Incorrect embedding dimensions or dtype')
            if not np.isfinite(values).all() or np.max(np.abs(values)) > 1e6:
                raise ValueError('Embeddings must be finite and abs <= 1e6')
            if ids.ndim != 1 or ids.dtype.kind != 'U' or len(ids) != len(values):
                raise ValueError('IDs must be a one-dimensional Unicode string array')
            if len(set(ids)) != len(ids) or set(ids) != set(expected_ids):
                raise ValueError('Duplicate, missing or unknown IDs')
            lookup = {v:i for i,v in enumerate(ids)}
            arrays.append(values[[lookup[v] for v in expected_ids]].astype(float))
    return arrays


def probe(X, y, Z, t):
    with threadpool_limits(limits=1):
        center = X.mean(axis=0)
        _, singular, V = np.linalg.svd(X-center, full_matrices=False)
        basis = V[singular > max(float(singular[0])*1e-6, 1e-12)].T
        if basis.shape[1] == 0: return 0.5, 0.5
        train, test = (X-center) @ basis, (Z-center) @ basis
        auc = []
        for j in range(5):
            scores = []
            for C in ([1.0] if j < 4 else [0.01, 1.0, 100.0]):
                model = make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=1000, solver='lbfgs'))
                model.fit(train, y[:,j])
                value = roc_auc_score(t[:,j], model.predict_proba(test)[:,1])
                scores.append(max(value, 1-value) if j == 4 else value)
            auc.append(max(scores))
    return float(np.mean(auc[:4])), float(auc[4])


def raw_quality(utility, leakage, original_utility, original_leakage):
    u = float(np.clip((utility-.5)/(original_utility-.5), 0, 1))
    d = float(np.clip((original_leakage-leakage)/(original_leakage-.5), 0, 1))
    h = 2*u*d/(u+d) if u+d else 0.0
    return u, d, h


def evaluate(submission, fit_embeddings, fit_labels, eval_embeddings, eval_labels, calibration):
    paths = [fit_embeddings, fit_labels, eval_embeddings, eval_labels]
    config = json.loads(Path(calibration).read_text())
    if config.get('fingerprint') != fingerprint(paths): raise ValueError('Calibration does not match this dataset and split')
    for key in ['utility_original','leakage_original','reference_h']:
        if not isinstance(config.get(key),(int,float)) or not np.isfinite(config[key]): raise ValueError('Invalid calibration')
    if not (.5 < config['utility_original'] <= 1 and .5 < config['leakage_original'] <= 1 and 0 < config['reference_h'] <= 1):
        raise ValueError('Invalid calibration range')
    A, B = read_submission(submission, fit_embeddings, eval_embeddings)
    X,y = read_data(fit_embeddings,fit_labels); Z,t = read_data(eval_embeddings,eval_labels)
    utility,leakage = probe(A,y,B,t)
    u,d,h = raw_quality(utility,leakage,config['utility_original'],config['leakage_original'])
    return dict(score=float(np.clip(100*h/config['reference_h'],0,100)), utility_auc=utility,
                source_auc=leakage, preservation=u, removal=d, h=h)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--submission',required=True)
    p.add_argument('--fit-embeddings',required=True);p.add_argument('--fit-labels',required=True)
    p.add_argument('--eval-embeddings',required=True);p.add_argument('--eval-labels',required=True)
    p.add_argument('--calibration',required=True)
    a=p.parse_args()
    try: result=evaluate(a.submission,a.fit_embeddings,a.fit_labels,a.eval_embeddings,a.eval_labels,a.calibration)
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        print(f'Error: {exc}',file=sys.stderr);return 2
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0

if __name__=='__main__':raise SystemExit(main())
