from abc import ABC, abstractmethod
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, **config):
        self.id = f"{self.__class__.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.status = "initialized"
        self.config = config
        self.last_update = datetime.now()
        self.error_count = 0
        self.max_errors = 3
        
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the agent with required setup"""
        pass
        
    @abstractmethod
    async def run(self) -> None:
        """Main execution loop for the agent"""
        pass
        
    @abstractmethod
    async def shutdown(self) -> None:
        """Clean shutdown of the agent"""
        pass
    
    async def health_check(self) -> Dict[str, Any]:
        """Check the health status of the agent"""
        return {
            "id": self.id,
            "status": self.status,
            "last_update": self.last_update,
            "error_count": self.error_count
        }
    
    async def handle_error(self, error: Exception) -> None:
        """Handle agent errors and update status"""
        self.error_count += 1
        logger.error(f"Agent {self.id} error: {str(error)}")
        
        if self.error_count >= self.max_errors:
            self.status = "error"
            logger.critical(f"Agent {self.id} exceeded maximum error count")
        
    def update_status(self, new_status: str) -> None:
        """Update the agent's status"""
        self.status = new_status
        self.last_update = datetime.now()
        logger.info(f"Agent {self.id} status updated to: {new_status}")
    
    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages/commands"""
        pass
        
    def get_config(self) -> Dict[str, Any]:
        """Get the agent's configuration"""
        return self.config