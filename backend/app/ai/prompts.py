def build_user_prompt(requirement: str) -> str:
    """Builds the user prompt containing the software requirement to analyze.

    Args:
        requirement: The user's input requirement.

    Returns:
        str: Formatted user prompt.
    """
    return f"Requirement:\n\n{requirement}"
