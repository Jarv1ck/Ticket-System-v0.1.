from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
import datetime

class Product(models.Model):
    title = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo/products')

    def __str__(self):
        return self.title

TICKET_STATUS_CHOICES = [
    ('New', 'New'),
    ('Troubleshooting', 'Troubleshooting'),
    ('Closed', 'Closed')
]

class File(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True, default='File')
    file = models.FileField(upload_to='files/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='New')
    responsible_user = models.ForeignKey(User,related_name='Responsible', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        return reverse("tickets:detail", kwargs={"id": self.pk})

class TicketComment(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    posted = models.BooleanField(default=True)

    def __str__(self):
        return 'User {} commented  in {}'.format(self.creator, self.ticket)


