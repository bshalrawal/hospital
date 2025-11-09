# Hospital Equipment Management - Web App Migration Plan

This document outlines the migration of the legacy Tkinter + SQLite desktop application to a modern FastAPI + React (Vite + TypeScript) web application. It captures the desired architecture, feature set, and implementation roadmap needed to ship a production-ready platform for managing the full lifecycle of hospital equipment.

## 1. Current State

- **Application**: Single-file Tkinter desktop GUI (`hospital/hospital_app.py`).
- **Database**: SQLite database with five loosely normalized tables (`department`, `vendor`, `equipment`, `issue_report`, `discard_equipment`).
- **Features**: CRUD flows, simple dashboard statistics, media file handling through raw paths.
- **Limitations**: Desktop-only usage, no authentication/authorization, limited reporting, manual media management.

## 2. Target Architecture Overview

| Layer      | Technology & Standards |
|------------|------------------------|
| Backend    | FastAPI, SQLAlchemy 2.0 ORM, Pydantic v2, Alembic migrations, async execution. |
| Frontend   | React 18 + Vite, TypeScript (strict), Material-UI, React Query, React Router, React Hook Form, Yup. |
| Database   | PostgreSQL in production (SQLite for development/testing). |
| Auth       | JWT-based access tokens + refresh tokens with role-based access control (admin, technician, viewer). |
| Storage    | Local filesystem (dev) and AWS S3 with presigned URLs (prod) behind an abstraction layer. |
| Deployment | Docker Compose (services: api, db, web) with CI/CD via GitHub Actions and pre-commit hooks. |

Key success criteria include:

- Secure authentication and authorization flows.
- Fully normalized relational model with referential integrity.
- REST API with pagination, search, filtering, and consistent response envelopes.
- Feature-complete React frontend with responsive layout, server-driven tables, and robust forms.
- File upload pipeline with validation and storage abstraction.
- Data migration path from the existing SQLite database, including historical media assets.
- One-command local environment (`docker compose up`) and automated CI quality gates.

## 3. Database Schema & Models

### 3.1 Normalization Highlights

1. Replace free-text department field on equipment with a `department_id` foreign key.
2. Issue and discard tables reference equipment by `equipment_id` and drop duplicated equipment details.
3. Remove redundant vendor contact data from equipment, relying on `vendor_id` foreign key.
4. Promote TEXT date columns to real DATE/DateTime types.
5. Encode status fields as PostgreSQL ENUMs for data integrity.

### 3.2 SQLAlchemy Models (Async ORM)

Models live under `backend/app/models/` with shared metadata for Alembic:

- **Department**: `department_id`, unique `department_name`, timestamps, relationship to equipment.
- **Vendor**: core contact details plus optional category metadata.
- **Equipment**: primary lifecycle entity capturing department/vendor FK, serial number, purchase/expiry dates, quantity, and `EquipmentStatus` enum.
- **IssueReport**: FK to equipment, `IssueType` and `IssueStatus` enums, problem description, optional media URL, technician attribution, timestamps.
- **DiscardEquipment**: One-to-one with equipment (enforced via unique FK), reason/media/date metadata.
- **User**: Authentication entity with `UserRole` enum, hashed password, activity flags, timestamps.
- **RefreshToken**: Stores hashed refresh tokens for logout/rotation support.

Enums (`EquipmentStatus`, `IssueType`, `IssueStatus`, `UserRole`) are defined in `backend/app/models/enums.py` and migrated as PostgreSQL ENUM types.

## 4. Backend API Design

- Base path: `/api/v1` with consistent JSON envelopes (`{"data": ...}` plus optional pagination metadata).
- Authentication via Bearer access tokens; refresh handled through httpOnly cookie workflow.
- Pagination (`page`, `page_size`), search (`search`), sorting (`sort_by`, `sort_order`), and filter parameters implemented on list endpoints.
- Pydantic schemas under `backend/app/schemas/` define create/update/response DTOs.
- CRUD logic is implemented in service modules under `backend/app/crud/` to keep routers thin.

### 4.1 Endpoint Summary

| Domain       | Router Path                 | Access Highlights |
|--------------|-----------------------------|-------------------|
| Departments  | `/api/v1/departments`       | Admin CRUD, unique name validation, deletion guard if equipment exists. |
| Vendors      | `/api/v1/vendors`           | Technician/Admin write access, email validation, equipment usage guard on delete. |
| Equipment    | `/api/v1/equipment`         | Extensive filters (status, department, vendor, date ranges, expired flag), nested relations in responses. |
| Issues       | `/api/v1/issues`            | Technician/Admin write access, automatic `resolved_at` handling, optional media. |
| Discards     | `/api/v1/discards`          | Technician/Admin write access, status side-effects on equipment, restore path for admins. |
| Dashboard    | `/api/v1/dashboard/stats`   | Aggregated metrics for cards & charts, optimized SQL queries. |
| Upload       | `/api/v1/upload` / `/files` | Validated media uploads (<=50 MB, allowed MIME), storage abstraction. |
| Health       | `/api/v1/health`            | Public readiness check (DB + storage capacity). |
| Auth         | `/api/v1/auth/*`            | Register (admin-only), login, refresh, logout, `me`. |

### 4.2 Error Handling & Observability

- Custom exception handlers for 401/403/404/422/500 responses with standardized payloads.
- Request ID middleware for traceability.
- Structured logging with configurable log level (`LOG_LEVEL`).

## 5. Frontend Application Plan

