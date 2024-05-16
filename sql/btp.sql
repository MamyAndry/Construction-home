CREATE TABLE utilisateurs(
   id_utilisateur SERIAL,
   numero VARCHAR(50)  NOT NULL,
   email VARCHAR(50) ,
   mot_de_passe VARCHAR(100) ,
   role INTEGER NOT NULL DEFAULT 10,
   PRIMARY KEY(id_utilisateur),
   UNIQUE(numero)
);

CREATE TABLE type_maison(
   id_type SERIAL,
   duree DOUBLE PRECISION,
   libelle VARCHAR(50)  NOT NULL,
   description TEXT NOT NULL,
   surface DOUBLE PRECISION,
   PRIMARY KEY(id_type),
   UNIQUE(libelle)
);

CREATE TABLE finition(
   id_finition SERIAL,
   libelle VARCHAR(50)  NOT NULL,
   pourcentage DOUBLE PRECISION NOT NULL,
   PRIMARY KEY(id_finition),
   UNIQUE(libelle)
);

CREATE TABLE unite(
   id_unite SERIAL,
   libelle VARCHAR(50)  NOT NULL,
   PRIMARY KEY(id_unite),
   UNIQUE(libelle)
);

CREATE TABLE lieu(
   id_lieu SERIAL,
   libelle VARCHAR(100) ,
   PRIMARY KEY(id_lieu),
   UNIQUE(libelle)
);

CREATE TABLE mois(
   id_mois SERIAL,
   libelle VARCHAR(50)  NOT NULL,
   PRIMARY KEY(id_mois)
);

CREATE TABLE travaux(
   id_travaux SERIAL,
   code VARCHAR(50) ,
   libelle VARCHAR(100)  NOT NULL,
   prix_unitaire DOUBLE PRECISION,
   unite INTEGER NOT NULL,
   PRIMARY KEY(id_travaux),
   UNIQUE(libelle),
   FOREIGN KEY(unite) REFERENCES unite(id_unite)
);

CREATE TABLE devis(
   id_devis SERIAL,
   prix_total DOUBLE PRECISION DEFAULT 0,
   date_debut_construction DATE,
   date_fin_construction DATE,
   date_devis DATE,
   pourcentage  DOUBLE PRECISION DEFAULT 0,
   ref_devis VARCHAR(50) ,
   paiement_effectue DOUBLE PRECISION  DEFAULT 0,
   lieu INTEGER,
   finition INTEGER NOT NULL,
   client INTEGER NOT NULL,
   type INTEGER NOT NULL,
   PRIMARY KEY(id_devis),
   FOREIGN KEY(lieu) REFERENCES lieu(id_lieu),
   FOREIGN KEY(finition) REFERENCES finition(id_finition),
   FOREIGN KEY(client) REFERENCES utilisateurs(id_utilisateur),
   FOREIGN KEY(type) REFERENCES type_maison(id_type),
   UNIQUE(ref_devis)
);

CREATE TABLE paiement(
   id_paiement SERIAL,
   date_paiement DATE NOT NULL,
   montant DOUBLE PRECISION NOT NULL,
   ref_paiement VARCHAR(50) ,
   devis INTEGER NOT NULL,
   PRIMARY KEY(id_paiement),
   FOREIGN KEY(devis) REFERENCES devis(id_devis),
   UNIQUE(ref_paiement)
);


CREATE TABLE details_devis(
   id_details SERIAL PRIMARY KEY,   
   travaux INTEGER,
   devis INTEGER,
   quantite DOUBLE PRECISION,
   prix_unitaire DOUBLE PRECISION,
   FOREIGN KEY(travaux) REFERENCES travaux(id_travaux),
   FOREIGN KEY(devis) REFERENCES devis(id_devis)
);

CREATE TABLE details_construction(
   id_details SERIAL PRIMARY KEY,
   type_maison INTEGER,
   travaux INTEGER,
   quantite DOUBLE PRECISION,
   FOREIGN KEY(type_maison) REFERENCES type_maison(id_type),
   FOREIGN KEY(travaux) REFERENCES travaux(id_travaux)
);
