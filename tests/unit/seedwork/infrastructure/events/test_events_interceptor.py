from unittest.mock import Mock
from uuid import UUID

import pytest

from src.seedwork.domain.entities import AggregateRoot
from src.seedwork.domain.repositories.repository import Repository
from src.seedwork.infrastructure.events import EventsInterceptor, EventsPublisher


@pytest.mark.unit
def test_get_should_call_repository_get_method(faker):
    events_publisher = Mock(EventsPublisher)
    aggregate_root = Mock(AggregateRoot)
    repository = Mock(Repository[AggregateRoot[UUID], UUID])
    repository.get.return_value = aggregate_root
    events_interceptor = EventsInterceptor(events_publisher=events_publisher, repository=repository)
    id = faker.uuid4()

    aggregate_root_founded = events_interceptor.get(id)

    repository.get.assert_called_once_with(id=id)
    assert aggregate_root_founded == aggregate_root


@pytest.mark.unit
def test_get_should_call_repository_save_and_publish_events():
    events_publisher = Mock(EventsPublisher)
    aggregate_root = Mock(AggregateRoot)
    aggregate_root.events = []
    repository = Mock(Repository[AggregateRoot[UUID], UUID])
    repository.save.return_value = None
    events_interceptor = EventsInterceptor(events_publisher=events_publisher, repository=repository)

    events_interceptor.save(aggregate_root)

    repository.save.assert_called_once_with(aggregate_root)
    assert aggregate_root.clear_events.call_count == 1
    assert events_publisher.publish.call_count == 1
