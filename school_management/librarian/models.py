from django.db import models

# Create your models here.
class Book(models.Model):
    
    CATEGORY_CHOICES = (
        ('novel', 'Novel'),
        ('poem', 'Poem'),
        ('mystery', 'Mystery'),
        ('fantasy', 'Fantasy'),
        ('biography', 'Biography'),
        ('science_fiction', 'Science Fiction'),
        ('historical', 'Historical'),
    )
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    available = models.CharField(max_length=50, default="instock") 
    
    def __str__(self):
        return self.title


class LibraryRecord(models.Model):
    student = models.ForeignKey("student.Student", on_delete=models.CASCADE)
    book = models.ForeignKey("librarian.Book", on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(null= True, blank=True)
    lend_date = models.DateTimeField(blank=True, null=True)