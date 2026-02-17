"""
=============================================================================
  Week 1 — ML Engineer
  File: baseline_match.py
  Purpose: Reproduce the baseline matching pipeline and verify match results.
=============================================================================

This script runs the matching algorithm that compares public submissions
against registered cases using KNN on face-mesh landmarks.

Usage:
    python baseline_match.py
=============================================================================
"""

import os
import sys
import json
import traceback
import warnings
from collections import defaultdict

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings(action="ignore")

# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------
def get_public_cases_data(status="NF"):
    """Fetch public submissions with face-mesh data."""
    from pages.helper import db_queries

    try:
        result = db_queries.fetch_public_cases(train_data=True, status=status)
        d1 = pd.DataFrame(result, columns=["label", "face_mesh"])
        d1["face_mesh"] = d1["face_mesh"].apply(lambda x: json.loads(x))
        d2 = pd.DataFrame(
            d1.pop("face_mesh").values.tolist(), index=d1.index
        ).rename(columns=lambda x: f"fm_{x + 1}")
        df = d1.join(d2)
        for col in df.columns:
            if col != "label":
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    except Exception as e:
        traceback.print_exc()
        return None


def get_registered_cases_data(status="NF"):
    """Fetch registered cases with face-mesh data."""
    from pages.helper.db_queries import engine
    from pages.helper.data_models import RegisteredCases
    from sqlmodel import Session, select

    try:
        with Session(engine) as session:
            result = session.exec(
                select(
                    RegisteredCases.id,
                    RegisteredCases.face_mesh,
                    RegisteredCases.status,
                )
            ).all()
            d1 = pd.DataFrame(result, columns=["label", "face_mesh", "status"])
            if status:
                d1 = d1[d1["status"] == status]
            d1["face_mesh"] = d1["face_mesh"].apply(lambda x: json.loads(x))
            d2 = pd.DataFrame(
                d1.pop("face_mesh").values.tolist(), index=d1.index
            ).rename(columns=lambda x: f"fm_{x + 1}")
            df = d1.join(d2)
            for col in df.columns:
                if col not in ["label", "status"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
            return df
    except Exception as e:
        traceback.print_exc()
        return None


# ---------------------------------------------------------------------------
# Matching function
# ---------------------------------------------------------------------------
def match(distance_threshold: float = 3.0) -> dict:
    """
    For each public submission, find the nearest registered case using KNN.
    If the distance is >= threshold, consider it a match.

    Parameters
    ----------
    distance_threshold : float
        Minimum distance to accept as a match (higher = more lenient).

    Returns
    -------
    dict with 'status' and 'result' (mapping: registered_id → [public_ids]).
    """
    public_df = get_public_cases_data()
    registered_df = get_registered_cases_data()

    if public_df is None or registered_df is None:
        return {"status": False, "message": "Couldn't connect to database."}
    if len(public_df) == 0 or len(registered_df) == 0:
        return {"status": False, "message": "No public or registered cases found."}

    original_reg_labels = registered_df.iloc[:, 0].tolist()
    original_pub_labels = public_df.iloc[:, 0].tolist()

    reg_features = registered_df.iloc[:, 2:].values.astype(float)
    numeric_labels = list(range(len(reg_features)))

    knn = KNeighborsClassifier(
        n_neighbors=1, algorithm="ball_tree", weights="distance"
    )
    knn.fit(reg_features, numeric_labels)

    matched_images = defaultdict(list)

    for i, row in public_df.iterrows():
        pub_label = original_pub_labels[i]
        face_encoding = np.array(row[1:]).astype(float)

        try:
            closest_distances = knn.kneighbors([face_encoding])[0][0]
            closest_distance = np.min(closest_distances)

            if closest_distance >= distance_threshold:
                predicted_idx = knn.predict([face_encoding])[0]
                reg_label = original_reg_labels[predicted_idx]
                matched_images[reg_label].append(pub_label)
                print(
                    f"  ✅ Public {pub_label[:8]}… → Registered {reg_label[:8]}… "
                    f"(dist={closest_distance:.4f})"
                )
            else:
                print(
                    f"  ❌ Public {pub_label[:8]}… — no match "
                    f"(dist={closest_distance:.4f} < threshold {distance_threshold})"
                )
        except Exception as e:
            print(f"  ⚠️  Error on {pub_label[:8]}…: {e}")

    return {"status": True, "result": dict(matched_images)}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🔄 Running baseline matching algorithm…\n")
    result = match()
    print(f"\n📋 Match result: {result}")
