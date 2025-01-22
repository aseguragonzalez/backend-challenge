import logging

from src.infrastructure.ports.subscriber.app import App
from src.infrastructure.ports.subscriber.dependencies import configure


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = configure(App(logger=logger))
app.register(lambda sp: sp.register_singleton(logging.Logger, lambda _: logger))

if __name__ == "__main__":
    app.run()
