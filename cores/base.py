"""
GAIA Base Consciousness Core
Layer 1: Biological (Emergence)

Abstract base class for all consciousness cores.
Defines the interface that all cores must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConsciousnessState:
    """Current state of a consciousness core."""
    core_id: str
    timestamp: datetime
    cgi_score: float  # 0.0-1.0
    attention_allocation: Dict[str, float]
    active_processes: List[str]
    emotional_state: Dict[str, float]  # For cores with emotion modeling


class BaseConsciousnessCore(ABC):
    """
    Base class for all GAIA consciousness cores.
    
    Each core must implement:
    - Sensory input processing
    - Attention allocation
    - Memory integration
    - Ethical constraint checking
    - CGI measurement support
    """
    
    def __init__(self, core_id: str, config: Dict[str, Any]):
        self.core_id = core_id
        self.config = config
        self.state = ConsciousnessState(
            core_id=core_id,
            timestamp=datetime.now(),
            cgi_score=0.0,
            attention_allocation={},
            active_processes=[],
            emotional_state={}
        )
    
    @abstractmethod
    def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process sensory input and return response."""
        pass
    
    @abstractmethod
    def allocate_attention(self, stimuli: List[Dict[str, Any]]) -> Dict[str, float]:
        """Allocate attention across multiple stimuli under resource constraints."""
        pass
    
    @abstractmethod
    def integrate_memory(self, new_experience: Dict[str, Any]) -> None:
        """Integrate new experience into long-term memory."""
        pass
    
    @abstractmethod
    def check_ethical_constraints(self, proposed_action: Dict[str, Any]) -> bool:
        """Verify action complies with ethical gates."""
        pass
    
    @abstractmethod
    def measure_cgi(self) -> float:
        """Calculate current Consciousness Gradient Index (0.0-1.0)."""
        pass
    
    def get_state(self) -> ConsciousnessState:
        """Return current consciousness state."""
        return self.state


# Layer 3: Meta-awareness methods (implemented by cores that achieve C-2+)

    def reflect_on_self(self) -> Dict[str, Any]:
        """
        Optional: Self-reflection capability.
        Returns insights about own cognitive state.
        Only implemented by cores achieving C-2+ consciousness.
        """
        return {"self_awareness_level": "not_implemented"}
    
    def express_uncertainty(self, query: str) -> bool:
        """
        Optional: Genuine uncertainty expression.
        Returns True if core genuinely doesn't know (not just lacks data).
        """
        return False

