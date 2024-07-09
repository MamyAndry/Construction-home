--INSERT DETAIL DEVIS APRES INSEERTION DE NOUVEAU DEVIS
CREATE OR REPLACE FUNCTION insert_into_details_devis_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE format('INSERT INTO details_devis(travaux, devis, quantite, prix_unitaire) 
            SELECT travaux, devis, quantite, COALESCE(prix_unitaire, 0) 
            FROM v_details_devis 
            WHERE devis = %s', NEW.id_devis);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_insert_devis
AFTER INSERT ON devis
FOR EACH ROW
EXECUTE FUNCTION insert_into_details_devis_after_insert();


--UPDATE DENORMALISATION OF PAIEMENT EFFECTUE
CREATE OR REPLACE FUNCTION update_devis_after_deleting_paiement()
RETURNS TRIGGER AS $$
BEGIN
    EXECUTE format('UPDATE devis SET paiement_effectue = (
        devis.paiement_effectue - (SELECT montant FROM paiement WHERE id_paiement = %s)
        ) WHERE id_devis = %s', OLD.id_paiement, OLD.devis);

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_delete_paiement
BEFORE DELETE ON paiement
FOR EACH ROW
EXECUTE FUNCTION update_devis_after_deleting_paiement();

--PROCEDURE DE MISE A JOUR DEVIS
CREATE OR REPLACE PROCEDURE update_devis()
LANGUAGE plpgsql
AS $$
BEGIN

    UPDATE devis 
    SET prix_total = calculate_prix_total(devis.id_devis, devis.pourcentage) 
    WHERE prix_total = 0;

    UPDATE devis 
    SET date_fin_construction = 
        (SELECT (d.date_debut_construction + INTERVAL '1 day' * t.duree) AS date_fin  
        FROM devis d 
        JOIN type_maison t ON d.type = t.id_type 
        WHERE d.id_devis = devis.id_devis)
    WHERE date_fin_construction IS NULL;
END;
$$;


CREATE OR REPLACE FUNCTION calculate_prix_total(devis_id INTEGER, pourcentage DOUBLE PRECISION)
RETURNS NUMERIC AS $$
DECLARE
    temp NUMERIC;
BEGIN
    SELECT total INTO temp FROM v_montant_devis v WHERE devis = devis_id;
    RETURN ((temp * pourcentage) / 100) + temp;
END;
$$ LANGUAGE plpgsql;
    UPDATE devis SET paiement_effectue = (
            devis.paiement_effectue - (SELECT montant FROM paiement WHERE id_paiement = 48)
            ) WHERE id_devis = 2