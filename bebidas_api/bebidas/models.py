from django.db import models

#Para referencia
class Bebida:
    def __init__(self, id, nombre, tipo, tamanio):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.tamanio = tamanio