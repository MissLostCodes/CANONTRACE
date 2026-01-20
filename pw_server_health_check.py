import uvicorn
from fastapi import FastAPI
import httpx

PATHWAY_URL = "http://127.0.0.1:8080"

app = FastAPI(title="Pathway Health Server")


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Pathway vector server is up 🚀",
        "vector_port": 8080
    }


@app.get("/health")
def health_check():
    """
    Checks whether Pathway server on 8080 is reachable.
    """
    try:
        with httpx.Client(timeout=2.0) as client:
            response = client.get(PATHWAY_URL)
        return {
            "status": "healthy",
            "pathway_port": 8080,
            "reachable": True,
            "pathway_http_status": response.status_code
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "pathway_port": 8080,
            "reachable": False,
            "error": str(e)
        }
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8081,
        log_level="info",
    )