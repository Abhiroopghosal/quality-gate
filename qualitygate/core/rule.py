#different rules from individual logic gets subjected to this uniform frameowrk

from abc import ABC, abstractmethod
from .context import ValidationContext
from .enums import Severity
from .result import RuleResult

class ValidationRule(ABC):
    rule_name : str = "UnnamedRule"
    rule_category : str = "UNCATEGORISED"
    execution_strategy : str = "AGGREGATE"
    required_inputs : list[str] = ["dataset"]

    def __init__(self, target, severity, weight, **params):
        self.target = target
        self.severity = severity 
        self.weight = weight
        self.params = params 

    @abstractmethod
    def validate(self, context: ValidationContext) -> RuleResult:
        pass