from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes.resource_client import ResourceClient


class ResourceService:
    def __init__(self, resource_client: ResourceClient) -> None:
        self._resource_client = resource_client

    def execute(self) -> None:
        if self._resource_client.is_open():
            self._resource_client.do_things()
