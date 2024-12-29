import pytest
from tests.unit.seedwork.infrastructure.ports.dependency_injection.fakes import (
    AbstractService,
    CircularDependency,
    ConcreteService,
    CustomService,
    EnvironmentVariables,
    ExternalService,
    NestedService,
    ResourceClient,
    ResourceService,
    Service,
    ServiceDecorator,
    ThirdPartyService,
    ThirdPartySettings,
)

from src.seedwork.infrastructure.ports.dependency_injection import BasicServiceProvider, ServiceProvider


def test_get_service_should_resolve_concrete_component():
    service_provider = BasicServiceProvider()
    service_provider.register(AbstractService, ConcreteService)

    concrete_service = service_provider.get(AbstractService)

    assert isinstance(concrete_service, AbstractService)
    assert isinstance(concrete_service, ConcreteService)
    assert concrete_service.hello_world() is None
    assert concrete_service.id() is not None


def test_get_service_should_retrieve_new_instance_of_type_rule():
    service_provider = BasicServiceProvider()
    service_provider.register(ConcreteService, ConcreteService)

    first_service = service_provider.get(ConcreteService)
    second_service = service_provider.get(ConcreteService)

    assert isinstance(first_service, ConcreteService)
    assert isinstance(second_service, ConcreteService)
    assert first_service != second_service


def test_get_service_should_retrieve_new_instance_of_type_rule_function():
    service_provider = BasicServiceProvider()
    service_provider.register(ConcreteService, lambda service_provider: ConcreteService())

    first_service = service_provider.get(ConcreteService)
    second_service = service_provider.get(ConcreteService)

    assert isinstance(first_service, ConcreteService)
    assert isinstance(second_service, ConcreteService)
    assert first_service != second_service


def test_get_service_should_retrieve_singleton_of_type_rule():
    service_provider = BasicServiceProvider()
    service_provider.register_singleton(ConcreteService, ConcreteService)

    first_service = service_provider.get(ConcreteService)
    second_service = service_provider.get(ConcreteService)

    assert isinstance(first_service, ConcreteService)
    assert isinstance(second_service, ConcreteService)
    assert second_service == first_service


def test_get_service_should_retrive_singleton_of_concrete_component():
    service_provider = BasicServiceProvider()
    service_provider.register_singleton(AbstractService, ConcreteService)

    concrete_service_a = service_provider.get(AbstractService)
    concrete_service_b = service_provider.get(AbstractService)

    assert isinstance(concrete_service_a, AbstractService)
    assert isinstance(concrete_service_b, AbstractService)
    assert concrete_service_a.id() == concrete_service_b.id()


def test_get_service_should_retrive_new_instance_of_nested_service():
    def third_party_settings(sp: ServiceProvider) -> ThirdPartySettings:
        environment_variables = sp.get(EnvironmentVariables)
        return ThirdPartySettings(
            api_key=environment_variables.api_key, host=environment_variables.host, port=environment_variables.port
        )

    service_provider = BasicServiceProvider()
    service_provider.register(EnvironmentVariables, lambda sp: EnvironmentVariables())
    service_provider.register(AbstractService, ConcreteService)
    service_provider.register(AbstractService, lambda sp: ConcreteService())
    service_provider.register(NestedService, NestedService)
    service_provider.register(ExternalService, ThirdPartyService)
    service_provider.register(ThirdPartySettings, third_party_settings)

    nested_service = service_provider.get(NestedService)

    assert isinstance(nested_service, NestedService)
    assert isinstance(nested_service.concrete_service, ConcreteService)
    assert isinstance(nested_service.concrete_service, AbstractService)
    assert isinstance(nested_service.external_service, ExternalService)


def test_get_service_should_fails_when_detect_circular_dependency():
    service_provider = BasicServiceProvider()
    service_provider.register(CircularDependency, CircularDependency)

    with pytest.raises(RuntimeError) as exc_info:
        service_provider.get(CircularDependency)

    assert f"Max recursion level reached reaching: {CircularDependency}" in str(exc_info.value)


def test_get_service_should_retrieve_decorated_instance_of_abstract_component():
    sp = BasicServiceProvider()
    sp.register(CustomService, CustomService)
    sp.register(Service, ServiceDecorator)
    decorated_service = sp.get(Service)

    assert isinstance(decorated_service, Service)
    assert isinstance(decorated_service, ServiceDecorator)
    assert not isinstance(decorated_service, CustomService)
    assert isinstance(decorated_service._service, CustomService)
    assert decorated_service.execute() is None


def test_get_service_should_retrieve_a_context_managed_singleton():
    client = None
    with BasicServiceProvider() as sp:
        sp.register_context_managed_singleton(ResourceClient, ResourceClient)
        sp.register_singleton(ResourceService, ResourceService)
        resource_service = sp.get(ResourceService)

        resource_service.execute()

        client = sp.get(ResourceClient)
        assert client.is_open() is True

    assert client.is_open() is False
