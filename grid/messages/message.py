from uuid import uuid1, UUID


class Message:
    def __init__(self, id: UUID = None):
        """Base class for Message objects.

        Args:
            id (uuid1): original id of message
        """
        self.id = id if id else uuid1()

    @classmethod
    def deserialize(clss, data: dict):
        """To be implemented by child message class"""
        raise NotImplemented()

    def serialize(self):
        """To be implemented by child message class"""
        raise NotImplemented()

    def reduce(self, responses, node):
        """To be implemented by child message class"""
        raise NotImplemented()

    def from_tell(self, node, mailroom, env):
        """To be implemented by child message class"""
        # TODO: May want to rethink args. Envelope isn't
        #   needed all the time. Could be better way of allowing
        #   message logic to use it when it needs but not pass
        #   it down when it doesn't.
        raise NotImplementedError

    def from_ask(self, node, mailroom, env):
        """To be implemented by child message class"""
        raise NotImplementedError

    def from_response(self, node, mailroom, env):
        """To be implemented by child message class"""
        raise NotImplementedError

    def gettype(self):
        return self.__class__.__name__

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self):
        return id(self.id)

    def __repr__(self):
        clss_name = self.__class__.__name__
        attr_list = [f'{k}={v.__str__()}' for k,
                     v in self.__dict__.items() if not isinstance(v, UUID)]
        attr_str = ' '.join(attr_list)
        return f'<{clss_name} {attr_str}>'
