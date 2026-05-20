from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.providers.anthropic import AnthropicProvider
from motor.motor_asyncio import AsyncIOMotorDatabase
from agent.result_types import QueryResult
from agent.tools import get_customer_info, validate_invoice, get_order_status
from app.config import get_settings

settings = get_settings()

SYSTEM_PROMPT = """You are a helpful customer service agent for a retail application.

You have access to tools that let you:
- Look up customer information by their customer ID
- Validate invoices and check their format
- Check order status and details

Be precise, professional, and helpful in all your responses.
Always confirm information before taking action on behalf of customers.
When you return a result, ensure it matches the required schema exactly.
"""

SYSTEM_PROMPT_CHAT = """You are a helpful customer service agent for a retail application.

You have access to tools that let you:
- Look up customer information by their customer ID
- Validate invoices and check their format
- Check order status and details

Be conversational and helpful. Respond with natural language text.
"""


def create_agent(db: AsyncIOMotorDatabase) -> Agent:
    """Create a configured Pydantic AI agent with database dependency injection.

    This agent uses structured output (QueryResult).
    """

    provider = AnthropicProvider(api_key=settings.ANTHROPIC_API_KEY)
    model = AnthropicModel("claude-sonnet-4-20250514", provider=provider)

    agent = Agent(
        model=model,
        output_type=QueryResult,
        system_prompt=SYSTEM_PROMPT,
        deps_type=AsyncIOMotorDatabase,
    )

    agent.tool(get_customer_info)
    agent.tool(validate_invoice)
    agent.tool(get_order_status)

    return agent


def create_chat_agent(db: AsyncIOMotorDatabase) -> Agent:
    """Create a streaming-capable chat agent.

    This agent returns plain text (not structured output) to enable streaming.
    """

    provider = AnthropicProvider(api_key=settings.ANTHROPIC_API_KEY)
    model = AnthropicModel("claude-sonnet-4-20250514", provider=provider)

    agent = Agent(
        model=model,
        system_prompt=SYSTEM_PROMPT_CHAT,
        deps_type=AsyncIOMotorDatabase,
    )

    agent.tool(get_customer_info)
    agent.tool(validate_invoice)
    agent.tool(get_order_status)

    return agent
