import io
from reportes.services.generators.base_generator import BaseReportGenerator


class DocenteReportGenerator(BaseReportGenerator):

    def _get_queryset(self):
        from docentes.models.docente import Docente
        qs = Docente.objects.select_related('user').filter(estado=True)
        if self.filtros.get('especialidad'):
            qs = qs.filter(especialidad__icontains=self.filtros['especialidad'])
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
        elementos = [Paragraph('Reporte de Docentes', styles['Title'])]

        datos = [['Nombre', 'Email', 'Especialidad', 'Horas máx.']]
        for docente in self._get_queryset():
            datos.append([
                docente.user.nombre,
                docente.user.email,
                docente.especialidad,
                str(docente.horas_max_semanales),
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
        ws.title = 'Docentes'
        ws.append(['Nombre', 'Email', 'Especialidad', 'Horas máx.'])
        for docente in self._get_queryset():
            ws.append([
                docente.user.nombre,
                docente.user.email,
                docente.especialidad,
                docente.horas_max_semanales,
            ])
        buffer = io.BytesIO()
        wb.save(buffer)
        return buffer.getvalue()