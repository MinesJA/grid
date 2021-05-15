body: {
    id: uuid,
    timestamp: float,
    envType: str,
    msgType: str,
    msg: {},
    returnId: uuid,
    reqId: uuid,
    masterReqId
}



## Terminology
1. Prime Mover - The first node to kick off a chain of message passing
1. Primary Message - The first call to a Node. Can be called from an IoT device, a user, etc. 
Primary Messages need to be call via the queue like any other message, even though they are not 
forwarded from another Node.
2. Secondary Message - Call coming from a another node
