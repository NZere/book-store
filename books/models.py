import json
import urllib.parse
from django.contrib.postgres.fields import ArrayField
from django.db import models
from rest_framework import serializers


class Book(models.Model):
    title = models.CharField(max_length=100)
    # authors = ArrayField(models.CharField(max_length=100), default=list)
    authors = models.TextField()
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='book_covers/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    popularity = models.IntegerField(default=0)
    category = models.CharField(max_length=50, default="UNCATEGORISED", choices=(
        ('EDUCATIONAL', 'EDUCATIONAL'),
        ('SELFHELP', 'SELFHELP'),
        ('NOVELS', 'NOVELS'),
        ('FINANCE', 'FINANCE'),
        ('COMICS', 'COMICS'),
        ('UNCATEGORISE', 'UNCATEGORISE'),
    ))

    def get_image_url(self):
        self.image = urllib.parse.unquote(self.image.url)
        return self.image

    def __str__(self):
        return self.title

    def set_authors(self, value):
        self.authors = json.dumps(value)

    def get_authors(self):
        return json.loads(self.authors)

    # def image_url(self):
    #     print(self.image.url)
    #     return

