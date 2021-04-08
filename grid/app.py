import uvicorn
import sys
from grid.server import create_app, parse_args
from grid.models.node import NodeBuilder


APP_PATH = 'grid.app:app'
args = parse_args(sys.argv[1:])
node_builder = NodeBuilder(id=args.id, address=args.address,
                           port=args.port, pro=10, con=5)

app = create_app(node_builder)

if __name__ == "__main__":
    uvicorn.run(APP_PATH, host=args.address, port=args.port, log_level="info")
