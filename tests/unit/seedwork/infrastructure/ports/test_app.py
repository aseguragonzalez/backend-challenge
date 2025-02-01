from unittest.mock import Mock

import pytest
from tests.unit.seedwork.infrastructure.ports.fakes import FakeApp, FakeService, FakeSettings


@pytest.mark.unit
def test_fake_app_should_allow_set_and_get_dependencies(faker):
    settings = FakeSettings(service_host=faker.word(), service_port=faker.pyint(), api_key=faker.word())
    fake_app = FakeApp()
    fake_app.register(lambda sp: sp.register_singleton(FakeSettings, lambda _: settings))

    fake_settings = fake_app.service_provider.get(FakeSettings)

    assert fake_settings.service_host == settings.service_host
    assert fake_settings.service_port == settings.service_port
    assert fake_settings.api_key == settings.api_key


@pytest.mark.unit
def test_service_executes_on_main_run():
    mock_service = Mock(FakeService)
    fake_app = FakeApp()
    fake_app.register(lambda sp: sp.register(FakeService, lambda _: mock_service))

    fake_app.run()

    mock_service.execute.assert_called_once()
