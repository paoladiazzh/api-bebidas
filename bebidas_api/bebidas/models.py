from django.db import models

class Bebida(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    tamanio = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"