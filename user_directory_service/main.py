import os
import sys

from src import create_app

# Instance configuration
if __name__ == "__main__":
    node_type = os.environ.get('NODE_TYPE', None)
    print(f'Node type: {node_type}')
    if node_type not in ('COORDINATOR', 'WORKER'):
        sys.exit(1)

    app = create_app(coordinator=(node_type == 'COORDINATOR'))
    app.run(host='0.0.0.0', port=8080)
