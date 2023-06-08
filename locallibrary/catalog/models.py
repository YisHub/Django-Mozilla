from django.db import models
import uuid
from django.urls import reverse
import random

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")
    
    def __str__(self):

        return self.name

class Language(models.Model):

    name = models.CharField(max_length=200,
                            help_text="Ingrsa el lenguaje natural del libro (English, French, Japanese etc.)")

    def __str__(self):

        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")

    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>*Si no se proporciona un ISBN, se generará uno aleatoriamente de 13 dígitos.*', default=''.join([str(random.randint(0, 9)) for _ in range(13)]))


    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):

        return self.title
    
    def display_genre(self):
  
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])

    display_genre.short_description = 'Genre'


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('book-detail', args=[str(self.id)])
    
class BookInstance(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    imprint = models.CharField(max_length=200)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):

        return '%s (%s)' % (self.id,self.book.title)
    
class Author(models.Model):

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    date_of_birth = models.DateField(null=True, blank=True)

    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):

        return reverse('author-detail', args=[str(self.id)])


    def __str__(self):

        return '%s, %s' % (self.last_name, self.first_name)