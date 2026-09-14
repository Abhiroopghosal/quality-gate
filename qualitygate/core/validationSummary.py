#rule result --> (aggregation engine) ---> Validation Summary(immutable)

#validation summary : counts(passed results, failed results, skipped results, errored results, critical) + quality score

from dataclasses import dataclass, field
from typing import Any
from qualitygate.core.result import RuleResult

@dataclass(frozen=True)
class ValidationSummary:
    """
    an immutable record which gives a holistic view of the whole data rather than view from a specific rule or target column perspective
    """
    rule_results : list[RuleResult]
    quality_score : float # on the basis of soft lane weighted score

    passed_rules : int #count when execution_status == Completed and validation_status == passed
    failed_rules : int #count when execution_status == Completed and Validation_status == Failed
    errored_rules : int # when execution_status == errored and validaiton_status == not_evaluated
    skipped_rules : int# when execution_status == skipped and validation_status == not evaluated

    critical_rules : int # count of the number of Critical Failures

    total_rules : int # len(RuleResult)

    # for auditing purposes
    dataset : str 
    batch_id : str
