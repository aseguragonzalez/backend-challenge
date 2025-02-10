from src.application.services import FailAssistanceService, SendAssistanceService
from src.seedwork.infrastructure.ports.dependency_injection import ServiceProvider


def fail_assistance_service(sp: ServiceProvider) -> None:
    sp.register_singleton(FailAssistanceService, FailAssistanceService)


def send_assistance_service(sp: ServiceProvider) -> None:
    sp.register_singleton(SendAssistanceService, SendAssistanceService)
