from django.db import models
from programa.models.programa_model import Programa


class VersionPrograma(models.Model):
    programa = models.ForeignKey(
        Programa,
        on_delete=models.PROTECT,
        related_name='versiones',
    )
    numero      = models.PositiveIntegerField(help_text='Numero de version. Ej: 1, 2.')
    descripcion = models.TextField(blank=True)
    vigente = models.BooleanField(default=False, db_index=True)
    fecha_inicio = models.DateField()
    fecha_fin    = models.DateField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Version de programa'
        verbose_name_plural = 'Versiones de programa'
        ordering = ['programa', '-numero']
        unique_together = [('programa', 'numero')]

    def __str__(self):
        return f"{self.programa.nombre} v{self.numero}"

    @property
    def total_horas(self):
        return sum(m.total_horas for m in self.modulos.all())

    def save(self, *args, **kwargs):
        if self.vigente:
            VersionPrograma.objects.filter(
                programa=self.programa, vigente=True,
            ).exclude(pk=self.pk).update(vigente=False)
        super().save(*args, **kwargs)