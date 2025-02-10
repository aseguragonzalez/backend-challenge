# Landbot Backend Challenge

## Overview

This project is a solution for the **Landbot Backend Challenge**, implementing an assistance request system using the **Outbox pattern** for handling third-party integrations asynchronously. The system ensures scalability, reliability, and fault tolerance by leveraging **FastAPI**, **message brokers**, and **background services**.

## Features

- **FastAPI**: Provides a high-performance web API.
- **Asynchronous Processing**: Uses an event-driven architecture with a message broker.
- **Outbox Pattern**: Ensures consistency between database transactions and message publishing.
- **Scalability**: Supports horizontal scaling via containerization.
- **Automated Testing**: Includes integration tests using **pytest** and **Testcontainers**.
- **Pre-commit Hooks**: Enforces code quality and formatting.
- **Development Container (Devcontainer)**: Supports reproducible development environments.

## Build With

- [FastAPI][fastapi]
- [pre-commit][pre-commit]
- [pytest][pytest]
- [Testcontainers][testcontainers]
- [Postman][postman] for API testing
- [MongoDB][mongodb] as NoSQL Database
- [RabbitMQ][rabbitmq] as Message Broker
- [Docker][docker]
- [VS Code][vscode] with [Devcontainers Extension][devcontainer]

## Installation

### Prerequisites

Ensure you have the following installed:

- [Docker][docker]
- [VS Code][vscode]
- [Devcontainers Extension][devcontainer]

### Getting started (Using Devcontainer)

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Open in VS Code:

   ```sh
   code .
   ```

3. When prompted, reopen the project in a devcontainer.
4. Once inside the container, install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

5. Start components from devcontainer terminal:

    You can use the launch configurations provided in `.vscode/launch.json` to start the services.

    or manually unsing the following commands:

    - API: `$python dev src/infrastructure/ports/api/main.py --reload --host 0.0.0.0 --port 8000`
    - DLQ Consumer: `$python -m src.infrastructure.ports.dlq.main`
    - Publisher: `$python -m src.infrastructure.ports.publisher.main`
    - Reconcilier: `$python -m src.infrastructure.ports.reconciler.main`
    - Subscriber: `$python -m src.infrastructure.ports.subscriber.main`

6. Run tests:

   ```sh
   pytest
   ```

## How to run

You can run the services using **Docker Compose**:

1. Build the images:

   ```sh
   docker-compose build
   ```

2. Start the services:

   ```sh
    docker-compose up
    ```

3. Use the API:

    The API exposes endpoints for assistance requests and it is available at [http://localhost:8000][api]. Also, it exposes an OpenAPI documentation at [http://localhost:8000/docs][api-docs]. You can interact with it using **cURL**, importing the **Postman Collection** from `docs` folder.

## License

This project is licensed under the [MIT License](LICENSE).

[api-docs]: http://localhost:8000/docs
[api]: http://localhost:8000
[devcontainer]: https://code.visualstudio.com/docs/remote/containers
[docker]: https://www.docker.com/
[fastapi]: https://fastapi.tiangolo.com/
[mongodb]: https://www.mongodb.com/
[postman]: https://www.postman.com/
[pre-commit]: https://pre-commit.com/
[pytest]: https://docs.pytest.org/en/stable/
[rabbitmq]: https://www.rabbitmq.com/
[testcontainers]: https://testcontainers.org/
[vscode]: https://code.visualstudio.com/
