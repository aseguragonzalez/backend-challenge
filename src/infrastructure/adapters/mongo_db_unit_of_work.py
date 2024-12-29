from pymongo.client_session import ClientSession

from src.seedwork.domain import UnitOfWork


class MongoDbUnitOfWork(UnitOfWork):
    def __init__(self, session: ClientSession | None) -> None:
        self._session = session

    def __enter__(self) -> "MongoDbUnitOfWork":
        if self._session:
            self._session.start_transaction()
        return self

    def __exit__(self, exc_type: type, exc_val: Exception, exc_tb: object) -> None:
        if not self._session:
            return None

        if exc_val:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        if self._session and self._session.in_transaction:
            self._session.commit_transaction()

    def rollback(self) -> None:
        if self._session and self._session.in_transaction:
            self._session.abort_transaction()
