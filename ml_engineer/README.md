# Week 1 — ML Engineer

## Objective
Reproduce the baseline training and matching pipelines on sample data.
Verify that `classifier.pkl` is generated and predictions work end-to-end.

## Files Delivered
| File                | Purpose                                                  |
|---------------------|----------------------------------------------------------|
| `baseline_train.py` | Self-contained training script — trains KNN, saves model.|
| `baseline_match.py` | Runs matching between public submissions & registered cases.|
| `verify_model.py`   | Loads `classifier.pkl` and runs sanity checks + dummy prediction.|

## How to Run
```bash
# First, ensure the backend has seeded sample data:
cd ../backend_engineer
python migrations.py
python seed_data.py

# Then run ML scripts:
cd ../ml_engineer
python baseline_train.py     # Train model
python verify_model.py       # Verify saved model
python baseline_match.py     # Run matching
```

## Key Observations (Week 1)
- KNN uses **ball_tree** algorithm on **1404 features** (468 MediaPipe landmarks × 3).
- `n_neighbors` is set to `len(labels)` — every sample is a neighbor. This is unusual
  and will be tuned in Week 3.
- Model is serialized as a `(LabelEncoder, KNeighborsClassifier)` pickle tuple.
- Match threshold logic uses `distance >= threshold` (higher distance = accepted match).
  This needs review — typically lower distance = better match.

## Next Week Preview
- Validate and clean features from `extract_face_mesh_landmarks()`.
- Implement normalization / scaling and NaN handling.
