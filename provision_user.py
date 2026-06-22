import yaml

def load_role_rules(path="roles.yaml"):
    with open(path) as f:
        data = yaml.safe_load(f)
    return data["roles"]