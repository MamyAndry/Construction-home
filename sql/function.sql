CREATE OR REPLACE FUNCTION insert_into_details_devis_after_insert()
RETURNS TRIGGER AS $$
BEGIN
    -- Execute the query to insert into details_devis
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

CREATE OR REPLACE FUNCTION calculate_prix_total(devis_id INTEGER, pourcentage DOUBLE PRECISION)
RETURNS NUMERIC AS $$
DECLARE
    temp NUMERIC;
BEGIN
    -- Fetch the total from v_montant_devis for the given devis_id
    SELECT total INTO temp FROM v_montant_devis v WHERE devis = devis_id;

    -- Calculate the prix_total based on the fetched total and the pourcentage passed as an argument
    RETURN ((temp * pourcentage) / 100) + temp;
END;
$$ LANGUAGE plpgsql;

