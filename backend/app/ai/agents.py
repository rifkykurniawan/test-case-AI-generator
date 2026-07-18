import os

from loguru import logger

from app.core.exceptions import AppError


def load_agents_markdown() -> str:
    """Finds and loads the AGENTS.md (or agents.md) file from the workspace root.

    Returns:
        str: Contents of the agents.md file.

    Raises:
        AppError: If the file cannot be found or read.
    """
    # Start looking from the current directory and traverse upwards
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Try different possible locations
    search_paths = [
        # Relative to this file (3 directories up)
        os.path.abspath(os.path.join(current_dir, "..", "..", "..")),
        # Cwd
        os.getcwd(),
    ]

    for path in search_paths:
        for filename in ["agents.md", "AGENTS.md"]:
            candidate = os.path.join(path, filename)
            if os.path.isfile(candidate):
                try:
                    with open(candidate, encoding="utf-8") as f:
                        content = f.read()
                        logger.info(
                            "Successfully loaded agent system prompt from: {}",
                            candidate,
                        )
                        return content
                except Exception as e:
                    logger.error(
                        "Failed to read agent prompt file from {}: {}", candidate, e
                    )
                    raise AppError(f"Failed to read agent prompt file: {e}")

    # Default fall-back check if parent of backend exists
    logger.error(
        "Could not find agents.md or AGENTS.md in search paths: {}", search_paths
    )
    raise AppError("agents.md system prompt file not found in workspace.")
