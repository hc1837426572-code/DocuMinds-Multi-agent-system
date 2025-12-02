from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta
import redis
import hashlib

class FederatedMemory:
    """Federal Memory System - Provides personalized memory views for different agents"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.memory_index = {}
        self.perspectives = {
            "extractor": ["data", "structure", "format"],
            "analyzer": ["insight", "pattern", "correlation"],
            "summarizer": ["narrative", "key_points", "action_items"],
            "validator": ["accuracy", "completeness", "consistency"]
        }
    
    def _generate_memory_key(self, fact: str, agent_type: str) -> str:
        """Generate memory key values"""
        content_hash = hashlib.md5(fact.encode()).hexdigest()
        return f"memory:{agent_type}:{content_hash}"
    
    def store(self, fact: str, metadata: Dict[str, Any], 
              perspectives: Optional[List[str]] = None):
        """Storing facts into the Federal Memory System"""
        if perspectives is None:
            perspectives = list(self.perspectives.keys())
        
        memory_data = {
            "fact": fact,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat(),
            "perspectives": perspectives
        }
        
        # Create an index for each perspective

        for agent_type in perspectives:
            key = self._generate_memory_key(fact, agent_type)
            agent_keywords = self.perspectives.get(agent_type, [])
            
            # Add perspective specific keywords

            indexed_data = memory_data.copy()
            indexed_data["agent_keywords"] = agent_keywords
            
            # Store to Redis

            self.redis.setex(
                key, 
                timedelta(days=30), 
                json.dumps(indexed_data)
            )
    
    def retrieve_for_agent(self, agent_type: str, query: str, 
                          limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve relevant memories for specific intelligent medical examinations"""
        pattern = f"memory:{agent_type}:*"
        relevant_memories = []
        
        # Scan relevant memories

        for key in self.redis.scan_iter(match=pattern):
            memory_data = json.loads(self.redis.get(key))
            
            # Simple relevance rating

            relevance_score = self._calculate_relevance(
                query, memory_data["fact"], agent_type
            )
            
            if relevance_score > 0.3:  # threshold
                memory_data["relevance_score"] = relevance_score
                relevant_memories.append(memory_data)
        
        # Sort by relevance

        relevant_memories.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return relevant_memories[:limit]
    
    def _calculate_relevance(self, query: str, fact: str, agent_type: str) -> float:
        """Calculate the correlation between queries and facts"""
        query_words = set(query.lower().split())
        fact_words = set(fact.lower().split())
        
        # Calculate word overlap

        overlap = len(query_words.intersection(fact_words))
        total_words = len(query_words.union(fact_words))
        
        base_score = overlap / total_words if total_words > 0 else 0
        
        # Adjust weights based on the type of intelligent agent

        agent_weights = {
            "extractor": 1.2,
            "analyzer": 1.0,
            "summarizer": 0.8,
            "validator": 1.1
        }
        
        return base_score * agent_weights.get(agent_type, 1.0)
