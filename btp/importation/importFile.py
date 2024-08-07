import csv
from datetime import datetime

from django.conf import settings
from django.db import connection

from .devisTemp import DevisTemp
from .maisonTemp import MaisonTemp
from .paiementTemp import PaiementTemp
from btp.paiement.paiement import Paiement

def cast_to_float(value):
    string = value.replace(",",".")
    return float(string)  

def check_is_data_travaux_valid(lines):
    bool = True
    try:
        if len(lines[0]) < 1:
            return False 
        if len(lines[1]) < 1:
            return False
        if cast_to_float(lines[2]) < 0:
            return False 
        if len(lines[3]) < 1:
            return False 
        if len(lines[4]) < 1:
            return False 
        if len(lines[5]) < 1:
            return False 
        if cast_to_float(lines[6]) < 0:
            return False 
        if cast_to_float(lines[7]) < 0:
            return False 
        if cast_to_float(lines[8]) < 0:
            return False 
    except:
        return False
    return bool

def check_is_data_devis_valid(lines):
    bool = True
    pattern = "%d/%m/%Y"
    try:
        if len(lines[0]) < 10:
            return False 
        if len(lines[1]) < 1:
            return False
        if len(lines[2]) < 1:
            return False 
        if len(lines[3]) < 1:
            return False 
        if cast_to_float(lines[4].replace("%","")) < 0:
            return False 
        date_1 = datetime.strptime(lines[5],pattern)
        date_2 = datetime.strptime(lines[6],pattern)
        print(date_1)
        if date_1 > date_2:
            return False 
        if len(lines[7]) < 1:
            return False 
    except:
        return False
    return bool

def check_reference_paiement(ref):
    paiement = Paiement.objects.filter(ref_paiement__exact = ref)
    if(not paiement):
        print(paiement)
        return True
    return False

def check_is_data_paiement_valid(lines):
    bool = True
    try:
        if len(lines[0]) < 1:
            return False 
        if len(lines[1]) < 1:
            return False
        date_1 = datetime.strptime(lines[2],"%d/%m/%Y")
        if cast_to_float(lines[3]) < 0:
            return False 
        if check_reference_paiement(lines[1]) is False:
            return False       
    except:
        return False
    return bool

