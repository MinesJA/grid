import yaml


def parse():
    with open("grid_data.yml", 'r') as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)
