# Hospital Equipment Management (Migration Planning)

This repository currently contains the legacy Tkinter-based hospital equipment management application (`hospital_app.py`).

The long-term goal is to modernize the solution into a web-based platform built with FastAPI, PostgreSQL, and a React (Vite + TypeScript) frontend. A comprehensive migration plan describing the target architecture, feature set, DevOps workflow, and implementation roadmap is available at [`docs/web_app_migration_plan.md`](docs/web_app_migration_plan.md).

## Repository Layout

```
.
├── README.md
├── docs/
│   └── web_app_migration_plan.md
└── hospital_app.py  # legacy Tkinter + SQLite implementation
```

## Next Steps

- Review the migration plan to understand the desired end state and phased delivery approach.
- Use the plan as the blueprint for creating the new backend (`backend/`) and frontend (`frontend/`) services.
- Track progress against the acceptance criteria checklist defined in the plan.

## License

Specify the project license here.
