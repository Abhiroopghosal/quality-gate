from qualitygate.core.rule import ValidationRule
from qualitygate.core.context import ValidationContext
import time

class SchemaRule(ValidationRule):
    rule_name = "SchemaRule"
    rule_category = "STRUCTURE"
    execution_strategy = "META-DATA"
    required_inputs = [""]