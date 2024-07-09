CREATE OR REPLACE VIEW v_data_warehouse AS
    SELECT
        d.prix_total,
        d.date_debut_construction,
        d.date_fin_construction,
        d.date_devis,
        d.ref_devis,
        dd.quantite, 
        tr.code code_travaux,
        tr.libelle travaux  ,          
        tr.prix_unitaire prix_unitaire_travaux,
        un.libelle unite,
        l.libelle lieu,
        f.libelle finition,
        f.pourcentage pourcentage_finition,
        c.numero,
        ty.duree,
        ty.libelle type_maison,
        ty.description,
        ty.surface,
        d.pourcentage,
        p.date_paiement,
        p.montant,
        p.ref_paiement
        FROM 
            devis d
            JOIN details_devis dd
                ON d.id_devis = dd.devis
            JOIN travaux tr
                ON tr.id_travaux = dd.travaux
            JOIN unite un
                ON un.id_unite = tr.unite
            JOIN paiement p
                ON d.id_devis = p.devis
            JOIN finition f
                ON d.finition = f.id_finition
            JOIN utilisateurs c
                ON d.client = c.id_utilisateur
            JOIN type_maison ty
                ON d.type = ty.id_type
            JOIN lieu l
                ON d.lieu = l.id_lieu;
