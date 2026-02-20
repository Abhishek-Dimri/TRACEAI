"""
=============================================================================
  Week 1 — ML Engineer
  File: verify_model.py
  Purpose: Load a saved classifier.pkl and run sanity checks.
=============================================================================

Checks performed:
  1. File exists and is loadable.
  2. Contains (LabelEncoder, KNeighborsClassifier) tuple.
  3. Prints summary stats (classes, features, algorithm).
  4. Runs a dummy prediction to confirm the pipeline works end-to-end.

Usage:
    python verify_model.py
=============================================================================
"""

import os
import pickle
import numpy as np


MODEL_FILE = "classifier.pkl"


def verify():
    print("=" * 60)
    print("  Model Verification Report")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. File existence
    # ------------------------------------------------------------------
    if not os.path.isfile(MODEL_FILE):
        print(f"\n❌ FAIL — '{MODEL_FILE}' not found.")
        print("   → Run baseline_train.py first to generate the model.")
        return False

    file_size = os.path.getsize(MODEL_FILE)
    print(f"\n✅ File found: {MODEL_FILE} ({file_size:,} bytes)")

    # ------------------------------------------------------------------
    # 2. Load & type check
    # ------------------------------------------------------------------
    with open(MODEL_FILE, "rb") as f:
        obj = pickle.load(f)

    if not isinstance(obj, tuple) or len(obj) != 2:
        print(f"❌ FAIL — Expected (LabelEncoder, KNN) tuple, got {type(obj)}")
        return False

    le, clf = obj
    print(f"✅ Loaded tuple: (LabelEncoder, {type(clf).__name__})")

    # ------------------------------------------------------------------
    # 3. Summary stats
    # ------------------------------------------------------------------
    print(f"\n--- LabelEncoder ---")
    print(f"   Classes       : {list(le.classes_)}")
    print(f"   Num classes   : {len(le.classes_)}")

    print(f"\n--- KNeighborsClassifier ---")
    print(f"   n_neighbors   : {clf.n_neighbors}")
    print(f"   algorithm     : {clf.algorithm}")
    print(f"   weights       : {clf.weights}")
    print(f"   metric        : {clf.metric}")
    print(f"   n_samples_fit : {clf.n_samples_fit_}")
    print(f"   n_features_in : {clf.n_features_in_}")

    # ------------------------------------------------------------------
    # 4. Dummy prediction
    # ------------------------------------------------------------------
    print(f"\n--- Dummy Prediction Test ---")
    dummy_input = np.random.rand(1, clf.n_features_in_)
    predicted_label_idx = clf.predict(dummy_input)[0]
    predicted_label = le.inverse_transform([predicted_label_idx])[0]
    distances, indices = clf.kneighbors(dummy_input)

    print(f"   Random input shape : {dummy_input.shape}")
    print(f"   Predicted class idx: {predicted_label_idx}")
    print(f"   Predicted label    : {predicted_label[:16]}…")
    print(f"   Nearest distance   : {distances[0][0]:.6f}")
    print(f"\n✅ All checks passed.")
    return True


if __name__ == "__main__":
    verify()
