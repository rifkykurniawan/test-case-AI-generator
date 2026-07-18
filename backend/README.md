# Test Case AI Generator Backend (Phase 1)

This project provides the backend foundation for an AI-powered Test Case Generator that translates software requirements into structured test cases and edge cases.

## Technology Stack

- **Python**: 3.13+
- **Framework**: FastAPI
- **Validation**: Pydantic v2
- **Excel Export**: openpyxl
- **Logging**: Loguru
- **Linting & Formatting**: Ruff
- **Testing**: Pytest

## Project Structure

```text
backend/
├── app/
│   ├── ai/               # Prompt and AI provider logic
│   │   ├── providers/    # Extensible provider implementations (Gemini, OpenAI, etc.)
│   │   └── ...
│   ├── api/              # Route handlers (generate, export, health)
│   ├── core/             # Configuration, logging, exception management, and DI dependencies
│   ├── schemas/          # Input/output validation models
│   ├── services/         # Business logic (AI orchestration, Excel export generation)
│   ├── utils/            # Utility helpers
│   └── main.py           # FastAPI Application entrypoint
├── tests/                # Endpoint validation tests (pytest)
├── pyproject.toml        # Ruff, Pytest, and project metadata
└── Dockerfile            # Multi-stage container setup
```

## Running the Application

### 1. Setup Environment
Copy `.env.example` to `.env` and fill in configuration settings:
```bash
cp .env.example .env
```

### 2. Install Dependencies
Ensure you have a Python environment setup:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pip install pytest pytest-asyncio ruff
```

### 3. Start Development Server
```bash
uvicorn app.main:app --reload
```
Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to view the interactive Swagger OpenAPI documentation.

### 4. Running Tests & Linting
Run unit tests:
```bash
pytest
```

Run code formatting and lint verification:
```bash
ruff format .
ruff check .
```

## Docker Container

Build and run in production-ready containerized environment:
```bash
docker build -t test-case-generator-backend .
docker run -p 8000:8000 --env-file .env test-case-generator-backend
```
