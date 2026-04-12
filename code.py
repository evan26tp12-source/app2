import random

trafic = []

def generate_random_traffic(n, scenario="normal"):
    for i in range(n):
        avions = {}  # Nouveau dictionnaire pour chaque avion

        # Génération des caractéristiques de base de l'avion
        fuel = random.randint(5, 50)
        medical = random.random() < 0.15          # 15% de chance d'urgence médicale
        technical_issue = random.random() < 0.12  # 12% de chance de panne technique
        diplomatic_level = random.randint(1, 5)

        # Modification des probabilités selon le scénario choisi
        if scenario == "medical_crisis":
            medical = random.random() < 0.3       # Plus d'urgences médicales
        elif scenario == "technical_failure":
            technical_issue = random.random() < 0.25  # Plus de pannes
        elif scenario == "fuel_crisis":
            fuel = random.randint(5, 15)           # Carburant très bas pour tous
        elif scenario == "diplomatic_summit":
            diplomatic_level = random.randint(3, 5)   # Niveaux diplomatiques élevés

        # Remplissage du dictionnaire de l'avion
        avions["id"] = f"FL{i:03}"
        avions["fuel"] = fuel
        avions["medical"] = medical
        avions["technical_issue"] = technical_issue
        avions["diplomatic_level"] = diplomatic_level
        avions["arrival_time"] = round(19.40 + i * 0.01, 2)
        avions["score"] = 0  # Score de priorité, calculé plus tard

        trafic.append(avions)
    return trafic


generate_random_traffic(100, scenario="normal")


def check_avion(avion):
    # Liste des champs obligatoires pour qu'un avion soit valide
    acquis = ["id", "arrival_time", "diplomatic_level", "fuel", "medical", "technical_issue"]

    # Vérification que chaque champ est bien présent dans le dictionnaire de l'avion
    for champ in acquis:
        if champ not in avion:
            print(f"[ERREUR] Champ manquant : {champ} dans {avion}")
            return False

    return True  # L'avion est complet


def load_trafic(data):
    valide = []  # Contiendra uniquement les avions avec toutes leurs données

    for avion in data:
        if check_avion(avion) == True:
            valide.append(avion)  # On ne garde que les avions valides
    return valide


def info_avion(trafic):
    # Affichage des informations de chaque avion
    for avion in trafic:
        print("ID :", avion["id"])
        print("Carburant :", avion["fuel"])
        print("Urgence médicale :", avion["medical"])
        print("Incident technique :", avion["technical_issue"])
        print("Importance diplomatique :", avion["diplomatic_level"])
        print("Heure d'arrivée :", avion["arrival_time"])


# --- POLITIQUES DE PRIORITÉ ---
# Chaque fonction compare deux avions et retourne True si le premier est plus prioritaire

def policy_carburant(avion, avion1):
    # Un avion avec moins de carburant est plus urgent
    if avion["fuel"] < avion1["fuel"]:
        return True
    else:
        return False


def policy_medical(avion, avion1):
    # Un avion avec urgence médicale passe devant un avion sans urgence
    if avion["medical"] == True and avion1["medical"] == False:
        return True
    else:
        return False


def policy_diplomatique(avion, avion1):
    # Un avion avec un niveau diplomatique plus élevé est prioritaire
    if avion["diplomatic_level"] > avion1["diplomatic_level"]:
        return True
    else:
        return False


def policy_technical(avion, avion1):
    # Un avion avec une panne technique passe devant un avion sans panne
    if avion["technical_issue"] == True and avion1["technical_issue"] == False:
        return True
    else:
        return False


# TRIS ET ATTRIBUTION DES SCORES 
# Chaque critère est trié puis un score est attribué selon la position dans la liste.
# Les poids sont : carburant x4, technique x3, médical x2, diplomatique x1

def tri_selection_fuel(trafic):
    # Tri par carburant croissant (le moins de carburant = le plus prioritaire)
    # En cas d'égalité, on trie par heure d'arrivée
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


