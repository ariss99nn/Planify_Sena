from abc import ABC, abstractmethod


class BaseReportGenerator(ABC):
    """Clase base para todos los generadores de reportes."""

    def __init__(self, filtros: dict):
        self.filtros = filtros

    @abstractmethod
    def generar_pdf(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def generar_excel(self) -> bytes:
        raise NotImplementedError