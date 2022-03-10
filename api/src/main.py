#!/usr/bin/env python3
"""
run api
"""

from utils.config import PORT
from server import build_server

# needs to be initialized here to work with uwsgi in production
app = build_server()


def main() -> None:
    """
    run server

    default port is 8080
    """
    app.run(host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
