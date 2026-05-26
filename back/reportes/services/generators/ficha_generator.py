import io
from reportes.services.generators.base_generator import BaseReportGenerator


class FichaReportGenerator(BaseReportGenerator):

    def _get_queryset(self):
        from ficha.models.ficha_model import Ficha
        qs = Ficha.objects.select_related(
            'version__programa', 'jefe_grupo'
        )
        if self.filtros.get('etapa'):
            qs = qs.filter(etapa=self.filtros['etapa'])
        if self.filtros.get('jornada'):
            qs = qs.filter(jornada=self.filtros['jornada'])
        if self.filtros.get('estado') is not None:
            qs = qs.filter(estado=self.filtros['estado'])
        return qs

    def generar_pdf(self) -> bytes:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
        except ImportError:
            raise RuntimeError('Instala reportlab: pip install reportlab')

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elementos = [Paragraph('Reporte de Fichas', styles['Title'])]

        datos = [['Código', 'Programa', 'Etapa', 'Trimestre', 'Jornada', 'Estudiantes']]
        for ficha in self._get_queryset():
            datos.append([
                ficha.codigo_ficha,
                ficha.version.programa.nombre,
                ficha.get_etapa_display(),
                str(ficha.trimestre),
                ficha.get_jornada_display(),
                str(ficha.numero_estudiantes_real),
            ])

        tabla = Table(datos)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        elementos.append(tabla)
        doc.build(elementos)
        return buffer.getvalue()

    def generar_excel(self) -> bytes:
        try:
            import openpyxl
        except ImportError:
            raise RuntimeError('Instala openpyxl: pip install openpyxl')

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Fichas'
        ws.append(['Código', 'Programa', 'Etapa', 'Trimestre', 'Jornada', 'Estudiantes'])

        for ficha in self._get_queryset():
            ws.append([
                ficha.codigo_ficha,
                ficha.version.programa.nombre,
                ficha.get_etapa_display(),
                ficha.trimestre,
                ficha.get_jornada_display(),
                ficha.numero_estudiantes_real,
            ])

        buffer = io.BytesIO()
        wb.save(buffer)
        return buffer.getvalue()