from django.db import models

from apps.core.abstracts.models import CreatedModifiedAbstract
from apps.core.constants import BOOK_CATEGORY 

class BookManager(models.Manager):
    """Book Manager"""

    def get_books_by_tags(self, *tags):
        """Get books by list of tags"""
        
        return self.filter(tags__name__in=tags)
    

class BookAuthor(models.Model):
    """ManyToMany intermediate table between Book and Author"""

    BOOK_AUTHOR_ROLE = {
        'author': 'Author',
        'co_author': 'Co-Author',
        'editor': 'Editor'
    }
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    author = models.ForeignKey('book.Author', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=BOOK_AUTHOR_ROLE, default='author')

    def __str__(self) -> str:
        return f'{self.author} {self.role} {self.book}'
    
    class Meta:
        verbose_name_plural = 'Books and Authors'

class Book(CreatedModifiedAbstract):
    
    BOOK_FORMAT = {
        "eb": "ebook",
        "hc": "hardcover"
    }
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    page_count = models.PositiveSmallIntegerField()
    category = models.CharField(max_length=2, choices=BOOK_CATEGORY, default='pr')
    published_date = models.IntegerField()
    publisher = models.CharField(max_length=50)
    authors = models.ManyToManyField('book.Author', through='book.BookAuthor')
    lang = models.CharField(max_length=50)
    edition = models.SmallIntegerField(null=True, blank=True)
    book_format = models.CharField(max_length=2, choices=BOOK_FORMAT, default='eb')
    tags = models.ManyToManyField('book.Tag')


    objects = BookManager()

    @property
    def short_des(self):
        """Short version of description"""

        return f'{self.description[:30] if self.description else ""}...' #pylint: disable=E1136

    def __str__(self) -> str:
        return f'{self.title}({self.isbn})'

    class Meta:
        ordering = ('-title',)
        default_related_name = '%(app_label)s_%(model_name)s'