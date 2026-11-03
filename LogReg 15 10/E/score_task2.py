"""Score a CSV submission of binary predictions."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
FEATURE_COLUMNS = ['amount','customer_mean_amount','seconds_since_previous','hour','location_dx','location_dy']


def fingerprint(data,labels=None):
    h=hashlib.sha256()
    for p in [data]+([labels] if labels is not None else []):
        b=Path(p).read_bytes();h.update(len(b).to_bytes(8,'big'));h.update(b)
    return h.hexdigest()


def evaluate(submission,data,calibration,labels=None):
    frame=pd.read_csv(data,dtype={'id':str})
    expected=['id']+FEATURE_COLUMNS+(['target'] if labels is None else [])
    if list(frame.columns)!=expected or frame.id.isna().any() or frame.id.duplicated().any():
        raise ValueError('Invalid data schema or IDs')
    if not np.isfinite(frame[FEATURE_COLUMNS].to_numpy()).all():raise ValueError('Non-finite input data')
    if labels is None: y=frame.target.to_numpy()
    else:
        truth=pd.read_csv(labels,dtype={'id':str})
        if list(truth.columns)!=['id','target'] or truth.id.duplicated().any() or set(truth.id)!=set(frame.id):
            raise ValueError('Invalid labels or IDs')
        y=truth.set_index('id').loc[frame.id,'target'].to_numpy()
    if set(y)!={0,1}:raise ValueError('Expected both binary classes')
    config=json.loads(Path(calibration).read_text())
    if config.get('fingerprint')!=fingerprint(data,labels):raise ValueError('Calibration does not match this split')
    reference=config.get('reference_j')
    if isinstance(reference,bool) or not isinstance(reference,(int,float)) or not np.isfinite(reference) or not 0<reference<=1:
        raise ValueError('Invalid calibration')
    if Path(submission).stat().st_size > 10_000_000: raise ValueError('Submission exceeds 10 MB')
    submitted = pd.read_csv(submission, dtype={'id':str})
    if list(submitted.columns) != ['id','target'] or submitted.id.isna().any() or submitted.id.duplicated().any():
        raise ValueError('Expected id,target and unique nonempty IDs')
    if set(submitted.id) != set(frame.id): raise ValueError('Missing or unknown IDs')
    if not submitted.target.isin([0,1]).all(): raise ValueError('target must contain only binary classes 0 or 1')
    predictions = submitted.set_index('id').loc[frame.id,'target'].to_numpy(dtype=int)
    tn,fp,fn,tp=confusion_matrix(y,predictions,labels=[0,1]).ravel()
    tpr=tp/(tp+fn);fpr=fp/(fp+tn);j=float(tpr-fpr)
    return dict(score=float(np.clip(100*j/reference,0,100)),j=j,tpr=float(tpr),fpr=float(fpr),
                tp=int(tp),fp=int(fp),tn=int(tn),fn=int(fn))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--submission',required=True);p.add_argument('--data',required=True)
    p.add_argument('--calibration',required=True);p.add_argument('--labels')
    a=p.parse_args()
    try:result=evaluate(a.submission,a.data,a.calibration,a.labels)
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print(f'Error: {exc}',file=sys.stderr);return 2
    print(json.dumps(result,ensure_ascii=False,indent=2));return 0

if __name__=='__main__':raise SystemExit(main())
