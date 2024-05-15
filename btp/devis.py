# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Devis(models.Model):
    id_devis = models.AutoField(primary_key=True)
    prix_total = models.FloatField(blank=True, null=True)
    date_debut_construction = models.DateField(blank=True, null=True)
    date_fin_construction = models.DateField(blank=True, null=True)
    date_devis = models.DateField(blank=True, null=True)
    ref_devis = models.CharField(max_length=50, blank=True, null=True)
    paiement_effectue = models.FloatField(blank=True, null=True)
    lieu = models.ForeignKey('Lieu', models.DO_NOTHING, db_column='lieu', blank=True, null=True)
    finition = models.ForeignKey('Finition', models.DO_NOTHING, db_column='finition')
    client = models.ForeignKey('Utilisateurs', models.DO_NOTHING, db_column='client')
    type = models.ForeignKey('TypeMaison', models.DO_NOTHING, db_column='type')
    pourcentage = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'devis'
