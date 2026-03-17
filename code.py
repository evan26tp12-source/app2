Trafic_initial=[]
def check_avion(avion): # on crée une fonction qui va vérifier les infos de chqua avion.
    acquis = ["id","arrival_time","diplomatic_level","fuel","medical","technical_issue"] # on définit tous les paramètres a analyser
# on va vérifier si chaque avion possède toutes les données necessaires
    for champ in acquis: 
        if champ not in avion:
            print(f"[ERREUR] Champ manquant : {champ} dans {avion}") #si l'avion ne possède pas toutes les données nécessaire on dit qu'il y a un problème et on dit quelle est l'information qu'il manque.
            return False 

    return True # Si l'avion possède toutes les données on retourne true

   
def load_trafic(data):
    valide = [] # on crée une liste qui va garder seulement les avions qui ont toutes leur données
    for avion in data:# on parcour la liste d'avions complète contenu dans notre variable data
        if check_avion(avion) == True: # on vérifie les avions qui ont toutes les données nécessaire
            valide.append(avion) # ceux qui ont toutes leur données sont ajouté dans la liste des avions "valide"
    return valide

    # on affiche tous les avions avec leurs données
def info_avion(trafic):

    for avion in trafic:
        print("ID :", plane["id"])
        print("Carburant :", plane["fuel"])
        print("Urgence médicale :", plane["medical"])
        print("Incident technique :", plane["technical_issue"])
        print("Importance diplomatique :", plane["diplomatic_level"])
        print("Heure d'arrivée :", plane["arrival_time"])



def policy_carburant(avion):
    return avion["fuel"]# plus le fuel d'un avion est faible plus il sera prioritaire


def policy_medical(avion):
    if avion["medical"] == True:
        return 0
    else:
        return 1 # si un avion n'a pas d'urgence medical, il est moins prioritaire


def policy_diplomatique(avion):
    niveau = avion["diplomatic_level"] #plus le niveau diplomatique est éleve, plus l'avion est prioritaire
    priorite = -niveau
    return priorite



def tri_selection(trafic, policy): # on prend en paramètre la liste de tous les avion et l'ordre de priorite
    trafic_copy = trafic.copy()  # on effectue une copie de la liste de base pour la garder comme tel
    n = len(trafic_copy) #pour savoir le nombre d'avion

    for i in range(n): 
        index_min = i #on dit que l'avion le plus prioritaire est a l'indice i
