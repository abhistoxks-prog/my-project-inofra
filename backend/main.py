import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.agent_manager import AgentManager
from api.routes import router, set_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    manager = AgentManager()
    set_manager(manager)
    manager.apply_config()
    asyncio.create_task(manager.run_all())
    manager.start_background_refresh()
    yield
    manager.stop_background_refresh()


app = FastAPI(
    title="WorldWatch AI",
    description="Multi-Agent AI Intelligence System",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "WorldWatch AI — Multi-Agent Intelligence System", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
