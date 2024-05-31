from django.db import connection
from django.db.models import Q
from btp.utilisateurs import Utilisateurs
import re

# Create your models here.

# def check_if_numero(numero):
#     success = False
#     if numero.startswith("0"):
#         if numero[1] == "2" and numero[2] == "0":
#             if "0" <= numero[3] <= "9":
#                 if len(numero) == 10:
#                     return True
#         elif numero[1] == "3" and numero[2] in  ["2", "3", "4", "7", "8"]:
#             if "0" <= numero[3] <= "9":
#                 if len(numero) == 10:
#                     return True
                        
#     elif numero.startswith("+261"):
#         if numero[4] == "2" and numero[5] == "0":
#             if "0" <= numero[6] <= "9":
#                 if len(numero) == 10:
#                     return True
#         elif numero[4] == "3" and numero[5] in  ["2", "3", "4", "7", "8"]:
#             if "0" <= numero[6] <= "9":
#                 if len(numero) == 13:
#                     return True
#     return success


def check_if_numero(numero):
    pattern_02 = r'^0(2)0\d{7}$'
    pattern_03 = r'^0(3)[02478]\d{7}$'
    pattern_261_2 = r'^\+261(2)0\d{7}$'
    pattern_261_3 = r'^\+261(3)[02478]\d{7}$'
    
    pattern_02_compiled = re.compile(pattern_02)
    pattern_03_compiled = re.compile(pattern_03)
    pattern_261_2_compiled = re.compile(pattern_261_2)
    pattern_261_3_compiled = re.compile(pattern_261_3)
    
    if pattern_02_compiled.match(numero) or pattern_03_compiled.match(numero) or pattern_261_2_compiled.match(numero) or pattern_261_3_compiled.match(numero):
        return True
    else:
        return False


def login(numero):
    user = None
    if check_if_numero(numero) is True:
        utilisateur = Utilisateurs.objects.filter(numero__exact=numero).values('id_utilisateur', 'numero', 'role')
        user = Utilisateurs()
        if len(utilisateur) == 1:
            user = utilisateur[0]
        else:
            user.numero = numero
            user.role = 10
            user.save()
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
    string = """INSERT INTO details_devis(travaux, devis, quantite, prix_unitaire) 
                (SELECT travaux, devis, quantite, COALESCE(prix_unitaire, 0) from v_details_devis WHERE devis = %s)""" %id
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
    string = "SELECT COALESCE(SUM(montant),0) from paiement"
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
    string = """SELECT m.libelle, COALESCE(q.total, 0) montant FROM 
        mois m LEFT JOIN (SELECT SUM(prix_total) total, extract('month' from date_devis) mois 
            FROM devis WHERE extract('year' from date_devis) = %s GROUP BY mois) q 
                ON m.id_mois = q.mois""" %str(annee)
    with connection.cursor() as c:
        c.execute(string)
        rows = c.fetchall()
    res = list()
    for row in rows:
        res.append(int(row[1]))
    return res

def clean_datas():
    string = """
        TRUNCATE TABLE maison_temp, devis_temp, paiement_temp, details_devis, details_construction, paiement, devis, lieu, type_maison, finition, travaux, unite, utilisateurs RESTART IDENTITY CASCADE;
        INSERT INTO utilisateurs(numero, email, mot_de_passe, role) VALUES 
            ('0344881819', 'email@email.com', 'mdp', 0);"""
    with connection.cursor() as c:
        c.execute(string)
