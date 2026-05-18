from django.db import models

class Post(models.Model):
    titulo = models.CharField(max_length=100) # Nombre del postre
    categoria = models.CharField(max_length=50, default="Postre") # ¡Nuestra mejora! (Pastel, Galleta, etc.)
    contenido = models.TextField() # Ingredientes y preparación
    fecha = models.DateTimeField(auto_now_add=True)
    autor = models.CharField(max_length=100) # Quién la comparte

    def __str__(self):
        return f"{self.titulo} ({self.categoria})"