import logging
from fastapi import FastAPI
from src.core.master_agent import MasterAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Master Agent API")
master_agent = MasterAgent()

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Initializing Master Agent system...")
        await master_agent.initialize()
        logger.info("Master Agent system initialized successfully")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/agents")
async def list_agents():
    return await master_agent.list_agents()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
