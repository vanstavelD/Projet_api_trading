import sqlite3

# CREER UN UTILISATEUR
def ajouter_utilisateur(nom, email, mdp, jwt ):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO utilisateur
                    VALUES(NULL, ?,?,?,?)
                    """,(nom, email, mdp, jwt))

        connexion.commit()
        
# ajouter_utilisateur('Dylan','dylan@gmail.com','dylan1234','123456789')

# SUPPRIMER UN UTILISATEUR
def supprimer_user(utilisateur_id):
        connexion = sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                        DELETE FROM utilisateur
                        WHERE id = ?
                        """,(utilisateur_id,))
        connexion.commit()

# supprimer_user(1)
        
# ACTION DISPONIBLE
def ajouter_action(entreprise, prix):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO action
                    VALUES(NULL, ?,?)
                    """,(entreprise, prix))

        connexion.commit()
        
# ajouter_action('ESSILORLUXOTTICA',164)


#ACHETER UNE ACTION
def ajouter_asso_action_user(utilisateur_id, action_id, prix_achat, date_achat):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO asso_action_utilisateur
                    VALUES(NULL, ?, ?, NULL, NULL, ?, ?)
                    """,(prix_achat, date_achat, utilisateur_id, action_id))
    connexion.commit()

#ajouter_asso_action_user(1, 'janvier', 5,6)

# SUIVRE UN USER
def ajouter_asso_user_suiveur(suiveur_id, suivi_id ):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    INSERT INTO asso_utilisateur_suiveur
                    VALUES(?, ?)
                    """,(suiveur_id, suivi_id ))

        connexion.commit()
        
# ajouter_asso_user_suiveur(2,1)

# SE DESABONNER
def desabonner_user(suiveur_id, suivi_id):
        connexion = sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                        DELETE FROM asso_utilisateur_suiveur
                        WHERE suiveur_id = ? AND suivi_id = ?
                        """,(suiveur_id,suivi_id))
        connexion.commit()

# desabonner_user(1,2)

######READ##############################################

#PORTEFOLIO
def recuperer_list_action(utilisateur_id: int):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor() 
        curseur.execute("""
                    SELECT * FROM action
                    INNER JOIN asso_action_utilisateur ON action.id = asso_action_utilisateur.action_id
                    WHERE asso_action_utilisateur.utilisateur_id = ?
                    """, (utilisateur_id,)) #on peut remplacer nom par * ie tout
        resultat = curseur.fetchall()
        connexion.close()
        return resultat
        
#print(recuperer_list_action())

#UPDATE_PRIX_VENTE   VENDRE ACTION
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


################################### AUTHENTIFICATION ########################################

def obtenir_jwt_depuis_email_mdp(email:str, mdp:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM utilisateur WHERE email=? AND mdp=?
                    """, (email, mdp))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

def get_users_by_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM utilisateur WHERE email=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

def get_id_user_by_email(email:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM utilisateur WHERE email=?
                    """, (email,))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

def update_token(id, token:str)->None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE utilisateur
                        SET jwt = ?
                        WHERE id=?
                    """,(token, id))
    connexion.commit()
    connexion.close()
    
    


        

