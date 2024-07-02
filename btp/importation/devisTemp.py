# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DevisTemp(models.Model):
    client = models.CharField(max_length=50, blank=True, null=True)
    ref_devis = models.CharField(max_length=50, blank=True, null=True)
    type_maison = models.CharField(max_length=50, blank=True, null=True)
    finition = models.CharField(max_length=50, blank=True, null=True)
    taux_finition = models.FloatField(blank=True, null=True)
    date_devis = models.CharField(max_length=50, blank=True, null=True)
    date_debut = models.CharField(max_length=50, blank=True, null=True)
    lieu = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devis_temp'
