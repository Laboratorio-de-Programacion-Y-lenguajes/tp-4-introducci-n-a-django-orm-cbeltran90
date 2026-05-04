from __future__ import annotations

from django.db import models
from django.utils import timezone


class Autor(models.Model):
    """
    Representa a un autor/a.
    Requerido: nombre, email único, biografía opcional.
    """

    # TODO: implementar los campos del modelo
    # Ejemplo de campo:
    # nombre = models.CharField(max_length=120)
    #
    # nombre   → CharField (max_length a elección)
    # email    → EmailField (unique=True)
    # biografia → TextField (blank=True para hacerlo opcional)
    
    # Opcional: definir __str__ para que sea legible en el admin y en el shell
    # def __str__(self) -> str:
    #     return self.nombre

    nombre = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    biografia = models.TextField(blank=True)  # blank=True permite que quede vacío en formularios/admin

    def __str__(self):
        return self.nombre

    pass



class Categoria(models.Model):
    """
    Categoría temática de libros.
    Ejemplos: 'fantasía', 'ciencia ficción', 'historia'.
    """

    # TODO: implementar el campo nombre (unique=True)

    pass

    # def __str__(self) -> str:
    #     return self.nombre
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    """
    Libro del catálogo de la biblioteca.
    Tiene relación N:1 con Autor y N:M con Categoria.
    """

    # TODO: implementar los campos:
    # titulo          → CharField
    # isbn            → CharField (unique=True)
    # fecha_publicacion → DateField
    # cantidad_total  → PositiveIntegerField
    # autor           → ForeignKey(Autor, on_delete=models.PROTECT)
    # categorias      → ManyToManyField(Categoria)
    #
    # Preguntas guía:
    # ¿Qué pasa si eliminás un autor que tiene libros? (PROTECT vs CASCADE)
    # ¿Por qué isbn debe ser único?

    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    fecha_publicacion = models.DateField()
    cantidad_total = models.PositiveIntegerField(default=1)
    autor = models.ForeignKey(Autor, on_delete=models.PROTECT)
    categorias = models.ManyToManyField(Categoria)

    def __str__(self):
        return self.titulo

    pass

    def prestamos_activos(self) -> int:
        """
        Retorna la cantidad de préstamos activos (fecha_devolucion IS NULL).

        Un préstamo es "activo" cuando no se ha registrado devolución.
        """
        # TODO: implementar con ORM usando filter sobre los préstamos relacionados
        # Pista: self.prestamo_set.filter(fecha_devolucion__isnull=True).count()
        #        (o el related_name que hayas definido en Prestamo.libro)
        return self.prestamo_set.filter(fecha_devolucion__isnull=True).count()

    def disponibles(self) -> int:
        """
        Retorna cuántas copias están disponibles:
        cantidad_total - prestamos_activos()
        """
        # TODO: implementar
        return self.cantidad_total - self.prestamos_activos()

    def tiene_disponibles(self) -> bool:
        """Retorna True si hay al menos una copia disponible."""
        # TODO: implementar
        return self.disponibles() > 0


class Prestamo(models.Model):
    """
    Registro de un préstamo de libro a un usuario.
    Si fecha_devolucion es NULL → el préstamo está activo.
    """

    # TODO: implementar los campos:
    # libro              → ForeignKey(Libro, on_delete=models.CASCADE)
    # nombre_prestatario → CharField
    # fecha_prestamo     → DateField
    # fecha_devolucion   → DateField (null=True, blank=True)
    #
    # Preguntas guía:
    # ¿Por qué usamos CASCADE aquí y PROTECT en Libro→Autor?
    # ¿Qué valor por defecto tendría sentido para fecha_prestamo?
    # Tip: podés usar default=timezone.now si querés fecha automática,
    #      o dejarlo sin default para que el test lo defina explícitamente.

    pass

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_prestatario = models.CharField(max_length=120)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.libro.titulo} - {self.nombre_prestatario} - {self.fecha_prestamo}"