- Organized Vite + React + TypeScript project under `frontend/` with domain-focused folders (`api/`, `components/`, `pages/`, `hooks/`, `store/`, `types/`, `utils/`).
- Main layout (`MainLayout.tsx`) combines persistent navigation drawer, top app bar with user menu, and responsive breakpoints.
- Routing via React Router v6 with `ProtectedRoute` and role-based guards.
- React Query manages server state; Zustand stores handle auth tokens and lightweight UI state (e.g., nav collapse, theme preference).
- Forms built with React Hook Form + Yup validation schemas (`frontend/src/utils/validation.ts`).
- Shared UI primitives (DataTable, FilterPanel, FileUpload, ConfirmDialog, StatusBadge) provide consistent interactions.
- Dashboard page presents eight KPI cards, equipment status pie chart, issues trend line chart, and expiring equipment alerts.
- CRUD pages for Equipment, Vendors, Issues, Discards, plus admin-only Departments and Users management views. Server-side pagination/search/filtering is surfaced through reusable DataTable component.
- Login flow handles credential submission, stores access token in memory, and triggers refresh flow via Axios interceptors.

## 6. File Storage Strategy

- Storage interface (`StorageBackend`) with local and S3 implementations (`backend/app/storage/`).
- File validation utilities enforce max size (50 MB) and MIME/extension checks using `python-magic`.
- Upload endpoint saves files to `UPLOAD_DIR` (dev) or S3, returning API-served URLs (`/api/v1/files/{filename}`) or presigned links.
- Scheduled cleanup task removes orphaned media files (configurable via `ENABLE_MEDIA_CLEANUP`).

## 7. DevOps & Tooling

- **Docker Compose** (dev) orchestrates PostgreSQL, FastAPI (with autoreload), and Vite dev server. Production compose uses built images (FastAPI + Gunicorn/Uvicorn, Nginx for static assets).
- **Environment configuration**: `.env.example` files for backend/fronted document required secrets (DB URL, JWT secret, storage backend, first admin credentials, API base URL, etc.).
- **GitHub Actions CI**: lint (ruff, black, mypy, eslint, prettier), tests (pytest with coverage, Vitest), type checks, and Docker build verification across backend/frontend jobs.
- **Pre-commit**: Formatters, linters, YAML/JSON validators enforce code hygiene before commits.
- **Local development**: Documented workflows for Docker and bare-metal setups, including Alembic migrations and seed data scripts.

## 8. Data Migration & Validation

- Alembic manages schema migrations starting with an "initial schema" revision that creates ENUMs and normalized tables with indexes.
- Seed script provides sample departments, vendors, equipment, issues, discards, and user roles for local testing.
- SQLite import script (`backend/scripts/import_sqlite.py`) migrates legacy data by:
  - Mapping departments/vendors/equipment to new FK-based schema.
  - Converting statuses to enums and dates to proper types.
  - Copying media assets into the new storage backend.
  - Logging skipped/duplicate records with summary output.
- Data validation script checks referential integrity, enum constraints, discarded equipment status alignment, and orphaned media.

## 9. Testing Strategy

- **Backend** (`pytest`, `pytest-asyncio`):
  - Fixtures for async DB session, authenticated users by role, sample data.
  - Coverage goals ≥80% focusing on routers, CRUD services, auth flows, file upload validation.
- **Frontend** (`Vitest`, React Testing Library):
  - Unit tests for utilities and components (DataTable, FileUpload, forms).
  - Integration tests for form validation and auth store behavior.
  - Optional Playwright E2E smoke suite wired into CI.

## 10. Acceptance Criteria Checklist

1. `/docs` exposes complete OpenAPI documentation.
2. Authenticated routes reject unauthenticated requests (401) and enforce role-based permissions (403).
3. List endpoints implement pagination, search, and filtering; UI tables mirror these capabilities.
4. CRUD forms handle validation, submission, optimistic UX, and display server errors.
5. File uploads enforce size/type rules and render in detail views.
6. Dashboard metrics/charts reflect real-time database state.
7. CI pipeline runs automatically and passes on clean checkout.
8. Data import script successfully migrates existing SQLite dataset including media.
9. `docker compose up` boots the full stack with seeded admin user.

## 11. Implementation Roadmap (6–8 Weeks)

1. **Backend foundation**: project scaffolding, models, migrations, CRUD services.
2. **Auth & users**: JWT issuance, refresh token model, bootstrap admin, role dependencies.
3. **REST API completion**: routers, validation, response schemas, upload handling, dashboard metrics.
4. **Backend testing**: pytest coverage, fixtures, quality gates.
5. **Frontend scaffolding**: Vite setup, layout shell, routing, auth store.
6. **Domain pages & components**: data tables, forms, dashboard visuals, shared UI primitives.
7. **DevOps tooling**: Dockerfiles, Compose, pre-commit, GitHub Actions, README documentation.
8. **Data migration**: seed + SQLite import scripts, validation routines.
9. **Polish & verification**: accessibility, performance tuning, acceptance checklist sign-off.

## 12. Additional Notes

- Follow WCAG 2.1 AA accessibility guidelines (keyboard navigation, ARIA labels, contrast ratios).
- Optimize frontend performance with route-based code splitting, lazy-loaded images, and React Query caching.
- Plan for future enhancements such as S3 storage, Redis caching, or service worker offline support by keeping abstractions clean.

This migration plan serves as the blueprint for transforming the legacy desktop tooling into a secure, scalable, and maintainable web platform suitable for production hospital environments.
