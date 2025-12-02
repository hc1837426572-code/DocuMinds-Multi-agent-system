from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class BaseAgent(ABC):
    """Base classes for all intelligent agents"""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.created_at = datetime.now()
        self.interaction_chain = []
        
    def log_interaction(self, from_agent: str, to_agent: str, 
                       task: str, reasoning: str):
        """Record intelligent agent interaction logs"""
        interaction = {
            "timestamp": datetime.now(),
            "from": from_agent,
            "to": to_agent,
            "task": task,
            "reasoning": reasoning,
            "interaction_id": str(uuid.uuid4())
        }
        self.interaction_chain.append(interaction)
    
    @abstractmethod
    async def process(self, task_data: Dict[str, Any], 
                     context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Core methods for handling tasks"""
        pass
    
    def get_audit_trail(self) -> list:
        """Obtain audit trail"""
        return self.interaction_chain
