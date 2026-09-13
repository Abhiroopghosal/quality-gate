from pyspark.sql import functions as F
from qualitygate.core.context import ValidationContext
from qualitygate.core.enums  import Severity, ValidationStatus, ExecutionStatus
from qualitygate.core.rule import ValidationRule
from qualitygate.core.grading import grade_soft
from qualitygate.core.result import RuleResult
import time

class NullRule(ValidationRule):
    rule_name = "NullRule"
    rule_category = "COMPLETENESS"

    def validate(self, context):
        started = time.perf_counter()

        df = context.dataset


        total = df.count()
        null_count = df.filter(F.col(self.target).isNull()).count()

        null_rate = null_count / total

        if self.severity is Severity.CRITICAL:
            if null_count > 0:
                verdict = ValidationStatus.FAIL 
                risk = 1.0
                evidence = "null is not permitted"
            elif null_count == 0:
                verdict = ValidationStatus.PASS
                risk = 0.0
                evidence = "Everything in place"

        else :
            threshold = self.params["threshold"]
            kink = self.params["kink"]
            risk = grade_soft(null_rate, threshold=threshold, kink=kink)
            if null_rate > threshold:
                verdict = ValidationStatus.FAIL 
                evidence = (
                    f"Null rate {null_rate:.1%}"
                    f" exceeds threshold {threshold:.1%}"
                )
            else:
                verdict = ValidationStatus.PASS
                evidence = (
                    f"Null rate {null_rate:.1%} is within the threshold"
                )
            
        elapsed_time = (time.perf_counter() - started) * 1000
        return RuleResult(
            rule_name = self.rule_name,
            rule_category = self.rule_category,
            target = self.target,
            execution_status = ExecutionStatus.COMPLETED, 
            validation_status = verdict,
            severity= self.severity,
            weight = self.weight,
            evidence = evidence,
            metrics = {
                "null_count" : null_count, "null_rate" : null_rate, "total_rows": total 
            },
            execution_time_ms= elapsed_time,
            risk = risk 
        )