
class Command:

    def __init__(self, mailroom, node, env):
        self.mailroom = mailroom
        self.node = node
        self.env = env

    def add_action(self, action):
        self.actions.append(action)

    def execute(self):
        for action in self.actions:

    @staticmethod
    def build_command(clss, mailroom, node, env):
        pass


# def build_command