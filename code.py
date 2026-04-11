import random
trafic=[]
def generate_random_traffic(n, scenario="normal"):
    for i in range(n):
        avions = {}  # ← ici, un nouveau dictionnaire à chaque itération
        
        fuel = random.randint(5, 50)
        medical =random.random() < 0.15
        technical_issue = medical = random.random() < 0.12
        diplomatic_level = random.randint(1, 5)
        
        if scenario == "medical_crisis":
            medical = random.random() < 0.3
        elif scenario == "technical_failure":
            technical_issue = random.random() < 0.25
        elif scenario == "fuel_crisis":
            fuel = random.randint(5, 15)
        elif scenario == "diplomatic_summit":
            diplomatic_level = random.randint(3, 5)
        
        avions["id"] = f"FL{i:03}"
        avions["fuel"] = fuel
        avions["medical"] = medical
        avions["technical_issue"] = technical_issue
        avions["diplomatic_level"] = diplomatic_level
        avions["arrival_time"] = round(19.40 + i * 0.01, 2)
        avions["score"] = 0 
        trafic.append(avions)
    
    return trafic
    
generate_random_traffic(10, scenario="normal") 

def check_avion(avion): # on crée une fonction qui va vérifier les infos de chaque avion.
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


def policy_carburant(avion,avion1):
    if avion["fuel"]<avion1["fuel"]:
        return True 
    else : 
        return False
    # plus le fuel d'un avion est faible plus il sera prioritaire

def policy_medical(avion,avion1):
    if avion["medical"] == True and avion1["medical"]==False:
        return True
    else:
        return False # si un avion n'a pas d'urgence medical, il est moins prioritaire


def policy_diplomatique(avion,avion1):
    if avion["diplomatic_level"]>avion1["diplomatic_level"]:
        return True
    else: 
        return False
        
def policy_technical(avion,avion1):
    if avion["technical_issue"] == True and avion1["technical_issue"]==False:
        return True
    else:
        return False 
 
def tri_selection_fuel(trafic):
    n = len(trafic)
    for i in range(0, n - 1):
        minimum = i
        for j in range(i + 1, n):
            if (policy_carburant(trafic[j], trafic[minimum]) or
               (trafic[j]["fuel"] == trafic[minimum]["fuel"] and
                trafic[j]["arrival_time"] < trafic[minimum]["arrival_time"])):
                minimum = j
        trafic[i], trafic[minimum] = trafic[minimum], trafic[i]
    return trafic
       
    return trafic

tri_selection_fuel(trafic)
for i in range ( len ( trafic ) ) : 
    trafic[i]["score"]+= 4*(len(trafic) - i) 
# pour le tri des problèmes, on associe un score à chaque problème : +le problème est important, + le score est enlevé.

print(trafic)
def tri_insertion_technique(trafic):
    for i in range(1, len(trafic)):
        avion_courant = trafic[i]
        j = i - 1
        while j >= 0 and (
            policy_technical(avion_courant, trafic[j]) or
            (avion_courant["technical_issue"] == trafic[j]["technical_issue"] and
             avion_courant["arrival_time"] < trafic[j]["arrival_time"])
        ):
            trafic[j + 1] = trafic[j]
            j -= 1
        trafic[j + 1] = avion_courant
    return trafic

tri_selection_technique(trafic)

for i in range ( len ( trafic ) ) : 
    trafic[i]["score"]+= 3*(len(trafic) - i) 

print(trafic) 

def tri_insertion_medical(trafic):
    for i in range(1, len(trafic)):
        avion_courant = trafic[i]
        j = i - 1
        while j >= 0 and (
            policy_medical(avion_courant, trafic[j]) or
            (avion_courant["medical"] == trafic[j]["medical"] and
             avion_courant["arrival_time"] < trafic[j]["arrival_time"])
        ):
            trafic[j + 1] = trafic[j]
            j -= 1
        trafic[j + 1] = avion_courant
    return trafic
    
tri_selection_medical(trafic)

for i in range ( len ( trafic ) ) : 
    trafic[i]["score"]+= 2*(len(trafic) - i) 

print(trafic) 

def tri_selection_diplomatique(trafic):
    n = len(trafic)
    for i in range(0, n - 1):
        maximum= i
        for j in range(i + 1, n):
            if (policy_diplomatique(trafic[j], trafic[maximum]) or
               (trafic[j]["diplomatic_level"] == trafic[maximum]["diplomatic_level"] and
                trafic[j]["arrival_time"] < trafic[maximum]["arrival_time"])):
                maximum = j
        trafic[i], trafic[maximum] = trafic[maximum], trafic[i]
    return trafic

tri_selection_diplomatique(trafic)
for i in range ( len ( trafic ) ) : 
    trafic[i]["score"]+= (len(trafic) - i) 
print(trafic)

def tri_selection_final(trafic): 
    n = len(trafic)
    for i in range(0, n-1):
        max= i
        for j in range(i+1, n):
            if trafic[j]["score"]>trafic[max]["score"]:
                max = j
        trafic[i],trafic[max]=trafic[max],trafic[i]
    return trafic
    
tri_selection_final(trafic)

for i in trafic : 
    print("L'avion :",i["id"], "va atterir" )
