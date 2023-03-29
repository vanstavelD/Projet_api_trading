import sqlite3

def ajouter_utilisateur(nom, email, mdp):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO utilisateur
                    VALUES(NULL, ?,?,?)
                    """,(nom, email, mdp))

        connexion.commit()
        
#ajouter_utilisateur('Dylan','dylan@gmail.com','dylan1234')

def ajouter_action(entreprise, prix):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO action
                    VALUES(NULL, ?,?)
                    """,(entreprise, prix))

        connexion.commit()
        
#ajouter_action('ATOL','lunettes')

def ajouter_asso_action_user(prix_achat, date_achat, utilisateur_id, action_id ):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO asso_action_utilisateur
                    VALUES(NULL, ?, ?, ?, ?, ?, ?)
                    """,(prix_achat, date_achat, None , None, utilisateur_id, action_id ))

        connexion.commit()
#ajouter_asso_action_user(1, 'janvier', 2, 'fev', 5,6)


def ajouter_asso_user_suiveur(serveur_id, suivi_id ):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO asso_utilisateur_suiveur
                    VALUES(?, ?)
                    """,(serveur_id, suivi_id ))

        connexion.commit()
        
#ajouter_asso_user_suiveur(2,3)
        

        

