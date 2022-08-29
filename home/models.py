from django.db import models


class counter(models.Model):

    n=models.IntegerField()
    t=models.IntegerField()
    recahng=models.IntegerField(default=None)


class result(models.Model):

    nfa_nfa=models.TextField()
    nfa_pandas=models.TextField()

    dfa_dfa=models.TextField()
    dfa_pandas=models.TextField()
