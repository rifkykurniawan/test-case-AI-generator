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
Copy `.env.example` to `.env` (inside the `backend/` directory) and customize the configuration:
```bash
cd backend
cp .env.example .env
```

#### Configuration Options in `.env`:
- `AI_PROVIDER`: Choose `"ollama"` to run the model locally, or `"gemini"` to use the Gemini Cloud API.
- `GEMINI_API_KEY`: Required if `AI_PROVIDER="gemini"`.
- `OLLAMA_BASE_URL`: Base URL of your local Ollama instance (defaults to `http://localhost:11434`).
- `MODEL_NAME`: The target model name (e.g., `qwen3:4b` for Ollama, or `gemini-2.0-flash` for Gemini).

### 2. Install Dependencies
Ensure you have a Python environment setup:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pip install pytest pytest-asyncio ruff
```

### 3. Start Development Server
Ensure your local Ollama server is running (e.g., via `ollama serve` or the desktop app) if using Ollama.

Start the FastAPI server from the `backend` directory:
```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the uvicorn server
uvicorn app.main:app --reload
```
Alternatively, from the project root directory, you can run:
```bash
./backend/.venv/bin/uvicorn app.main:app --reload --app-dir backend
```

Navigate to **[http://localhost:8000/docs](http://localhost:8000/docs)** in your browser to view the interactive Swagger OpenAPI documentation.

### 4. Running Tests & Linting
From the `backend` directory:
```bash
# Run unit tests
.venv/bin/pytest

# Run code formatting and lint verification
.venv/bin/ruff format .
.venv/bin/ruff check .
```

## Docker Container

Build and run in a production-ready containerized environment:
```bash
cd backend
docker build -t test-case-generator-backend .
docker run -p 8000:8000 --env-file .env test-case-generator-backend
```

