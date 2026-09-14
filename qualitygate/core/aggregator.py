from qualitygate.core.enums import ExecutionStatus, ValidationStatus, Severity
from qualitygate.core.validationSummary import ValidationSummary
from qualitygate.core.result import RuleResult

# rule_result1 = (rule_name = Null_Rule, rule_category = "COMPLETENESS", target = email, execution_status = ExecutionStatus.COMPLETED,
#                 execution_time_ms = 4.24ms ... and so on)
# rule_result2 = (rule_name = Duplicate_Rule, rule_category = "COMPLETENESS", target = id, execution_status = ExecutionStatus.COMPLETED,
#                 execution_time_ms = 2.24ms ... and so on)

# list(rule_result) = [rule_result1, rule_result2]

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

        
    quality_score = 0.0

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
