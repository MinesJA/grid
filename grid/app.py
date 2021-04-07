import uvicorn
import sys
from grid.server import create_app, parse_args


APP_PATH = 'grid.app:app'
args = parse_args(sys.argv[1:])

app = create_app(args)

if __name__ == "__main__":
    uvicorn.run(APP_PATH, host=args.address, port=args.port, log_level="info")
