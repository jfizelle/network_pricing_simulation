import yaml
def load_config(path):
    """Load YAML configuration file."""
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
    return config

# this file contains a function that opens a YAML file and loads the content into python