"""
    Modelos de la app TFMs.

    Autores:
        - Emilio Sánchez Catalán <esc00019@gmail.com>.

      Version: 1.0.
"""

from django.db import models
from ckeditor.fields import RichTextField
from core.models import Tutor2, Masters
from announcements.models import AnnouncementsTfm

# Create your models here.
class Tfms(models.Model):

    """
        Modelo en el que se alvergarán la información referente a los
        TFMs
    """

    # Tipo de tfm
    TYPE_UNI = 0
    TYPE_TEXT_UNI = "Empresa"
    TYPE_BUSINESS = 1
    TYPE_TEXT_BUSINESS = "Universidad"
    TYPE_CHOICE = (
        (TYPE_BUSINESS, TYPE_TEXT_UNI),
        (TYPE_UNI, TYPE_TEXT_BUSINESS),
    )

    # Estado de Validacion
    NOT_VALIDATED = 0
    DEPARTAMENT_VALIDATION = 1
    CENTER_VALIDATION = 2
    FAIL_VALIDATION = 3

    # Campos del modelo
    title = models.CharField(max_length=255, verbose_name="Título")
    type = models.PositiveSmallIntegerField(verbose_name="Tipo de proyecto", choices=TYPE_CHOICE)
    objectives = RichTextField(verbose_name="objectivos")
    methodology = RichTextField(verbose_name="Metodología")
    docs_and_forms = RichTextField(verbose_name="Documentos y formatos de entrega")
    language = models.CharField(max_length=45, verbose_name="Idioma")
    knowledge = RichTextField(null=True, verbose_name="Conocimientos requeridos", blank=True)
    departament_validation = models.BooleanField(
        null=True,
        verbose_name="Validación del departamento"
    )
    center_validation = models.BooleanField(null=True, verbose_name="Validación del centro")
    draft = models.BooleanField(verbose_name="Borrador")
    date_assignment = models.DateTimeField(verbose_name="Fecha de asignación", null=True)
    tutor1 = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        verbose_name="Tutor principal",
        related_name="tfms"
    )
    tutor2 = models.ForeignKey(
        Tutor2,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Tutor de apoyo",
        blank=True
    )
    masters = models.ForeignKey(Masters, on_delete=models.CASCADE, verbose_name="Master")
    announcements = models.ForeignKey(
        AnnouncementsTfm,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Convocatoria"
    )
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return u'{0}'.format(self.title)

    class Meta:
        ordering = ['-updatedAt']
        verbose_name = 'Trabajo final de master'
        verbose_name_plural = 'Trabajos finales de master'
