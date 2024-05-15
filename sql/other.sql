CREATE TABLE maison_temp(
    id SERIAL PRIMARY KEY,
    type_maison VARCHAR(50),
    description  VARCHAR(255),
    surface DOUBLE PRECISION,
    code_travaux  INTEGER,
    type_travaux  VARCHAR(100),
    unite  VARCHAR(50),
    quantite DOUBLE PRECISION,
    prix_unitaire DOUBLE PRECISION,
    duree_travaux INTEGER
)

CREATE TABLE devis_temp(
    id SERIAL PRIMARY KEY,
    client VARCHAR(50),
    ref_devis  VARCHAR(50),
    type_maison VARCHAR(50),
    finition  VARCHAR(50),
    taux_finition DOUBLE PRECISION,
    date_devis  VARCHAR(50),
    date_debut VARCHAR(50),
    lieu VARCHAR(255)
);

CREATE TABLE paiement_temp(
    id SERIAL PRIMARY KEY,
    ref_devis VARCHAR(50),
    ref_paiement  VARCHAR(50),
    date_paiement VARCHAR(50),
    montant DOUBLE PRECISION
);

SELECT DISTINCT extract('year' from date_devis) FROM devis;

SELECT SUM(prix_total) total, extract('month' from date_devis) mois
    FROM devis WHERE extract('year' from date_devis) = 2024 GROUP BY mois;

SELECT m.libelle, COALESCE(q.total, 0) from mois m
    left join (SELECT SUM(prix_total) total, extract('month' from date_devis) mois
    FROM devis WHERE extract('year' from date_devis) = 2024 GROUP BY mois) q
    ON m.id_mois = q.mois

INSERT INTO details_devis(travaux, devis, quantite, prix_unitaire) 
    (SELECT travaux, devis, quantite, prix_unitaire from v_details_devis WHERE devis LIKE 1); 

UPDATE devis SET date_fin_construction = (
    SELECT ( d.date_debut_construction + INTERVAL '1 day' * t.duree) date_fin
    FROM devis d
    JOIN type_maison t ON d.type = t.id_type WHERE id_devis = devis.id_devis
    )
WHERE date_fin_construction IS NULL;

UPDATE devis SET paiement_effectue = (
    select total FROM v_total_payee_par_devis WHERE devis = devis.id_devis
) WHERE paiement_effectue IS NULL;