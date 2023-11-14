import yaml

class Config():
    def __init__(self):
        try:
            with open(file="src\\config.yml", mode="r") as config_file:
                self.configuration = yaml.safe_load(config_file)
        except FileNotFoundError:
            print("File not found or path incorrect.")
            self.configuration = {}
