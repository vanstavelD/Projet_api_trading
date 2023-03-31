import sqlite3
import datetime


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

# MODIFIER LE PRIX D'UNE ACTION 
def modifier_prix_action(nouveau_prix, entreprise):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE action
                    SET prix = ?
                    WHERE entreprise = ?
                    """, (nouveau_prix, entreprise))
    connexion.commit()

modifier_prix_action(838.40, 'LVMH')


#ACHETER UNE ACTION
def ajouter_asso_action_user(prix_achat, utilisateur_id, action_id):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO asso_action_utilisateur
                    VALUES(NULL, ?, ?, NULL, NULL, ?, ?)
                    """,(prix_achat, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), utilisateur_id, action_id))
    connexion.commit()

#ajouter_asso_action_user(1, 'janvier', 5,6)


# SUPPRIMER UN ACHAT 
def supprimer_achat(achat_id):
        connexion = sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                        DELETE FROM asso_action_utilisateur
                        WHERE id = ?
                        """,(achat_id,))
        connexion.commit()


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


# LISTE DES ACTIONS DISPONIBLE

def list_action_disponible():
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor() 
        curseur.execute("""
                    SELECT * FROM action
                    """, ()) #on peut remplacer nom par * ie tout
        resultat = curseur.fetchall()
        connexion.close()
        return resultat



#VENDRE ACTION
def modifier_prix_date_vente(id, nouveau_prix_vente, nouveau_date_vente):
        connexion= sqlite3.connect("bdd.db")
        curseur = connexion.cursor()
        curseur.execute("""
                    UPDATE asso_action_utilisateur
                    SET prix_vente = ?,
                        date_vente =?
                    WHERE id = ?
                    """,(nouveau_prix_vente, nouveau_date_vente, id)) 

        connexion.commit()
        
# modifier_prix_date_vente(1, 66, 'juin')


################################### AUTHENTIFICATION ########################################


# Ce code permet d'obtenir le jeton JWT d'un utilisateur à partir de son email et de son mot de passe stockés dans une base de données
def obtenir_jwt_depuis_email_mdp(email:str, mdp:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM utilisateur WHERE email=? AND mdp=?
                    """, (email, mdp))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

# Ce code permet d'obtenir tous les utilisateurs stockés dans la base de données qui ont l'adresse e-mail spécifiée en entrée.
def get_users_by_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM utilisateur WHERE email=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat


# Cette fonction récupère l'ID de l'utilisateur correspondant à l'adresse e-mail donnée dans la base de données.
def get_id_user_by_email(email:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM utilisateur WHERE email=?
                    """, (email,))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat


# Cette fonction met à jour le jeton JWT d'un utilisateur dans la base de données en utilisant son identifiant et le nouveau jeton fourni en paramètres.
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
    


        

