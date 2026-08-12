#  NullRule + email
#           ↓
#       RuleResult

# dataclass allows us to  create classes which hold data with __init__()
from dataclasses import dataclass, field
from typing import Any

#importing from the current package
from .enums import ExecutionStatus, ValidationStatus, Severity, SkipReason

#python genreates the constructor and other useful methods
#once the object is created the attributes can't be changed
# RuleReult by nature is an immutable snapshot
@dataclass(frozen=True) 
class RuleResult:
    """An immutable record of ONE rule evaluated against ONE target.

    NullRule over three columns produces three RuleResults, not one.
    The resolved configuration (severity, weight) is baked in so that an
    audit can reconstruct the verdict without re-reading the contract.
    """

    # --Identity--
    rule_name : str
    rule_category : str
    target : str | None = None # the thing being evaluated. None is necessary because soem rules are dataset-level rather than columnar

    #--Execution--
    execution_status : ExecutionStatus = ExecutionStatus.COMPLETED #default state 
    execution_time_ms : float | None = None   # records how long execution took in milliseconds

    #--Validation--
    validation_status : ValidationStatus = ValidationStatus.NOT_EVALUATED

    # --- Applied configuration (snapshot, not a live reference) ---
    severity : Severity | None = None
    weight : float = 0.0 

    #--diagnostics--

    evidence : str | None = None # a human readable explanation 

    # structured diagnostic information 
    # Result A -> its own {}, Result B -> its own {}, Result C -> another new {}
    metrics : dict[str, Any] = field(default_factory=dict) # field() is used so that when a new RuleResult is created without metrics, create a fresh empty dict for that object

    samples : list[Any] = field(default_factory=list) # field() ensures each RuleResult gets its own list

    #if a rule is skipped why? 
    skip_reason : SkipReason | None = None 
    dependency : str | None = None 

    #if the rule execution crashes
    error_message : str | None = None 



    # --- Graded contribution (soft lane only) ---
    # the soft lane's graded output, 0.0–1.0, from piecewise curve. 0.0 = clean, 1.0 = maximally bad
    risk : float | None = None  


    def __post_init__(self):
        #first invariant risk. risk must be between 0 and 1
        if self.risk is not None and not 0.0 <= self.risk <= 1.0:
            raise ValueError(f"risk ∈ [0.0, 1.0], got {self.risk}")

        #E second invariant : if execution did not complete, there cannot be validation verdict
        if self.execution_status is not ExecutionStatus.COMPLETED and self.validation_status is not ValidationStatus.NOT_EVALUATED:
            raise ValueError(f"{self.rule_name} : validation_status must be NOT_EVALUATED"
                             f"when execution_status is {self.execution_status.value}")







#                   RuleResult
#                   │
#                   ├── Identity
#                   │   ├── rule_name
#                   │   ├── rule_category
#                   │   └── target
#                   │
#                   ├── Execution
#                   │   ├── execution_status
#                   │   └── execution_time_ms
#                   │
#                   ├── Validation
#                   │   └── validation_status
#                   │
#                   ├── Applied configuration
#                   │   ├── severity
#                   │   └── weight
#                   │
#                   ├── Diagnostics
#                   │   ├── evidence
#                   │   ├── metrics
#                   │   ├── samples
#                   │   ├── skip_reason
#                   │   ├── dependency
#                   │   └── error_message
#                   │
#                   └── Scoring
#                       └── risk