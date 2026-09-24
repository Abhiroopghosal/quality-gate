from pyspark.sql import functions as F
from qualitygate.core.rule import ValidationRule
from qualitygate.core.context import ValidationContext
from qualitygate.core.result import RuleResult
from qualitygate.core.enums import ExecutionStatus, ValidationStatus, Severity
import time
from qualitygate.core.grading import grade_soft

class DuplicateRule(ValidationRule):
    rule_name = "DuplicateRule"
    rule_category = "UNIQUENESS"
    execution_strategy = "GROUPBY"
    required_inputs = ["dataset"]

    def __init__(self, target, severity, weight, **params):
        super().__init__(target, severity, weight, **params)
        self.target = [target] if isinstance(target, str) else list(target)

    def validate(self, context):

        started = time.perf_counter()
        df = context.dataset
        total = df.count()

        if total == 0:
            elapsed_time = (time.perf_counter() - started) * 1000
            return RuleResult(
                rule_name= self.rule_name,
                rule_category= self.rule_category,
                target= "+".join(self.target),
                execution_status= ExecutionStatus.COMPLETED,
                validation_status=ValidationStatus.NOT_EVALUATED,
                severity=self.severity,
                weight= self.weight,
                evidence="Empty Batch- Nothing to evaluate",
                metrics={"duplicate_count": 0, "duplicate_percentage" : 0, "total_rows" : 0},
                execution_time_ms= elapsed_time,
                risk= 0.0
            )

        """
        duplicate count as the count of excess rows after the first occurence. 
        """
        duplicate_count = total - df.select(*self.target).distinct().count()
        duplicate_rate = duplicate_count/total

        if self.severity is Severity.CRITICAL:
            if duplicate_count > 0 :
                verdict = ValidationStatus.FAIL
                risk = 1.0
                evidence = "Duplicates not permitted"
            else:
                verdict = ValidationStatus.PASS
                risk = 0.0
                evidence = "No Duplicates found"
        else:
            threshold = self.params["threshold"]
            kink = self.params["kink"]

            risk = grade_soft(duplicate_rate, threshold=threshold, kink=kink)

            if duplicate_rate > threshold:
                verdict = ValidationStatus.FAIL
                evidence = f"Duplicate Rate {duplicate_rate:.1%} exceeds {threshold:.1%}"
            else:
                verdict = ValidationStatus.PASS
                evidence = f"Duplciate Rate: {duplicate_rate:.1%} within the range of {threshold:.1%}"                


        elapsed_time = (time.perf_counter() - started) * 1000

        return RuleResult(
            rule_name= self.rule_name,
            rule_category=self.rule_category,
            target= "+".join(self.target),
            execution_status= ExecutionStatus.COMPLETED,
            validation_status= verdict,
            severity= self.severity,
            weight= self.weight,
            evidence= evidence, 
            metrics= {
                "duplicate_count" : duplicate_count, "duplicate_percentage" : duplicate_rate, "total_rows" : total
            },
            execution_time_ms= elapsed_time,
            risk=risk
            
        )