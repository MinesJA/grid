  async def add_sibling(self, env):
        """Adds a sibling NodeProxy to siblings. Then sends
        response message AddSibling with it's own info to maintain
        a bidirectional graph. Then sends a request to update
        the grids net output.

        Args:
            env (Envelope): envelope with add sibling details
        """

        sibling = NodeProxy(env.msg.sibling_id,
                            env.msg.sibling_name,
                            env.msg.sibling_address)

        if isinstance(env, Tell) and sibling.id not in self.siblings:
            await self.mailroom.ask(msg=AddSibling.with_node(self),
                                    sender=self,
                                    recipients=[sibling])

        elif isinstance(env, Ask) and sibling.id not in self.siblings:
            self.siblings.update({sibling.id: sibling})
            await self.mailroom.respond(ask=env,
                                        recipient=sibling,
                                        msg=AddSibling.with_node(self))

        elif isinstance(env, Response) and sibling.id not in self.siblings:
            self.siblings.update({sibling.id: sibling})
            self.mailroom.close_req(resp=env)

            await self.sync_grid(Tell.from(self, SyncGrid()))