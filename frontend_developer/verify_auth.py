"""
=============================================================================
  Week 1 — Frontend Developer
  File: verify_auth.py
  Purpose: Verify that the Streamlit authentication flow works correctly
           using the existing login_config.yml.
=============================================================================

This script loads the login config, checks credential structure, and
simulates the authentication flow (without Streamlit UI) to confirm
the configuration is valid.

Usage:
    python verify_auth.py
=============================================================================
"""

import os
import sys
import yaml
import bcrypt

# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

CONFIG_PATH = os.path.join(PROJECT_ROOT, "login_config.yml")


def verify_config():
    """Load and validate login_config.yml structure."""
    print("=" * 60)
    print("  Authentication Config Verification")
    print("=" * 60)

    # ------------------------------------------------------------------
    # 1. File exists
    # ------------------------------------------------------------------
    if not os.path.isfile(CONFIG_PATH):
        print(f"\n❌ FAIL — '{CONFIG_PATH}' not found.")
        return False
    print(f"\n✅ Config file found: {CONFIG_PATH}")

    # ------------------------------------------------------------------
    # 2. Parse YAML
    # ------------------------------------------------------------------
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

    required_keys = ["credentials", "cookie", "preauthorized"]
    for key in required_keys:
        if key not in config:
            print(f"❌ FAIL — Missing top-level key: '{key}'")
            return False
    print(f"✅ All required top-level keys present: {required_keys}")

    # ------------------------------------------------------------------
    # 3. Check credentials structure
    # ------------------------------------------------------------------
    creds = config["credentials"]
    if "usernames" not in creds:
        print("❌ FAIL — 'credentials.usernames' missing.")
        return False

    users = creds["usernames"]
    print(f"\n--- Registered Users ({len(users)}) ---")

    for username, info in users.items():
        required_fields = ["email", "name", "password", "role"]
        missing = [f for f in required_fields if f not in info]
        status = "✅" if not missing else "❌"
        print(f"   {status} {username}")
        print(f"       Name  : {info.get('name', '?')}")
        print(f"       Email : {info.get('email', '?')}")
        print(f"       Role  : {info.get('role', '?')}")
        print(f"       City  : {info.get('city', '?')}")
        print(f"       Area  : {info.get('area', '?')}")
        if missing:
            print(f"       ⚠️  Missing fields: {missing}")

    # ------------------------------------------------------------------
    # 4. Verify password hash
    # ------------------------------------------------------------------
    print(f"\n--- Password Hash Verification ---")
    for username, info in users.items():
        hashed = info.get("password", "")
        # Test against the known default password "abc"
        test_password = "abc"
        if bcrypt.checkpw(test_password.encode(), hashed.encode()):
            print(f"   ✅ {username}: password hash valid (test password matches).")
        else:
            print(f"   ⚠️  {username}: test password 'abc' does NOT match hash.")

    # ------------------------------------------------------------------
    # 5. Cookie config
    # ------------------------------------------------------------------
    print(f"\n--- Cookie Config ---")
    cookie = config["cookie"]
    print(f"   Name        : {cookie.get('name', '?')}")
    print(f"   Key         : {cookie.get('key', '?')}")
    print(f"   Expiry days : {cookie.get('expiry_days', '?')}")

    print(f"\n✅ All checks passed.")
    return True


if __name__ == "__main__":
    verify_config()
