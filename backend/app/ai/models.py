# AI Domain Models (could extend schema definitions or hold provider-specific model metadata)
from app.schemas.response import GenerateResponse

# Use schema responses as domain models for simplicity and type safety
AIGeneratedOutput = GenerateResponse
