from django.db import models
from django.db.models import constraints


class Visitor(models.Model):
    name = models.CharField(max_length=50)
    birth_date = models.DateField()
    passport_number = models.CharField(max_length=9)

    def __str__(self):
        return self.name

    pass


class Registration(models.Model):
    lend_date = models.DateField()
    return_date = models.DateField()
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    def __str__(self):
        r_str = '№ ' + str(self.id) + ', Name: ' + str(self.visitor) + ', Books: '
        for b in self.bookinstance_set.all():
            r_str += str(b)
        return r_str

    pass


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + ', ' + str(self.author)

    pass


class BookInstance(models.Model):
    type = models.ForeignKey(Book, on_delete=models.CASCADE)
    registration = models.ForeignKey(Registration, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=['type', 'registration'], name='unique_booking')
        ]
        pass

    def __str__(self):
        return str(self.type) + ' № ' + str(self.id)

    pass


class User(models.Model):
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.login

    pass
