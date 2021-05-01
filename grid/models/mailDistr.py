from collections import namedtuple


ForwardId = namedtuple('ForwardID', ['req_id', 'env_id'])


class MailDistr:

    def __init__(self, reply_to_id):
        """ For managing messages that have not been addressed
        yet.

        to_respond are messages that need to be sent back
        to some Node awaiting a reply.
            {req_id: Envelope<>}

        awaiting_response are messages that need a response from
        a Node which was sent a message.
            {(req_id, env_id): Envelope<>}
            forward_id (req_id, env_id)

        Args:
            reply_to_id ([type]): [description]
        """
       
        self.reply_to_id = reply_to_id
        self.awaiting_responses = {}
        self.responded = {}

    def get_awaiting(self, req_id, env_id):
        return self.awaiting_responses.get(ForwardId(req_id, env_id))

    def update_awaiting(self, req_id, ask):
        self.awaiting_response.update({req_id, ask})

    def close_awaiting(self, req_id, response):
        self.awaiting_response.pop(req_id)
        self.responded.update({req_id, response})

    def is_completed(self):
        return not self.awaiting_responses
