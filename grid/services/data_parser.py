import yaml


def parse():
    with open("grid/grid_data.yml", 'r') as stream:
        try:
            x = yaml.safe_load(stream)
            return x
        except yaml.YAMLError as exc:
            print(exc)
