import io
from reportes.services.generators.base_generator import BaseReportGenerator


class AulaReportGenerator(BaseReportGenerator):

    def _get_queryset(self):
        from aulas.models.aula import Aula
        qs = Aula.objects.select_related('bloque')
        if self.filtros.get('estado'):
            qs = qs.filter(estado=self.filtros['estado'])
        if self.filtros.get('tipo_aula'):
            qs = qs.filter(tipo_aula=self.filtros['tipo_aula'])
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
        elementos = [Paragraph('Reporte de Aulas', styles['Title'])]

        datos = [['Código', 'Bloque', 'Tipo', 'Estado', 'Capacidad']]
        for aula in self._get_queryset():
            datos.append([
                aula.codigo_aula,
                aula.bloque.nombre if aula.bloque else '—',
                aula.get_tipo_aula_display(),
                aula.get_estado_display(),
                str(aula.capacidad),
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
        ws.title = 'Aulas'
        ws.append(['Código', 'Bloque', 'Tipo', 'Estado', 'Capacidad'])
        for aula in self._get_queryset():
            ws.append([
                aula.codigo_aula,
                aula.bloque.nombre if aula.bloque else '',
                aula.get_tipo_aula_display(),
                aula.get_estado_display(),
                aula.capacidad,
            ])
        buffer = io.BytesIO()
        wb.save(buffer)
        return buffer.getvalue()