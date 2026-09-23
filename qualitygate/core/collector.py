from qualitygate.core.context import ValidationContext
from qualitygate.core.rule import ValidationRule
from qualitygate.core.result import RuleResult
from qualitygate.core.enums import ExecutionStatus, ValidationStatus

"""
Given a set of rule instances and context, the collector runs each rules validate, and gathers
the RuleResult(s) into a list and is downstreamed to the aggregator
"""

def collect(rules : list[ValidationRule], context : ValidationContext) -> list[RuleResult]:
    results = []

    for r in rules:
        try :
            result = r.validate(context)
        except Exception as e :
            result = RuleResult(
                rule_name = r.rule_name,
                rule_category = r.rule_category,
                target = r.target,
                execution_status = ExecutionStatus.ERRORED,
                validation_status = ValidationStatus.NOT_EVALUATED,
                severity= r.severity,
                weight = r.weight,
                evidence = f"Rule Execution failed : {e}",
                metrics = {},
                execution_time_ms= 0.0,
                risk = 0.0
            )
        results.append(result)
    return results