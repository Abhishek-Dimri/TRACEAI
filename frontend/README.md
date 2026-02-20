# Week 1 — Frontend Developer

## Objective
Set up the dev environment, verify Streamlit authentication works with
`login_config.yml`, audit the existing UI for UX bugs, and apply quick fixes.

## Files Delivered
| File              | Purpose                                                         |
|-------------------|-----------------------------------------------------------------|
| `verify_auth.py`  | Standalone script to validate `login_config.yml` (structure, password hashes, cookie config). |
| `Home_fixed.py`   | Improved `Home.py` with page config, native Streamlit components, and better error handling. |
| `ux_audit.md`     | Detailed audit of all pages — 12 issues found, 4 fixed this week. |

## How to Run
```bash
cd college_project/frontend_developer

# Verify auth config (no Streamlit needed)
python verify_auth.py

# Run the improved Home page
streamlit run Home_fixed.py
```

## Login Credentials (from login_config.yml)
| Username | Password | Role  |
|----------|----------|-------|
| gagan    | abc      | Admin |

## Key Fixes Applied
1. Added `st.set_page_config()` for proper page title and icon.
2. Replaced raw HTML user info display with native Streamlit (`st.title`, `st.caption`).
3. Improved error messages with emoji indicators.
4. Documented 12 UX issues across all pages (see `ux_audit.md`).

## Next Week Preview
- Improve upload UX (progress indicators, image previews, face-mesh error messages).
- Add input validation for phone numbers and Aadhaar.
