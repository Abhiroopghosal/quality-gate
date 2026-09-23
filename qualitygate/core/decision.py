from qualitygate.core.decision_store import Decision
from qualitygate.core.enums import DecisionStatus
from qualitygate.core.validationSummary import ValidationSummary
from datetime import datetime

def decide(summary : ValidationSummary, threshold = 70.0) -> Decision:
    if summary.errored_rules > 0:
        return Decision(
            status= DecisionStatus.SYSTEM_ERROR,
            decision_reason= f"{summary.errored_rules} rule(s) errored — batch could not be fully assessed",
            quality_score= summary.quality_score,
            decision_timestamp=datetime.now()
        )
    elif summary.critical_rules > 0:
        return Decision(
            status =  DecisionStatus.QUARANTINE,
            decision_reason = f"{summary.critical_rules} critical failures and hence they are quarantined",
            quality_score = summary.quality_score,
            decision_timestamp = datetime.now(),
        )
    elif summary.quality_score >= threshold:
        return Decision(
            status = DecisionStatus.PASS,
            decision_reason = f"quality score {summary.quality_score} meets threshold {threshold} — passed",
            quality_score = summary.quality_score,
            decision_timestamp = datetime.now()
        )
    else:
        return Decision(
            status =  DecisionStatus.QUARANTINE,
            decision_reason = f"quality score {summary.quality_score} below threshold {threshold} — quarantined",
            quality_score = summary.quality_score,
            decision_timestamp = datetime.now()
        )