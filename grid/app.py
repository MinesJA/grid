import uvicorn
from grid.server import create_app, parse_args

app = create_app()

if __name__ == "__main__":
    # TODO: WARNING:  ASGI app factory detected. Using it, but please consider setting the --factory flag explicitly.
    uvicorn.run("grid.app:app", host=parse_args().address,
                port=parse_args().port, log_level="info")