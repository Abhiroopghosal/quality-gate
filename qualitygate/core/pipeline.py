#pipeline.py automates collector -> aggregator engine -> decision engine

from qualitygate.core.rule import ValidationRule
from qualitygate.core.context import ValidationContext
from qualitygate.core.decision_store import Decision
from qualitygate.core.validationSummary import ValidationSummary
from qualitygate.core.collector import collect
from qualitygate.core.aggregator import aggregate
from qualitygate.core.decision import decide

def run(rules: list[ValidationRule], context: ValidationContext, dataset: str, batch_id : str, threshold = 70.0) -> tuple[Decision, ValidationSummary]:
    results = collect(rules, context)
    summary = aggregate(results, dataset, batch_id)
    decision = decide(summary, threshold)

    return decision, summary
