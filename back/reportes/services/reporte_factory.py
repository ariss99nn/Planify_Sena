class ReporteFactory:
    """
    Factory Pattern para generadores de reportes.
    Cada generador implementa generar_pdf() y generar_excel().
    """
    _registro: dict = {}

    @classmethod
    def registrar(cls, tipo: str, generador_cls):
        cls._registro[tipo] = generador_cls

    @classmethod
    def crear(cls, tipo: str, filtros: dict):
        generador_cls = cls._registro.get(tipo)
        if not generador_cls:
            tipos = ', '.join(cls._registro.keys())
            raise ValueError(
                f'Tipo desconocido: "{tipo}". Disponibles: {tipos}'
            )
        return generador_cls(filtros)