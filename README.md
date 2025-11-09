# Hospital Equipment Management (Migration Planning)

This repository currently contains the legacy Tkinter-based hospital equipment management application (`hospital_app.py`) **and** the first-phase scaffolding for the new FastAPI backend.

The long-term goal is to modernize the solution into a web-based platform built with FastAPI, PostgreSQL, and a React (Vite + TypeScript) frontend. A comprehensive migration plan describing the target architecture, feature set, DevOps workflow, and implementation roadmap is available at [`docs/web_app_migration_plan.md`](docs/web_app_migration_plan.md).

## Repository Layout

```
.
├── README.md
├── backend/
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   └── main.py
│   ├── requirements*.txt
│   └── .env.example
├── docs/
│   └── web_app_migration_plan.md
└── hospital_app.py  # legacy Tkinter + SQLite implementation
```

## Next Steps

- Review the migration plan to understand the desired end state and phased delivery approach.
- Use the plan as the blueprint for creating the new backend (`backend/`) and frontend (`frontend/`) services.
- Track progress against the acceptance criteria checklist defined in the plan.

## Phase 1 Progress – Backend Foundation

- [x] Establish FastAPI project skeleton (`backend/app`)
- [x] Implement normalized SQLAlchemy models with enumerations and relationships
- [x] Configure Pydantic settings and async database session helpers
- [x] Generate Alembic environment and initial migration
- [x] Provide baseline health-check endpoint

Subsequent phases will layer in authentication, CRUD routers, service logic, frontend implementation, Docker tooling, automated tests, and data migration utilities as outlined in the migration blueprint.

## License

Specify the project license here.
