RULE_CLASSES = {}

def register(cls):
    RULE_CLASSES[cls.rule_name] = cls
    return cls

def get_rule(name):
    if name not in RULE_CLASSES:
        raise ValueError(f"Unknown rule: {name!r}")
    return RULE_CLASSES[name]