# Backend compatibility patches

These patches run at startup so dependencies work on current Python/NumPy/Pydantic versions.

## 1. Windows stdout/stderr (main.py)

- **Issue:** `UnicodeEncodeError` when printing emoji or non-ASCII to console (cp1252).
- **Fix:** Wrap `sys.stdout`/`sys.stderr` in UTF-8 `TextIOWrapper` with `errors="replace"` on Windows.

## 2. ChromaDB + Pydantic 2.12 (chroma_pydantic_compat.py)

- **Issue:** ChromaDB’s `Settings` uses `BaseSettings` and has unannotated fields → `model-field-missing-annotation` and `unable to infer type for attribute`.
- **Fix:** Custom `BaseSettings` with a metaclass that injects type annotations for known ChromaDB fields and infers types for any other non-annotated attributes before Pydantic builds the model. `pydantic.BaseSettings` is patched at startup.

## 3. NumPy 2.0 type aliases (main.py)

- **Issue:** NumPy 2.0 removed `np.float_`, `np.int_`, `np.complex_`, etc. Dependencies (e.g. ChromaDB, hnswlib) still reference them → `was removed in the NumPy 2.0 release`.
- **Fix:** At startup, restore removed aliases on `numpy`: `float_`, `int_`, `complex_`, `string_`, `unicode_`, `str_`, `bool_`, `object_`, `longfloat`, `cfloat`, `clongfloat`, `singlecomplex`, `longcomplex` (see NumPy 2.0 migration guide).

## 4. Alembic URL `%` (alembic/env.py)

- **Issue:** `DATABASE_URL` with `%` (e.g. `%40` in password) triggers ConfigParser interpolation errors.
- **Fix:** Escape `%` as `%%` when setting `sqlalchemy.url` from `SYNC_DATABASE_URL`.

---

**Restart the backend** after changing any of these so patches are applied on startup.
