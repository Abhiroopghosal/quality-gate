#reads the config file(the contract) and produces the rule objects

import yaml
from qualitygate.rules.registry import get_rule
from qualitygate.core.enums import Severity

def load_contract(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    rules = []

    for rule_config in config:
        rule_name = rule_config.pop("rule")
        severity = Severity[rule_config.pop("severity").upper()]
        target = rule_config.pop("target")
        weight = rule_config.pop("weight", 0.0)


        cls = get_rule(rule_name)

        rule = cls(
            target = target,
            severity = severity,
            weight = weight,
            **rule_config
        )

        rules.append(rule)

    return rules