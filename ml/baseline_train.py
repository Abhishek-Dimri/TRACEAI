"""
=============================================================================
  Week 1 — ML Engineer
  File: baseline_train.py
  Purpose: Reproduce the baseline KNN training pipeline and verify that
           a classifier.pkl file is generated correctly.
=============================================================================

This script mirrors the original `train_model.py` logic but is self-contained
so the ML engineer can run and debug it independently.

Usage:
    python baseline_train.py
=============================================================================
"""

import os
import sys
import json
import pickle
import traceback

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier

# ---------------------------------------------------------------------------
# Add the sibling backend/ folder so we can import db_queries & data_models
# ---------------------------------------------------------------------------
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, BACKEND_DIR)


# ---------------------------------------------------------------------------
# Data loader — fetch face-mesh training rows from the database
# ---------------------------------------------------------------------------
def get_train_data(submitted_by: str):
    """
    Query the database for (id, face_mesh) rows belonging to `submitted_by`
    with status = 'NF', then expand the JSON face-mesh into feature columns.

    Returns
    -------
    labels : pd.Series   — case IDs (used as class labels)
    features : pd.DataFrame — numeric face-mesh columns (fm_1 … fm_1404)
    """
    # Change working directory to backend/ so SQLite DB is found
    original_cwd = os.getcwd()
    os.chdir(BACKEND_DIR)

    import db_queries
    result = db_queries.get_training_data(submitted_by)

    os.chdir(original_cwd)

    if not result:
        return pd.Series(dtype=str), pd.DataFrame()

    d1 = pd.DataFrame(result, columns=["label", "face_mesh"])
    d1["face_mesh"] = d1["face_mesh"].apply(lambda x: json.loads(x))

    d2 = pd.DataFrame(
        d1.pop("face_mesh").values.tolist(), index=d1.index
    ).rename(columns=lambda x: f"fm_{x + 1}")

    df = d1.join(d2)
    return df["label"], df.drop("label", axis=1)


# ---------------------------------------------------------------------------
# Training function
# ---------------------------------------------------------------------------
MODEL_FILE = "classifier.pkl"


def train(submitted_by: str) -> dict:
    """
    Train a K-Nearest Neighbors classifier on the registered cases and
    serialize the model + label encoder to `classifier.pkl`.

    Parameters
    ----------
    submitted_by : str
        The username whose cases should be used for training.

    Returns
    -------
    dict with keys 'status' (bool) and 'message' (str).
    """
    # Remove stale model
    if os.path.isfile(MODEL_FILE):
        os.remove(MODEL_FILE)

    try:
        labels, key_pts = get_train_data(submitted_by)

        if len(labels) == 0:
            return {"status": False, "message": "No cases submitted by this user."}

        # Encode string labels → integers
        le = LabelEncoder()
        encoded_labels = le.fit_transform(labels)

        # Build KNN classifier
        classifier = KNeighborsClassifier(
            n_neighbors=len(labels),
            algorithm="ball_tree",
            weights="distance",
        )
        classifier.fit(key_pts, encoded_labels)

        # Save (LabelEncoder, KNN) tuple
        with open(MODEL_FILE, "wb") as f:
            pickle.dump((le, classifier), f)

        file_size = os.path.getsize(MODEL_FILE)
        return {
            "status": True,
            "message": f"Model trained & saved ({file_size:,} bytes). "
                       f"Classes: {len(le.classes_)}, Features: {key_pts.shape[1]}.",
        }

    except Exception as e:
        traceback.print_exc()
        return {"status": False, "message": str(e)}


# ---------------------------------------------------------------------------
# Verification — load the saved model and print summary
# ---------------------------------------------------------------------------
def verify_model():
    """Load classifier.pkl and print basic stats."""
    if not os.path.isfile(MODEL_FILE):
        print("❌ classifier.pkl not found — run train() first.")
        return

    with open(MODEL_FILE, "rb") as f:
        le, clf = pickle.load(f)

    print("✅ Model loaded successfully.")
    print(f"   Label Encoder classes : {list(le.classes_)}")
    print(f"   KNN n_neighbors       : {clf.n_neighbors}")
    print(f"   KNN algorithm         : {clf.algorithm}")
    print(f"   KNN metric            : {clf.metric}")
    print(f"   Training samples      : {clf.n_samples_fit_}")
    print(f"   Feature dimensions    : {clf.n_features_in_}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    user = "Gagandeep Singh"  # default user from login_config.yml
    print(f"🔄 Training baseline model for user: {user}\n")
    result = train(user)
    print(f"\n📋 Result: {result}\n")
    verify_model()
