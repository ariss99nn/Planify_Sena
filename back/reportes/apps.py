from django.apps import AppConfig


class ReportesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reportes'

    def ready(self):
        from reportes.services.reporte_factory import ReporteFactory
        from reportes.services.generators.ficha_generator import FichaReportGenerator
        from reportes.services.generators.docente_generator import DocenteReportGenerator
        from reportes.services.generators.aula_generator import AulaReportGenerator
        ReporteFactory.registrar('fichas', FichaReportGenerator)
        ReporteFactory.registrar('docentes', DocenteReportGenerator)
        ReporteFactory.registrar('aulas', AulaReportGenerator)