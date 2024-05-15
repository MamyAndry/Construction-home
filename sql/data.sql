INSERT INTO utilisateurs VALUES 
    (default, 'RATSIBAZAFY', 'Mamisoa', '0344881819', 'email@email.com', 'mdp', 0);

INSERT INTO mois (libelle) VALUES 
    ('January'),
    ('February'),
    ('March'),
    ('April'),
    ('May'),
    ('June'),
    ('July'),
    ('August'),
    ('September'),
    ('October'),
    ('November'),
    ('December');

INSERT INTO unite VALUES
    (default, 'm2'),    
    (default, 'm3'),    
    (default, 'ftt');

INSERT INTO lieu VALUES
    (default, 'Imerintsiatosika'),
    (default, 'Ambohijanaka');

INSERT INTO type_maison VALUES  
    (default, 90, 'Tokyo', '4 chambres', 120),    
    (default, 50, 'Trano Bongo', '2 chambres', 100);

INSERT INTO finition VALUES
    (default, 'Standard', 3),
    (default, 'Gold', 5),
    (default, 'Premium', 7),
    (default, 'VIP', 10);

INSERT INTO travaux VALUES
    (default, '101', 'Decapage de plateforme', 3072.87, 1),
    (default, '202', 'Beton armee', 573215.8, 2);

INSERT INTO details_construction VALUES
    (default, 1, 1, 18.5),
    (default, 1, 2, 7.5),
    (default, 2, 1, 10.5),
    (default, 2, 2, 14.5); 