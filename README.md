# ToDoList - Python OOP

A Python-based ToDo List application built with Object-Oriented Programming principles, following Agile and Incremental Development methodologies.

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

```bash
# Clone and setup
git clone https://github.com/saniazzt/TodoList.git
cd TodoList

# Install dependencies with Poetry
poetry install

# Copy environment config
cp .env.example .env

# Run the application
poetry run python src/todolist/main.py
```

## Configuration

Create a .env file with the following variables:

```bash
MAX_NUMBER_OF_PROJECTS=50
MAX_NUMBER_OF_TASKS=1000
```
