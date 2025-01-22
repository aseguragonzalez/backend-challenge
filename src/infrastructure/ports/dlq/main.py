import logging

from src.infrastructure.ports.dlq.app import App
from src.infrastructure.ports.dlq.dependencies import configure


logging.basicConfig(level=logging.INFO)

app = configure(App(logger=logging.getLogger(__name__)))

if __name__ == "__main__":
    app.run()
