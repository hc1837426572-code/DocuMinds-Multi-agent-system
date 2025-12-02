from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Optional
import json
import asyncio
from pydantic import BaseModel

from src.agents.router_agent import RouterAgent
from src.agents.orchestrator_agent import OrchestratorAgent
from src.memory.federated_memory import FederatedMemory
import redis

app = FastAPI(title="DocuMinds", version="1.0.0")

redis_client = redis.Redis(host='localhost', port=6379, db=0)
federated_memory = FederatedMemory(redis_client)
router_agent = RouterAgent()
orchestrator_agent = OrchestratorAgent(federated_memory)

class DocumentRequest(BaseModel):
    content: str
    document_type: str
    metadata: Optional[dict] = {}
    requires_compliance_check: bool = False

@app.post("/api/v1/process-document")
async def process_document(request: DocumentRequest):
    try:
        document_data = {
            "document": {
                "type": request.document_type,
                "content": request.content,
                "metadata": request.metadata,
                "requires_compliance_check": request.requires_compliance_check
            }
        }
        
        routing_result = await router_agent.process(document_data)
        
        workflow_plan = await orchestrator_agent.create_workflow_plan(
            routing_result, 
            document_data["document"]
        )
        
        final_result = await orchestrator_agent.execute_workflow(
            workflow_plan,
            document_data["document"]
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "routing_decision": routing_result,
                "workflow_plan": workflow_plan,
                "final_output": final_result
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "service": "documinds"}

@app.get("/api/v1/agent/{agent_type}/audit")
async def get_agent_audit(agent_type: str):
    try:
        if agent_type == "router":
            audit_trail = router_agent.get_audit_trail()
        elif agent_type == "orchestrator":
            audit_trail = orchestrator_agent.get_audit_trail()
        else:
            audit_trail = []
        
        return {
            "agent_type": agent_type,
            "audit_trail": audit_trail,
            "total_interactions": len(audit_trail)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