tri_selection_fuel(trafic)

# Attribution des scores selon la position après tri carburant (poids x4)
for i in range(len(trafic)):
    trafic[i]["score"] += 4 * (len(trafic) - i)


def tri_insertion_technique(trafic):
    # Tri par panne technique : les avions en panne passent en premier
    # En cas d'égalité, on trie par heure d'arrivée
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


tri_insertion_technique(trafic)

# Attribution des scores selon la position après tri technique (poids x3)
for i in range(len(trafic)):
    trafic[i]["score"] += 3 * (len(trafic) - i)


def tri_insertion_medical(trafic):
    # Tri par urgence médicale : les avions avec urgence passent en premier
    # En cas d'égalité, on trie par heure d'arrivée
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


tri_insertion_medical(trafic)

# Attribution des scores selon la position après tri médical (poids x2)
for i in range(len(trafic)):
    trafic[i]["score"] += 2 * (len(trafic) - i)


def tri_selection_diplomatique(trafic):
    # Tri par niveau diplomatique décroissant (le plus haut niveau = le plus prioritaire)
    # En cas d'égalité, on trie par heure d'arrivée
    n = len(trafic)
    for i in range(0, n - 1):
        maximum = i
        for j in range(i + 1, n):
            if (policy_diplomatique(trafic[j], trafic[maximum]) or
                (trafic[j]["diplomatic_level"] == trafic[maximum]["diplomatic_level"] and
                 trafic[j]["arrival_time"] < trafic[maximum]["arrival_time"])):
                maximum = j
        trafic[i], trafic[maximum] = trafic[maximum], trafic[i]
    return trafic


tri_selection_diplomatique(trafic)

# Attribution des scores selon la position après tri diplomatique (poids x1)
for i in range(len(trafic)):
    trafic[i]["score"] += (len(trafic) - i)


def tri_selection_final(trafic):
    # Tri final par score décroissant : l'avion avec le score le plus élevé atterrit en premier
    n = len(trafic)
    for i in range(0, n - 1):
        maximum= i
        for j in range(i + 1, n):
            if trafic[j]["score"] > trafic[maximum]["score"]:
                maximum = j
        trafic[i], trafic[maximum] = trafic[maximum], trafic[i]
    return trafic


tri_selection_final(trafic)


def simulation(trafic):
    """
    Simule l'atterrissage des avions un par un.
    À chaque tour, l'avion en tête de liste atterrit,
    et le carburant des autres diminue de 1.
    Si un avion atteint fuel <= 0 avant d'atterrir, il crashe.
    """
    sauves = []
    crashes = []
    file = trafic.copy()  # On travaille sur une copie pour ne pas modifier l'original

    tour = 1
    while len(file) > 0:
        print("Tour numéro :", tour)

        # Détection des avions à court de carburant avant l'atterrissage
        crashs_ce_tour = []
        for a in file:
            if a["fuel"] <= 0:
                crashs_ce_tour.append(a)

        # Suppression des avions crashés de la file
        for avion in crashs_ce_tour:
            print("L'avion :", avion["id"], " s'est crashé")
            crashes.append(avion)
            file.remove(avion)

        if not file:
            break

        # L'avion en tête de file atterrit
        avion_qui_atterrit = file.pop(0)
        print("L'avion :", avion_qui_atterrit["id"], " a atterri\n")
        sauves.append(avion_qui_atterrit)

        # Consommation de carburant pour les avions encore en attente
        for avion in file:
            avion["fuel"] -= 1

        tour += 1

    # Affichage du bilan final
    print("BILAN\n")
    print(" Avions sauvés  :", len(sauves), "\n")
    for a in sauves:
        print(a['id'], "\n")
    print(" Avions crashés :", len(crashes), "\n")
    for a in crashes:
        print(a['id'], "\n")


simulation(trafic)
