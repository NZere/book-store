from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='book_covers/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    popularity = models.IntegerField(default=0)
    genre = models.CharField(max_length=50, choices=(
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Science Fiction', 'Science Fiction'),
        # Add more genres as needed
    ))

    def __str__(self):
        return self.title