def treat_csv_travaux():
    count  = 0
    error_line = []
    print(settings.FILES_DIR)
    with open(settings.FILES_DIR + '/uploads/maison_travaux.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if count > 0:
                if check_is_data_travaux_valid(lines):
                    maison = MaisonTemp()    
                    maison.type_maison = lines[0]
                    maison.description = lines[1]  
                    maison.surface = lines[2]  
                    maison.code_travaux = lines[3]
                    maison.type_travaux = lines[4]
                    maison.unite = lines[5]
                    maison.prix_unitaire = cast_to_float(lines[6])
                    maison.quantite = cast_to_float(lines[7])
                    maison.duree_travaux = lines[8]
                    maison.save()
                else:   
                    error_line.append("error on line"+str(count) + " of maison_travaux.csv\n")
            count += 1
    res = "".join(error_line)
    print(res)
    return res + "".join(fill_tables_travaux_maison())  

def treat_csv_devis():
    count  = 0
    error_line = []
    with open(settings.FILES_DIR + '/uploads/devis.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if count > 0:
                if check_is_data_devis_valid(lines):
                    devis = DevisTemp()
                    devis.client = lines[0]
                    devis.ref_devis = lines[1]
                    devis.type_maison = lines[2]
                    devis.finition = lines[3]
                    devis.taux_finition = cast_to_float(lines[4].replace("%",""))
                    devis.date_devis = lines[5]
                    devis.date_debut = lines[6]
                    devis.lieu = lines[7]
                    devis.save()
                else:
                    error_line.append("error on line"+str(count) + " of devis.csv\n")
            count += 1
    res = "".join(error_line)
    return res + "".join(fill_tables_devis())
    


def treat_csv_paiement():
    count  = 0
    error_line = []
    with open(settings.FILES_DIR + '/uploads/paiement.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            if count > 0:
                if check_is_data_paiement_valid(lines):
                    paiement = PaiementTemp()
                    paiement.ref_devis = lines[0]
                    paiement.ref_paiement = lines[1]
                    paiement.date_paiement = lines[2]
                    paiement.montant = cast_to_float(lines[3])
                    paiement.save()
                else:
                    error_line.append("error on line"+str(count) + " of paiement.csv")
            count += 1
    res = "".join(error_line)
    return res + "".join(fill_tables_paiement())
    

def fill_tables_devis():
    string_finition = """INSERT INTO finition(libelle, pourcentage) (SELECT DISTINCT finition, taux_finition from devis_temp) ON CONFLICT DO NOTHING"""
    string_lieu = """INSERT INTO lieu(libelle) (SELECT DISTINCT lieu from devis_temp) ON CONFLICT DO NOTHING"""
    string_client = """INSERT INTO utilisateurs(numero, role) (SELECT DISTINCT client, 10 FROM devis_temp) ON CONFLICT DO NOTHING"""
    string_devis = """INSERT INTO devis(date_debut_construction, date_devis, pourcentage, ref_devis, lieu, finition, client, type) 
        (SELECT 
        TO_DATE(d.date_debut, 'DD/MM/YYYY'), TO_DATE(d.date_devis, 'DD/MM/YYYY'), d.taux_finition, d.ref_devis, l.id_lieu, f.id_finition, u.id_utilisateur, t.id_type 
            FROM devis_temp d 
                JOIN utilisateurs u 
                    ON u.numero = d.client 
                JOIN lieu l 
                    ON l.libelle = d.lieu 
                JOIN finition f 
                    ON f.libelle = d.finition 
                JOIN type_maison t 
                ON t.libelle = d.type_maison) ON CONFLICT DO NOTHING"""
    string_update = "CALL update_devis()"
    string_delete = "TRUNCATE devis_temp"
    error = []
    with connection.cursor() as c:
        try:
            c.execute(string_finition)
        except Exception as e:
            error.append(f"Error executing {string_finition}: {e}")
        try:
            c.execute(string_lieu)
        except Exception as e:
            error.append(f"Error executing {string_lieu}: {e}")
        try:
            c.execute(string_client)
        except Exception as e:
            error.append(f"Error executing {string_client}: {e}")
        try:
            c.execute(string_devis)
        except Exception as e:
            error.append(f"Error executing {string_devis}: {e}")
        try:
            c.execute(string_update)
        except Exception as e:
            error.append(f"Error executing {string_update}: {e}")
        try:
            c.execute(string_delete)
        except Exception as e:
            error.append(f"Error executing {string_delete}: {e}")
    return error

def fill_tables_paiement():
    string_paiement = """INSERT INTO paiement(devis,ref_paiement,date_paiement,montant) 
        (SELECT d.id_devis, p.ref_paiement, TO_DATE(p.date_paiement, 'DD/MM/YYYY'), p.montant 
            FROM paiement_temp p 
                JOIN devis d
                    ON p.ref_devis = d.ref_devis)"""
    string_update = """UPDATE devis SET paiement_effectue = (
        select total 
            FROM v_total_payee_par_devis 
                WHERE devis = devis.id_devis) 
                    WHERE paiement_effectue = 0;"""
    string_delete = "TRUNCATE paiement_temp"
    error = []
    with connection.cursor() as c:
        try:
            c.execute(string_paiement)
        except Exception as e:
            error.append(f"Error executing {string_paiement}: {e}")
        try:
            c.execute(string_update)
        except Exception as e:
            error.append(f"Error executing {string_update}: {e}")
        try:
            c.execute(string_delete)
        except Exception as e:
            error.append(f"Error executing {string_delete}: {e}")
    return error

def fill_tables_travaux_maison():
    string_unite = "INSERT INTO unite(libelle) (SELECT DISTINCT unite FROM maison_temp)"
    string_type = "INSERT INTO type_maison(libelle, duree, description, surface) (SELECT DISTINCT type_maison, duree_travaux, description, surface  FROM maison_temp)"
    string_travaux = "INSERT INTO travaux(code, libelle, prix_unitaire, unite) (SELECT DISTINCT m.code_travaux, m.type_travaux , m.prix_unitaire , u.id_unite FROM maison_temp m join unite u on u.libelle = m.unite )"
    string_details = """INSERT INTO details_construction(type_maison, travaux, quantite) 
        (SELECT 
            type.id_type, tr.id_travaux, m.quantite 
                FROM maison_temp m 
                    JOIN travaux tr ON tr.libelle = m.type_travaux JOIN type_maison type ON type.libelle = m.type_maison) ON CONFLICT DO NOTHING"""
    string_delete = "TRUNCATE maison_temp"
    error = []
    with connection.cursor() as c:
        try:
            c.execute(string_unite)        
        except Exception as e:
            error.append(f"Error executing {string_unite}: {e}")
        
        try:
            c.execute(string_type)        
        except Exception as e:
            error.append(f"Error executing {string_type}: {e}")
        
        try:
            c.execute(string_travaux)        
        except Exception as e:
            error.append(f"Error executing {string_travaux}: {e}")
        
        try:
            c.execute(string_details)
        except Exception as e:
            error.append(f"Error executing {string_details}: {e}")
        
        try:
            c.execute(string_delete)
        except Exception as e:
            error.append(f"Error executing {string_delete}: {e}")
    return error