# ToDoList - Python OOP

A Python-based ToDo List application built with Object-Oriented Programming principles, following Agile and Incremental Development methodologies.

## 📢 Deprecation Notice

### CLI Interface Deprecation

The Command Line Interface (CLI) is now **deprecated** and scheduled for removal in the next major release.

#### This means:
- **The CLI is still functional** in the current version (v3.0)
- **No new features** will be added to the CLI
- **Bug fixes** for CLI will be limited
- **The CLI will be completely removed** in v4.0

## Features

### CLI
- List, create, edit and delete **projects**
- Add, edit, delete and change **task status** inside a project
- Auto-close DB tasks after thier daedline is passed

### API
- `/api/projects` → create/edit/list/delete projects
- `/api/tasks` → create/edit/list/delete tasks
- Interactive Swagger UI (`/docs`)

## Project Goals

- Practice Python OOP concepts
- Implement Agile development methodologies
- Learn and follow Python coding conventions
- Use Poetry for dependency management
- Prepare for future phases (persistent storage, Web API, automated testing)

## Architecture

The application follows a **layered architecture**:

- **Business Logic Layer**: Core application logic (project/task operations)
- **Data Access Layer**: In-memory data storage and retrieval
- **Presentation Layer**: CLI interface (prepared for future web interface)

## Used Technologies

- **Python 3.x** with OOP
- **Poetry** for dependency management
- **python-dotenv** for environment configuration
- **PEP8** coding standards

## Quick Start

### 1. Setup
```bash
# Clone and setup
git clone https://github.com/saniazzt/TodoList.git
cd TodoList

# Install dependencies with Poetry
poetry install

# Copy environment config
# And fill in the variables
cp .env.example .env
```

### 2. Run PostgreSQL using Docker Compose

```bash
docker compose down -v
docker compose up -d
```
### 3. Database Migration

```bash
poetry run alembic revision --autogenerate -m "init"
poetry run alembic upgrade head
```

### 4. Running main
```
poetry run python -m todolist.main
```
#### options:

  -h, --help   : show this help message and exit

  --menu       : Run CLI menu

  --schedule   : Run scheduler only
  
  --both       : Run CLI with background scheduler

  --api        : Create API app

  --host HOST

  --port PORT
