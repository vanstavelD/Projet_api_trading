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
        
#ajouter_action('ATOL',255)


#ACHETER UNE ACTION
def ajouter_asso_action_user(prix_achat, date_achat, utilisateur_id, action_id ):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO asso_action_utilisateur
                    VALUES(NULL, ?, ?, ?, ?, ?, ?)
                    """,(prix_achat, date_achat, None , None, utilisateur_id, action_id ))

        connexion.commit()
#ajouter_asso_action_user(1, 'janvier', 5,6)


def ajouter_asso_user_suiveur(serveur_id, suivi_id ):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO asso_utilisateur_suiveur
                    VALUES(?, ?)
                    """,(serveur_id, suivi_id ))

        connexion.commit()
        
#ajouter_asso_user_suiveur(2,3)

######READ##############################################
def recuperer_list_action():
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor() 
        curseur.execute("""
                    SELECT * FROM action
                    """) #on peut remplacer nom par * ie tout
        resultat = curseur.fetchall()
        connexion.close()
        return resultat
        
#print(recuperer_list_action())

#UPDATE_PRIX_VENTE
def modifier_prix_date_vente(id, nouveau_prix_vente, nouveau_date_vente):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    UPDATE asso_action_utilisateur
                    SET prix_vente = ?,
                        date_vente =?
                    WHERE ID = ?
                    """,(nouveau_prix_vente, nouveau_date_vente, id)) 

        connexion.commit()
        
#modifier_prix_date_vente(1, 66, 'juin')

        

