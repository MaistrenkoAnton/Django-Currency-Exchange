from django.db import models
from django.utils.translation import ugettext_lazy as _


class Rate(models.Model):

    currency = models.CharField(max_length=3, unique=True)
    value = models.DecimalField(max_digits=20, decimal_places=6)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('currency',)

    def __str__(self):
        return _("%s at %.2f") % (self.currency, self.value)
