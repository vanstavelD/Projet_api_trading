import sqlite3

connexion= sqlite3.connect("bdd.db")
curseur = connexion.cursor()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS utilisateur ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                email TEXT NOT NULL,
                mdp TEXT NOT NULL
                )
                """)

connexion.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS action ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entreprise TEXT NOT NULL,
                prix FLOAT
                )
                """)

connexion.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS asso_action_utilisateur ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prix_achat FLOAT,
                date_achat TEXT NOT NULL,
                prix_vente FLOAT,
                date_vente TEXT,
                utilisateur_id INTEGER,
                action_id  INTEGER,
                FOREIGN KEY(utilisateur_id) REFERENCES utilisateur(id),
                FOREIGN KEY(action_id) REFERENCES action(id)
                )
                """)

connexion.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS asso_utilisateur_suiveur ( 
                suiveur_id INTEGER,
                suivi_id  INTEGER,
                FOREIGN KEY(suiveur_id) REFERENCES utilisateur(id),
                FOREIGN KEY(suivi_id) REFERENCES utilisateur(id)
                )
                """)

connexion.commit()
#################################################################################

