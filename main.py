from fastapi import FastAPI, HTTPException, Request, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import crud
from jose import jwt
import hashlib


# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Fonctions utiles :

# La fonction hasher_mdp(mdp) utilise l'algorithme de hachage SHA256 pour crypter un mot de passe en une chaîne de caractères hexadécimaux.
def hasher_mdp(mdp):
    return hashlib.sha256(mdp.encode()).hexdigest()

# La variable pwd_context est initialisée en utilisant la librairie passlib pour la gestion de mots de passe en utilisant l'algorithme de cryptage Bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# La fonction verify_password(plain_password, hashed_password) prend un mot de passe en clair et le mot de passe crypté, elle renvoie True si le mot de passe en clair correspond au mot de passe crypté, False sinon.
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# La fonction get_password_hash(password) prend un mot de passe en clair, l'encrypte avec l'algorithme Bcrypt et renvoie l'encrypted password.
def get_password_hash(password):
    return pwd_context.hash(password)

# Modèles pour les requêtes POST :
# Ces modèles servent à valider les données envoyées dans les requêtes POST et à les transformer en objets Python.

class UserCreate(BaseModel):
    nom: str
    email: str
    mdp: str

class UserConnexion(BaseModel):
    email: str
    mdp: str

class ActionCreate(BaseModel):
    entreprise: str
    prix: float

class AchatAction(BaseModel):
    prix_achat: float
    date_achat: str
    utilisateur_id: int
    action_id: int

class VenteAction(BaseModel):
    id: int
    prix_vente: float
    date_vente: str
    

class SuivreUser(BaseModel):
    suiveur_id: int
    suivi_id: int

class Desabonnement(BaseModel):
    suiveur_id: int
    suivi_id: int

class DeleteUser(BaseModel):
    utilisateur_id: int
    
class DeleteAchat(BaseModel):
    achat_id: int

# Initialisation de l'application :
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/test")
async def test():
    liste = [i for i in range(100) if i%5==0]
    return {"liste des multiples de 5 :"}

# Ce code crée un nouvel utilisateur en utilisant les informations fournies dans la requête POST et stocke ces informations dans une base de données.
@app.post("/user/")
def creer_utilisateur(user: UserCreate):
    user_dict = user.dict()
    user_dict["mdp"] = get_password_hash(user_dict["mdp"]) # Cette ligne utilise la fonction get_password_hash pour hasher le mot de passe de l'utilisateur, puis met à jour la valeur du mot de passe dans le dictionnaire user_dict.
    jwt_token = jwt.encode({"sub": user_dict["email"]}, SECRET_KEY, algorithm=ALGORITHM)
    crud.ajouter_utilisateur(user_dict["nom"], user_dict["email"], user_dict["mdp"], jwt_token)
    return {"message": "Utilisateur créé"}

@app.post("/user/connexion/")
def connexion_utilisateur(user: UserConnexion):
    user_dict = user.dict()
    user_enregistre = crud.get_users_by_mail(user_dict["email"])
    if not user_enregistre:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    user_enregistre = user_enregistre[0]
    jwt_token = jwt.encode({"sub": user_enregistre[1]}, SECRET_KEY, algorithm=ALGORITHM)
    crud.update_token(user_enregistre[0], jwt_token)
    return {"jwt_token": jwt_token}



# AJOUTER UNE ACTION
# @app.post("/action/")
# def ajouter_action(action: ActionCreate):
#     action_dict = action.dict()
#     crud.ajouter_action(action_dict["entreprise"], action_dict["prix"])
#     return {"message": "Action ajoutée"}

# ACHETER UNE ACTION
@app.post("/achat-action/")
async def achat_action(achat: AchatAction, req: Request):
    achat_dict = achat.dict()
    crud.ajouter_asso_action_user(achat_dict["prix_achat"], achat_dict["date_achat"], achat_dict["utilisateur_id"], achat_dict["action_id"])
    return {"message": "Action achetée"}


# VENDRE ACTION
@app.put("/asso-action-utilisateur/")
def modifier_prix_date_vente(vendre: VenteAction):
    vendre_dict = vendre.dict()
    crud.modifier_prix_date_vente(vendre_dict["id"], vendre_dict["prix_vente"], vendre_dict["date_vente"])
    return {"message": "Action vendu"}


# SUIVRE UN USER 
@app.post("/suivre/")
def suivre_user(suivre: SuivreUser):
    suivre_dict = suivre.dict()
    crud.ajouter_asso_user_suiveur(suivre_dict["suiveur_id"], suivre_dict["suivi_id"])
    return {"message": "Abonnement ajouté"}

# DESABONNEMENT 
@app.delete("/desabonnement/")
def desabonner_user(desabonnement: Desabonnement):
    desabonnement_dict = desabonnement.dict()
    crud.desabonner_user(desabonnement_dict["suiveur_id"], desabonnement_dict["suivi_id"])
    return {"message": "Abonnement supprimé"}

# LISTE DES ACTIONS DISPONIBLES 
@app.get("/actions/")
def get_actions():
    actions = crud.list_action_disponible()
    actions_list = []
    for action in actions:
        action_dict = {"id": action[0], "entreprise": action[1], "prix": action[2]}
        actions_list.append(action_dict)
    return {"actions": actions_list}


# VOIR LA LISTE DES ACTIONS PAR UTILISATEUR
@app.get("/actions-utilisateur/{utilisateur_id}")
def get_actions_utilisateur(utilisateur_id: int):
    actions_utilisateur = crud.recuperer_list_action(utilisateur_id)
    actions_list = []
    for action in actions_utilisateur:
        action_dict = {"id": action[0], "entreprise": action[1], "prix": action[2]}
        actions_list.append(action_dict)
    return {"actions": actions_list}


# SUPPRIMER USER
# @app.delete("/delete_user/")
# def supprimer_user(delete_user: DeleteUser):
#     delete_user_dict = delete_user.dict()
#     crud.supprimer_user(delete_user_dict["utilisateur_id"])
#     return {"message": "Utilisateur supprimé"}

# SUPPRIMER UN ACHAT
@app.delete("/delete_achat-action/")
def supprimer_achat(delete_achat: DeleteAchat):
    delete_achat_dict = delete_achat.dict()
    crud.supprimer_achat(delete_achat_dict["achat_id"])
    return {"message": "Achat supprimé"}