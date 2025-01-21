from uuid import UUID

from src.seedwork.domain.entities import AggregateRoot
from src.seedwork.domain.repositories import Repository
from src.seedwork.infrastructure.events.event import Event
from src.seedwork.infrastructure.events.events_publisher import EventsPublisher


class EventsInterceptor(Repository[AggregateRoot[UUID]]):
    def __init__(self, events_publisher: EventsPublisher, repository: Repository[AggregateRoot[UUID]]) -> None:
        self._repository = repository
        self._events_publisher = events_publisher

    def get(self, id: UUID) -> AggregateRoot[UUID]:
        return self._repository.get(id=id)

    def save(self, entity: AggregateRoot[UUID]) -> None:
        self._repository.save(entity)
        events = [Event.from_domain_event(event) for event in entity.events]
        self._events_publisher.publish(events=events)
        entity.clear_events()
        return None
