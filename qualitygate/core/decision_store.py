from dataclasses import dataclass
from datetime import datetime

from qualitygate.core.enums import DecisionStatus

@dataclass(frozen=True)
class Decision:
    """
    decision object will give verdict on the basis of the Validation Summary
    """
    status :  DecisionStatus
    decision_reason : str
    quality_score : float
    decision_timestamp : datetime
    