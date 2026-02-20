# =============================================================================
#   Week 1 — Frontend Developer
#   File: ux_audit.md
#   Purpose: Document UX bugs found and fixes applied during Week 1.
# =============================================================================

# UX Audit — Week 1 Findings

## 1. Home.py — Login Page

| # | Issue | Severity | Status | Fix |
|---|-------|----------|--------|-----|
| 1 | No page title set (`st.set_page_config` missing in Home.py) | Medium | 🔧 Fixed | Added `st.set_page_config(page_title="Find Missing Person")` |
| 2 | Raw HTML used for name/area/role display — not accessible | Low | 📋 Noted | Will replace with `st.header()` / `st.subheader()` in Week 2 |
| 3 | No feedback when login_config.yml is missing beyond `st.error` | Low | 📋 Noted | Consider fallback instructions |
| 4 | Dashboard metrics show count but no link to view cases | Low | 📋 Noted | Will add navigation buttons in Week 4 |

## 2. Register New Case (pages/1_Register New Case.py)

| # | Issue | Severity | Status | Fix |
|---|-------|----------|--------|-----|
| 1 | No validation on mobile number (accepts any string) | High | 📋 Noted | Will add regex validation in Week 2 |
| 2 | No feedback if face mesh extraction fails — form still shows | Medium | 🔧 Fixed | Added guard: hide form if `face_mesh is None` |
| 3 | Image preview loads before processing completes — confusing | Low | 📋 Noted | Move image display inside spinner |
| 4 | `uuid` imported twice (line 1 and line 40) | Low | 🔧 Fixed | Removed duplicate import |

## 3. Mobile App (mobile_app.py)

| # | Issue | Severity | Status | Fix |
|---|-------|----------|--------|-----|
| 1 | No authentication required — anyone can submit | Medium | 📋 Noted | Discuss with team — intentional for public use? |
| 2 | Same face-mesh failure issue as Register page | Medium | 🔧 Fixed | Added guard |
| 3 | No success/error summary after submission | Low | 📋 Noted | Will improve in Week 2 |

## 4. Match Cases (pages/3_Match Cases.py)

| # | Issue | Severity | Status | Fix |
|---|-------|----------|--------|-----|
| 1 | Train button doesn't show progress/spinner | Medium | 📋 Noted | Will add in Week 3 |
| 2 | Match results not clearly formatted | Medium | 📋 Noted | Will add thumbnails in Week 4 |

## Summary
- **Total issues found**: 12
- **Fixed this week**: 4
- **Noted for future weeks**: 8
