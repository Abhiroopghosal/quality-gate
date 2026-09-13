from qualitygate.core.rule import ValidationRule
from qualitygate.core.context import ValidationContext
import time
from qualitygate.core.result import RuleResult
from qualitygate.core.enums import ValidationStatus, ExecutionStatus, Severity


class SchemaRule(ValidationRule):
    rule_name = "SchemaRule"
    rule_category = "STRUCTURE"
    execution_strategy = "METADATA"
    required_inputs = ["evidence"]

    def validate(self, context):
        started = time.perf_counter()
        expected = self.params["expected_schema"]
        actual = context.evidence

        """
        in schema rule we have evidence and actual and we check for the column data type mismatches and cardinality issues
        actual = {
        "id" : "string", "name" : "string", "age": "int"
        }

        expected = {
        "id" : "int", "name" : "string", "age": "int"
        }
        """

        #columns present
        missing_columns = set(expected) - set(actual)
        additional_columns = set(actual) - set(expected)

        #data type
        type_mismatch = {}
        for column in expected.keys() & actual.keys():
            if expected[column] != actual[column]:
                type_mismatch[column] = {
                                    "expected" : expected[column],
                                    "actual" : actual[column] }       

        if not missing_columns and not additional_columns and not type_mismatch:
            verdict = ValidationStatus.PASS
            risk = 0.0
            evidence = "Schema matches expected schema"
        else:
            verdict = ValidationStatus.FAIL
            risk = 1.0
            evidence = (f"Schema mismatch — missing: {missing_columns or 'none'}, "
                        f"extra: {additional_columns or 'none'}, "
                        f"type mismatches: {list(type_mismatch) or 'none'}")


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
                "additional_columns" : list(additional_columns),
                "type_mismatch" : type_mismatch
            },
            risk = risk

        )
        