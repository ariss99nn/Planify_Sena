import csv
import io
from typing import List


class ExportacionService:
    """
    Exporta datos de cualquier módulo a CSV o Excel.
    Sin Celery — respuesta directa ya que CSV es liviano.
    Para archivos grandes usar la tarea async de reportes/.
    """

    @staticmethod
    def exportar_fichas(filtros: dict, formato: str) -> tuple:
        from ficha.models.ficha_model import Ficha
        qs = Ficha.objects.select_related(
            'version__programa', 'jefe_grupo'
        ).filter(estado=True)
        if filtros.get('etapa'):
            qs = qs.filter(etapa=filtros['etapa'])
        if filtros.get('jornada'):
            qs = qs.filter(jornada=filtros['jornada'])

        headers = [
            'codigo_ficha', 'programa', 'version',
            'etapa', 'trimestre', 'jornada',
            'estudiantes_estimados', 'estudiantes_reales',
            'jefe_grupo', 'fecha_inicio', 'fecha_finalizacion',
        ]
        rows = [
            [
                f.codigo_ficha,
                f.version.programa.nombre,
                f.version.numero,
                f.get_etapa_display(),
                f.trimestre,
                f.get_jornada_display(),
                f.numero_estudiantes_estimado,
                f.numero_estudiantes_real,
                f.jefe_grupo.nombre if f.jefe_grupo else '',
                f.fecha_inicio.isoformat(),
                f.fecha_finalizacion.isoformat() if f.fecha_finalizacion else '',
            ]
            for f in qs
        ]
        return headers, rows

    @staticmethod
    def exportar_docentes(filtros: dict, formato: str) -> tuple:
        from docentes.models.docente import Docente
        qs = Docente.objects.select_related('user').filter(estado=True)
        if filtros.get('especialidad'):
            qs = qs.filter(especialidad__icontains=filtros['especialidad'])

        headers = ['nombre', 'email', 'especialidad', 'horas_max_semanales']
        rows = [
            [d.user.nombre, d.user.email, d.especialidad, d.horas_max_semanales]
            for d in qs
        ]
        return headers, rows

    @staticmethod
    def exportar_bloques_horario(filtros: dict, formato: str) -> tuple:
        from bhorario.models.bloque_horario_model import BloqueHorario
        qs = BloqueHorario.objects.select_related(
            'docente__user', 'aula', 'ficha__version__programa'
        )
        if filtros.get('dia_semana'):
            qs = qs.filter(dia_semana=filtros['dia_semana'])
        if filtros.get('jornada'):
            qs = qs.filter(jornada=filtros['jornada'])

        headers = [
            'dia', 'hora_inicio', 'hora_fin', 'jornada',
            'docente', 'aula', 'ficha', 'programa',
        ]
        rows = [
            [
                b.get_dia_semana_display(),
                b.hora_inicio.strftime('%H:%M'),
                b.hora_fin.strftime('%H:%M'),
                b.get_jornada_display(),
                b.docente.user.nombre if b.docente else '',
                b.aula.codigo_aula if b.aula else '',
                b.ficha.codigo_ficha if b.ficha else '',
                b.ficha.version.programa.nombre if b.ficha else '',
            ]
            for b in qs
        ]
        return headers, rows

    @classmethod
    def exportar(cls, modulo: str, filtros: dict, formato: str) -> tuple:
        handlers = {
            'fichas': cls.exportar_fichas,
            'docentes': cls.exportar_docentes,
            'bloques_horario': cls.exportar_bloques_horario,
        }
        handler = handlers.get(modulo)
        if not handler:
            raise ValueError(f'Módulo "{modulo}" no tiene exportador definido.')
        return handler(filtros, formato)

    @staticmethod
    def a_csv(headers: list, rows: list) -> bytes:
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(headers)
        writer.writerows(rows)
        return buffer.getvalue().encode('utf-8-sig')  # BOM para Excel en Windows

    @staticmethod
    def a_excel(headers: list, rows: list) -> bytes:
        try:
            import openpyxl
        except ImportError:
            raise RuntimeError('Instala openpyxl: pip install openpyxl')
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        for row in rows:
            ws.append(row)
        buffer = io.BytesIO()
        wb.save(buffer)
        return buffer.getvalue()