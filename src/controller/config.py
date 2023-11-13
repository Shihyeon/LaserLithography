import yaml

class Config():
    def __init__(self):
        with open(file="src\\config.yml", mode="r") as config_file:
            self.config = yaml.safe_load(config_file)