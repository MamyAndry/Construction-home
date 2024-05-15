from django.db import connection
from django.db.models import Q
from btp.utilisateurs import Utilisateurs
import re

# Create your models here.

def login(numero):
    utilisateur = Utilisateurs.objects.filter(numero__exact=numero).values('id_utilisateur', 'numero', 'role')
    user = Utilisateurs()
    if len(utilisateur) == 1:
        user = utilisateur[0]
    else:
        if len(numero) == 10:
            user.numero = numero
            user.role = 10
            user.save()
        else:
            user = None
    return user

def log_admin(email, password):
    utilisateur = Utilisateurs.objects.filter(Q(email__exact=email) & Q(mot_de_passe__exact=password)).values('id_utilisateur', 'numero', 'role')
    user = Utilisateurs()
    if len(utilisateur) == 1:
        user = utilisateur[0]
    else:
        return None
    return user

def get_montant_devis(devis):
    string = "SELECT total FROM v_montant_devis WHERE devis = %s" %str(devis)
    with connection.cursor() as c:
        c.execute(string)
        row = c.fetchone()
    return row[0]

def get_duree_total_devis(devis):
    string = "SELECT duree FROM v_duree_total_devis WHERE devis = %s" %str(devis)
    with connection.cursor() as c:
        c.execute(string)
        row = c.fetchone()
    return row[0]

def get_montant_total(devis, pourcentage):
    res = 0 
    prix_revient = get_montant_devis(devis)
    majoration = (pourcentage * prix_revient) / 100
    res += prix_revient + majoration
    return res

def insert_details_devis(devis):
    id = str(devis)
    string = "INSERT INTO details_devis(travaux, devis, quantite, prix_unitaire) (SELECT travaux, devis, quantite, COALESCE(prix_unitaire, 0) from v_details_devis WHERE devis = %s)" %id
    with connection.cursor() as c:
        c.execute(string)
    return


def montant_total_devis():
    string = "SELECT COALESCE(SUM(prix_total),0) from devis"
    with connection.cursor() as c:
        c.execute(string)
        row = c.fetchone()
    return f"{row[0]:,.2f}"

def montant_paiement_effectue_total_devis():
    string = "SELECT COALESCE(SUM(paiement_effectue),0) from devis"
    with connection.cursor() as c:
        c.execute(string)
        row = c.fetchone()
    return f"{row[0]:,.2f}"


def get_annee():
    string = "SELECT DISTINCT extract('year' from date_devis) FROM devis"
    with connection.cursor() as c:
        c.execute(string)
        rows = c.fetchall()
    res = list()
    for row in rows:
        res.append(int(row[0]))
    return res

def montant_devis_par_mois_par_an(annee):
    annee = int(annee)
    string = " SELECT m.libelle, COALESCE(q.total, 0) montant from mois m LEFT JOIN (SELECT SUM(prix_total) total, extract('month' from date_devis) mois FROM devis WHERE extract('year' from date_devis) = %s GROUP BY mois) q ON m.id_mois = q.mois" %str(annee)
    with connection.cursor() as c:
        c.execute(string)
        rows = c.fetchall()
    res = list()
    for row in rows:
        res.append(int(row[1]))
    return res
