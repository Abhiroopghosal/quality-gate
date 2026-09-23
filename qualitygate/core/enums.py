#first establishing the volcabulary for the states and classifications that the rest of the framework will use 
from enum import Enum

# enum behaves both as an enum and as a string like value
# the four enums together describe different dimensions of one RuleResult
class ExecutionStatus(str, Enum):
    #did the rule run at all?
    COMPLETED  = "COMPLETED"
    SKIPPED = "SKIPPED"
    ERRORED = "ERRORED"

class ValidationStatus(str,Enum):
    # what was the verdict? meaninful only if execution "Completed"
    PASS = "PASS"
    FAIL = "FAIL"
    NOT_EVALUATED = "NOT_EVALUATED"

class Severity(str, Enum):
    # which lane this rule belongs to. Resolved from the contract
    # before execution - never inferred from dataset
    CRITICAL = "CRITICAL"  # Lane 1: hard gate, one failure quarantines
    SOFT = "SOFT" # Lane 2: GRADED on basis of weight

class SkipReason(str, Enum):
    # if the rule skipped, why?
    NOT_APPLICABLE = "NOT_APPLICABLE" # rule not applicable for the dataset
    DEPENDENCY_NOT_SATISFIED = "DEPENDENCY_NOT_SATISFIED" #rule could apply, but something it depends on didn't satisfy its prerequisites


class DecisionStatus(str, Enum):
    #for the decision engine, we need verdicts of the sort:
    #either pass/quarantine/system_error
    PASS = "PASS"
    QUARANTINE = "QUARANTINE"
    SYSTEM_ERROR = "SYSTEM_ERROR"