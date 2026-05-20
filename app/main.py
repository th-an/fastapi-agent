import logfire
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from agent.agent import create_agent
from agent.result_types import QueryResult
from app.config import get_settings
from app.database import connect_to_mongo, close_mongo_connection, get_database
from routers.api_v1 import router as api_v1_router

settings = get_settings()

if settings.LOGFIRE_TOKEN:
    logfire.configure(token=settings.LOGFIRE_TOKEN)
    logfire.instrument_pymongo()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

if settings.LOGFIRE_TOKEN:
    logfire.instrument_fastapi(app)

app.include_router(api_v1_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/agent/query", response_model=QueryResult)
async def agent_query(
    query: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Query the AI agent with database access."""
    agent = create_agent(db)
    result = await agent.run(query, deps=db)
    return result.output


@app.get("/agent/result-types")
async def list_result_types():
    """List available result types for agent responses."""
    return {
        "QueryResult": QueryResult.model_json_schema(),
    }
