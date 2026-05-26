from django.db import models
from django.core.exceptions import ValidationError


class Disponibilidad(models.Model):
    """
    Disponibilidad de un docente en un BloqueHorario especifico.
    CORRECCION: id_docente->docente, id_bloque->bloque (convencion Django).
    db_table eliminado; Django genera el nombre automaticamente.
    """
    docente = models.ForeignKey(
        'docentes.Docente',
        on_delete=models.CASCADE,
        related_name='disponibilidades',
    )
    bloque = models.ForeignKey(
        'bhorario.BloqueHorario',
        on_delete=models.CASCADE,
        related_name='disponibilidades',
    )
    disponible = models.BooleanField(default=True)
    motivo = models.TextField(
        blank=True,
        help_text='Obligatorio cuando disponible=False.',
    )

    class Meta:
        verbose_name        = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidades'
        unique_together = [('docente', 'bloque')]

    def __str__(self):
        estado = 'Disponible' if self.disponible else 'No disponible'
        return f"{self.docente} - {self.bloque} ({estado})"

    def clean(self):
        if not self.disponible and not self.motivo:
            raise ValidationError(
                {'motivo': 'Debe especificar un motivo si no esta disponible.'}
            )