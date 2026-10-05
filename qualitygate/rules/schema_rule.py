from qualitygate.core.rule import ValidationRule
from qualitygate.core.context import ValidationContext
import time
from qualitygate.core.result import RuleResult
from qualitygate.core.enums import ValidationStatus, ExecutionStatus, Severity
from qualitygate.rules.registry import register

@register
class SchemaRule(ValidationRule):
    rule_name = "SchemaRule"
    rule_category = "STRUCTURE"
    execution_strategy = "METADATA"
    required_inputs = ["evidence"]

    def validate(self, context):
        started = time.perf_counter()

        #guard for evidence - None
        if context.evidence is None :
            elapsed_time_guard = (time.perf_counter() - started) * 1000
            return RuleResult(
                rule_name= self.rule_name,
                rule_category= self.rule_category,
                target = None,
                execution_status= ExecutionStatus.SKIPPED,
                execution_time_ms= elapsed_time_guard,
                validation_status= ValidationStatus.NOT_EVALUATED,
                severity= self.severity,
                weight= self.weight,
                evidence= "No evidence available — schema not evaluated",
                risk = 0.0                
            )

        #columns present
        missing_columns = context.evidence["missing_columns"]
        additional_columns = context.evidence["extra_columns"]


        if not missing_columns and not additional_columns:
            verdict = ValidationStatus.PASS
            risk = 0.0
            evidence = "Schema matches expected schema"
        else:
            verdict = ValidationStatus.FAIL
            risk = 1.0
            evidence = (f"Schema mismatch — missing: {missing_columns or 'none'}, "
                        f"extra: {additional_columns or 'none'}, ")


        elapsed_time = (time.perf_counter() - started) * 1000

        return RuleResult(
            rule_name= self.rule_name,
            rule_category= self.rule_category,
            target = self.target,
            execution_status= ExecutionStatus.COMPLETED,
            execution_time_ms= elapsed_time,
            validation_status= verdict,
            severity= self.severity,
            weight= self.weight,
            evidence= evidence,
            metrics= {
                "missing_columns" : list(missing_columns),
                "additional_columns" : list(additional_columns)
            },
            risk = risk

        )
        