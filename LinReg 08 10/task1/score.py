"""Evaluate a submission against labels and matching calibration.

python score.py task1/validation.csv predictions.csv task1/validation_calibration.json
"""
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def read_table(path, *, submission=False):
    path = Path(path)
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, [])
        if not header or len(header) != len(set(header)):
            raise ValueError(f'{path.name}: empty or duplicate column names')
        if submission and (len(header) != 2 or set(header) != {'id', 'target'}):
            raise ValueError(f'{path.name}: submission columns must be id,target')
        if not {'id', 'target'} <= set(header):
            raise ValueError(f'{path.name}: required columns are id,target')
        for row_number, row in enumerate(reader, 2):
            if len(row) != len(header):
                raise ValueError(f'{path.name}: wrong number of fields in row {row_number}')
    table = pd.read_csv(path, dtype={'id': str}, keep_default_na=False, encoding='utf-8-sig')
    if table.empty:
        raise ValueError(f'{path.name}: file contains no data rows')
    if table.id.str.strip().eq('').any() or table.id.duplicated().any():
        raise ValueError(f'{path.name}: IDs must be nonempty and unique')
    try:
        target = pd.to_numeric(table.target, errors='raise').to_numpy(dtype=float)
    except (ValueError, TypeError) as exc:
        raise ValueError(f'{path.name}: target must contain numbers') from exc
    if not np.isfinite(target).all():
        raise ValueError(f'{path.name}: target must contain finite numbers')
    table['target'] = target
    return table


def evaluate(truth_path, submission_path, calibration_path):
    truth = read_table(truth_path)
    submission = read_table(submission_path, submission=True)
    if set(truth.id) != set(submission.id):
        raise ValueError('Submission IDs must exactly match the evaluated split')
    pred = submission.set_index('id').loc[truth.id, 'target'].to_numpy()
    target = truth.target.to_numpy()
    with Path(calibration_path).open(encoding='utf-8') as f:
        calibration = json.load(f)
    if not isinstance(calibration, dict):
        raise ValueError('Calibration must be a JSON object')
    values = []
    for key in ['baseline_constant', 'mse_baseline', 'mse_reference']:
        v = calibration.get(key)
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not np.isfinite(v):
            raise ValueError(f'Invalid calibration field: {key}')
        values.append(float(v))
    constant, mse_baseline, mse_reference = values
    if not 0 <= mse_reference < mse_baseline:
        raise ValueError('Expected 0 <= mse_reference < mse_baseline')
    with np.errstate(over='ignore', invalid='ignore'):
        actual_baseline = float(np.mean((target-constant)**2))
        mse = float(np.mean((target-pred)**2))
    if not np.isfinite(mse) or not np.isfinite(actual_baseline):
        raise ValueError('Squared error is outside the supported numeric range')
    if not np.isclose(actual_baseline, mse_baseline, rtol=1e-9, atol=1e-9):
        raise ValueError('Calibration does not match the supplied ground truth')
    value = 100*(mse_baseline-mse)/(mse_baseline-mse_reference)
    return {'mse': mse, 'score': float(np.clip(value, 0, 100))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('truth', help='CSV with id,target; extra feature columns are allowed')
    parser.add_argument('submission', help='CSV with exactly id,target')
    parser.add_argument('calibration', help='Matching calibration JSON')
    args = parser.parse_args()
    try:
        result = evaluate(args.truth, args.submission, args.calibration)
    except (OSError, ValueError, TypeError, csv.Error) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        return 2
    print(f'MSE={result["mse"]:.6f}; score={result["score"]:.2f}/100')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
