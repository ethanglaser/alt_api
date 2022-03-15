#!/usr/bin/env python3
"""
run api
"""

from utils.config import PORT
from server import build_server
from misc.index import *

# needs to be initialized here to work with uwsgi in production
app = build_server()


def main() -> None:
    """
    run server

    default port is 8080
    """
    app.run(host='0.0.0.0', port=PORT)

import sys
if __name__ == '__main__':
    param1 = int(sys.argv[1])
    print(param1)
    hello = Hello()
    hello.get(param1)
    main()
