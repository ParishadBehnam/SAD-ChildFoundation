from __future__ import unicode_literals

from django.db import models
from active_user.models import active_user
from madadjoo.models import madadjoo
from madadkar.models import madadkar
from system.models import information


class hamyar(active_user):
    pass


class sponsership():
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    madadkar = models.ForeignKey(madadkar, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("madadjoo", "madadkar"),)

class hamyar_madadjoo_payment():
    madadjoo = models.ForeignKey(madadjoo, on_delete=models.CASCADE)
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    type = models.CharField(choices=['monthly', 'annual', 'instantly'], max_length=60)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (("madadjoo", "hamyar", "date"),)

class hamyar_system_payment():
    hamyar = models.ForeignKey(hamyar, on_delete=models.CASCADE)
    system = models.ForeignKey(information, on_delete=models.CASCADE)
    amount = models.IntegerField(null=False)
    date = models.DateField(auto_now=True)

    class Meta:
        unique_together = (("hamyar", "date"),)






