
from django.db import models


class Aprendiz(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=30)
    documento = models.CharField(max_length=30)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()
    ficha = models.CharField(max_length=20)

    # NUEVOS CAMPOS PARA LA UBICACION
    direccion = models.CharField(max_length=250, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    programa = models.ForeignKey(
        'Programa',
        on_delete=models.CASCADE,
        related_name='aprendices',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Programa(models.Model):
    nombre = models.CharField(max_length=150)
    ficha = models.CharField(max_length=20)
    jornada = models.CharField(max_length=50)
    duracion = models.CharField(max_length=50)
    modalidad = models.CharField(max_length=50)
    nivel_formacion = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Instructor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    documento = models.CharField(max_length=30)
    ficha_asignada = models.CharField(max_length=20)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Competencia(models.Model):
    nombre = models.CharField(max_length=150)
    ficha = models.CharField(max_length=20)

    programa = models.ForeignKey(
        Programa,
        on_delete=models.CASCADE,
        related_name='competencias',
        null=True,
        blank=True
    )

    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        related_name='competencias',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nombre
