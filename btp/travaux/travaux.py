# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from btp.utility.unite import Unite

class Travaux(models.Model):
    id_travaux = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    libelle = models.CharField(unique=True, max_length=100)
    prix_unitaire = models.FloatField(blank=True, null=True)
    unite = models.ForeignKey('Unite', models.DO_NOTHING, db_column='unite')

    class Meta:
        managed = False
        db_table = 'travaux'
