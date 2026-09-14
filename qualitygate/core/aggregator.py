from qualitygate.core.enums import ExecutionStatus, ValidationStatus, Severity
from qualitygate.core.validationSummary import ValidationSummary
from qualitygate.core.result import RuleResult

# rule_result1 = (rule_name = Null_Rule, rule_category = "COMPLETENESS", target = email, execution_status = ExecutionStatus.COMPLETED,
#                 execution_time_ms = 4.24ms ... and so on)
# rule_result2 = (rule_name = Duplicate_Rule, rule_category = "COMPLETENESS", target = id, execution_status = ExecutionStatus.COMPLETED,
#                 execution_time_ms = 2.24ms ... and so on)

# list(rule_result) = [rule_result1, rule_result2]

def compute_quality_score(results : list[RuleResult]) -> float:
    """
    Quality_Score = (max_weight - failed_weight)/max_weight * 100
    max_weight -> the ideal case scenario where all completed soft rules have passed so just sum(rule_weight)
    quality_score -> the deviation from the ideal state
    failed_weight should be graded on the basis of the deviation from the threshold. If the threshold = 3.1% and actual1 = 3.5% and actual2 = 4% then they should be
    weighed differently 
    Below threshold (passing) risk is intentionally NOT
    penalized here within a single batch a passing rule is fine. That
    below-threshold risk is retained on the RuleResult for History rules,
    which read risk trends across batches to detect drift toward threshold.

    Returns 100.0 when there are no completed soft rules to score.
    """
    max_weight = 0.0
    failed_weight = 0.0
    for r in results:
        if r.severity is Severity.SOFT and r.execution_status is ExecutionStatus.COMPLETED:
            max_weight += r.weight

            if r.validation_status is ValidationStatus.FAIL:
                failed_weight += r.weight * r.risk

    if max_weight ==  0:
        return 100.0
    quality_score = (max_weight - failed_weight)/ max_weight * 100
    return quality_score




def aggregate(rule_results : list[RuleResult], dataset : str, batch_id : str)-> ValidationSummary :
    passed_rules = 0
    failed_rules = 0
    errored_rules = 0
    skipped_rules = 0
    critical_rules = 0

    for r in rule_results:
        if r.execution_status is ExecutionStatus.COMPLETED and r.validation_status is ValidationStatus.PASS:
            passed_rules += 1
        elif r.execution_status is ExecutionStatus.COMPLETED and r.validation_status is ValidationStatus.FAIL:
            failed_rules += 1

            if r.severity is Severity.CRITICAL:
                critical_rules += 1

        elif r.execution_status is ExecutionStatus.ERRORED and r.validation_status is ValidationStatus.NOT_EVALUATED:
            errored_rules += 1
        elif r.execution_status is ExecutionStatus.SKIPPED and r.validation_status is ValidationStatus.NOT_EVALUATED:
            skipped_rules += 1

    total_rules = len(rule_results)

        
    quality_score = compute_quality_score(rule_results)

    return ValidationSummary(
        rule_results =rule_results,
        quality_score= quality_score,
        passed_rules= passed_rules,
        failed_rules= failed_rules,
        errored_rules= errored_rules,
        skipped_rules= skipped_rules,
        critical_rules= critical_rules,
        total_rules= total_rules,
        dataset= dataset,
        batch_id=batch_id
    )
