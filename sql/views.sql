CREATE OR REPLACE VIEW v_details_devis AS
    SELECT prest.id_travaux travaux, prest.libelle, prest.prix_unitaire, det.quantite, ty.duree, d.id_devis devis FROM devis d
        JOIN type_maison ty
            ON d.type = ty.id_type
        JOIN details_construction det
            ON det.type_maison = ty.id_type
        JOIN travaux prest
            ON prest.id_travaux = det.travaux;

CREATE OR REPLACE VIEW v_montant_devis AS
    SELECT SUM(prix_unitaire * quantite) as total, devis from v_details_devis
        GROUP BY devis;

CREATE OR REPLACE VIEW v_duree_total_devis AS
    SELECT SUM(duree) as duree, devis from v_details_devis
        GROUP BY devis;

CREATE OR REPLACE VIEW v_total_payee_par_devis AS
    SELECT devis, SUM(montant) total  FROM paiement 
        GROUP BY devis;

-- SELECT m.libelle, COALESCE(q.total, 0) montant 
--     from mois m LEFT JOIN 
--         (SELECT SUM(prix_total) total, extract('month' from date_devis) mois 
--             FROM devis WHERE extract('year' from date_devis) = %s 
--                 GROUP BY mois) q 
--             ON m.id_mois = q.mois
    
-- CREATE OR REPLACE VIEW v_details_devis_travaux_lib AS
--     SELECT v.devis, t.code, t.id_travaux,  t.libelle  from v_details_devis v
--         JOIN travaux p
--             ON p.id_travaux = v.travaux
--         JOIN travaux t
--             ON t.id_travaux = p.travaux;

