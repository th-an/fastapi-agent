from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from pydantic_ai.agent import Agent as PydanticAgent
from motor.motor_asyncio import AsyncIOMotorDatabase
from agent.result_types import DocumentProcessingResult
from app.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are a document processing agent specialized in analyzing invoices and receipts.

Your task is to:
1. Analyze the uploaded document image or PDF
2. Extract relevant information (invoice number, date, amount, vendor, line items)
3. Determine if this is a valid invoice or receipt
4. Return structured data about the document

Be precise and only extract information you're confident about. If the document is unclear, indicate that in your response.
"""


def create_document_agent(db: AsyncIOMotorDatabase) -> PydanticAgent:
    """Create a configured document processing agent."""

    provider = AnthropicProvider(api_key=settings.ANTHROPIC_API_KEY)
    model = AnthropicModel("claude-sonnet-4-20250514", provider=provider)

    agent = PydanticAgent(
        model=model,
        output_type=DocumentProcessingResult,
        system_prompt=SYSTEM_PROMPT,
        deps_type=AsyncIOMotorDatabase,
    )

    return agent
