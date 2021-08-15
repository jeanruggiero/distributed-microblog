import os
import sys

from typing import List
from src import create_app

# Instance configuration
if __name__ == "__main__":
    node_type = os.environ.get('NODE_TYPE', None)
    if node_type not in ('COORDINATOR', 'WORKER'):
        sys.exit(1)
    print(node_type)

    app = create_app(coordinator=(node_type == 'COORDINATOR'))
    app.run(port=8080)
