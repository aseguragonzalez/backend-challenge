from uuid import UUID

import pytest

from src.domain.entities import AssistanceRequest
from src.domain.exceptions import AssistanceRequestNotFoundError
from src.domain.value_objects import Status, Topic
from src.infrastructure.adapters.repositories import MongoDbAssistancesRepository


def test_save_should_store_an_assistant(faker, db_collection):
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        description=faker.sentence(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
    )
    id = str(assistance_request.id)
    repository = MongoDbAssistancesRepository(db_collection=db_collection)

    repository.save(entity=assistance_request)

    expected_assistance_request = db_collection.find_one({"_id": id})
    assert expected_assistance_request["_id"] == id
    assert expected_assistance_request["description"] == assistance_request.description
    assert expected_assistance_request["topic"] == assistance_request.topic.value
    assert expected_assistance_request["status"] == assistance_request.status.value


def test_save_should_update_an_assistance_request(faker, db_collection):
    assistance_request = AssistanceRequest.new(
        id=UUID(faker.uuid4()),
        description=faker.sentence(),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
    )
    db_collection.insert_one(
        {
            "_id": str(assistance_request.id),
            "topic": assistance_request.topic.value,
            "description": assistance_request.description,
            "status": assistance_request.status.value,
        }
    )
    repository = MongoDbAssistancesRepository(db_collection=db_collection)

    assistance_request.fail()
    repository.save(entity=assistance_request)

    expected_assistance_request = db_collection.find_one({"_id": str(assistance_request.id)})
    assert expected_assistance_request["_id"] == str(assistance_request.id)
    assert expected_assistance_request["description"] == assistance_request.description
    assert expected_assistance_request["topic"] == assistance_request.topic.value
    assert expected_assistance_request["status"] == assistance_request.status.value


def test_get_should_return_an_assistance_request(faker, db_collection):
    expected_assistance_request = AssistanceRequest.stored(
        id=UUID(faker.uuid4()),
        description=faker.sentence(),
        status=faker.random_element(elements=[Status.Accepted, Status.Failed, Status.Succeeded]),
        topic=faker.random_element(elements=[Topic.Sales, Topic.Pricing]),
    )
    db_collection.insert_one(
        {
            "_id": str(expected_assistance_request.id),
            "topic": expected_assistance_request.topic.value,
            "description": expected_assistance_request.description,
            "status": expected_assistance_request.status.value,
        }
    )
    repository = MongoDbAssistancesRepository(db_collection=db_collection)

    assistance_request = repository.get(id=expected_assistance_request.id)

    assert assistance_request.id == expected_assistance_request.id
    assert assistance_request.description == expected_assistance_request.description
    assert assistance_request.status == expected_assistance_request.status
    assert assistance_request.topic == expected_assistance_request.topic


def test_get_should_raises_assistance_request_not_found_when_assistance_does_not_exist(faker, db_collection):
    repository = MongoDbAssistancesRepository(db_collection=db_collection)

    with pytest.raises(AssistanceRequestNotFoundError):
        repository.get(id=faker.uuid4())
