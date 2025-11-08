from pymongo import MongoClient
from datetime import datetime

mongo_client = MongoClient('mongodb://localhost:27017/')
db = mongo_client['test']

produits = db['produits']
clients = db['clients']
commandes = db['commandes']


def creer_commande():
    print("\n--- Créer une commande(Remplissez les infos demandees) ---")
    nom_client = input("Votre Nom et Prenom: ")
    nom_produit = input("Nom du produit souhaitee: ")
    quantite = int(input("Quantité de produit: "))
    
    client_doc = clients.find_one({"nom": nom_client})
    if not client_doc:
        print(" Client introuvable,Veuillez reessayer!")
        return
    
    produit = produits.find_one({"nom": nom_produit})
    if not produit:
        print(" Produit introuvable,Entrez le nom correcte!")
        return
    
    if produit['stock'] < quantite:
        print(f" Stock insuffisant! Le Stock disponible est : {produit['stock']}")
        return
    
    commande = {
        "client_id": client_doc['_id'],
        "produits": [{"nom": nom_produit, "quantite": quantite}],
        "date_commande": datetime.now(),
        "statut": "en cours",
        "montant_total": produit['prix'] * quantite
    }
    commandes.insert_one(commande)
    produits.update_one(
        {"nom": nom_produit},
        {"$inc": {"stock": -quantite}}
    )
    
    print("Votre commande est cree avec succes!")

def afficher_tous_produits():
    print("\n--- Tous les produits dispo chez nous ---")
    liste = list(produits.find())
    if not liste:
        print("Le produit que vous avez tape n est pas chez nous!")
        return
    for p in liste:
        print(f"Nom: {p['nom']}, Prix: {p['prix']} DH, Stock: {p['stock']}")

def rechercher_commandes():
    nom = input("Votre nom et prenom: ")
    client = clients.find_one({"nom": nom})
    if client:
        for c in commandes.find({"client_id": client['_id']}):
            print(f"Date: {c['date_commande']} - Statut: {c['statut']} - Total: {c['montant_total']} DH")

def rechercher_commandes_livrees():
    print("\n--- Commandes livrées ---")
    liste = list(commandes.find({"statut": "livrée"}))



def mettre_a_jour_produit():
    print("\n--- Modifier un produit ---")
    nom = input("Nom du produit que vous souhaitiez modifier: ")
    produit = produits.find_one({"nom": nom})
    
    if not produit:
        print(" Produit introuvable!")
        return
    
    nouveau_prix = float(input("Nouveau prix: "))
    produits.update_one({"nom": nom}, {"$set": {"prix": nouveau_prix}})
    print(" Prix modifie!")

def ajouter_champ_disponible():
    produits.update_many({}, {"$set": {"disponible": True}})
   





def supprimer_commande():
    print("\n--- Supprimer une commande ---")
    nom_client = input("Votre nom et prenom: ")
    nom_produit = input("Nom du produit: ")
    
    client_doc = clients.find_one({"nom": nom_client})
    if not client_doc:
        print(" Client introuvable!")
        return
    
    result = commandes.delete_one({
        "client_id": client_doc['_id'],
        "produits.nom": nom_produit
    })
    
    if result.deleted_count > 0:
        print("Votre commande est  supprimee!")
    else:
        print(" Aucune commande trouvee!")


def supprimer_commandes_client():
    print("\n--- Supprimer toutes les commandes d'un client ---")
    nom = input("Nom du client: ")
    client_doc = clients.find_one({"nom": nom})
    
    if not client_doc:
        print(" Client introuvable!")
        return
    
    result = commandes.delete_many({"client_id": client_doc['_id']})
    print(f"✓ {result.deleted_count} commande(s) supprimée(s)!")


def trier_commandes_par_date():
    print("\n--- Commandes triées par date ---")
    liste = list(commandes.find().sort("date_commande", -1))
    if not liste:
        print("Aucune commande trouvée!")
        return
    for c in liste:
        print(f"Date: {c['date_commande']}, Total: {c['montant_total']} DH")


def afficher_produits_disponibles():
    print("\n--- Produits disponibles ---")
    liste = list(produits.find({"stock": {"$gt": 0}}))
    if not liste:
        print("Aucun produit disponible!")
        return
    for p in liste:
        print(f"Nom: {p['nom']}, Stock: {p['stock']}")

def menu():
    while True:
        print("\n========== MENU ==========")
        print("1. Ajouter une commande")
        print("2. Afficher tous les produits")
        print("3. Afficher produits disponibles")
        print("4. Rechercher commande par client")
        print("5. Mettre à jour un produit")
        print("6. Supprimer une commande")
        print("7. Supprimer commandes d'un client")
        print("8. Afficher produits dispo")
        print("9. Trier commandes par date")
        print("10. Quitter")
        print("==========================")
        
        choix = input("Votre choix: ")
        
        if choix == "1":
            creer_commande()
        elif choix == "2":
            afficher_tous_produits()
        elif choix == "3":
            afficher_produits_disponibles()
        elif choix == "4":
            rechercher_commandes_client()
        elif choix == "5":
            mettre_a_jour_produit()
        elif choix == "6":
            supprimer_commande()
        elif choix == "7":
            supprimer_commandes_client()
        elif choix == "8":
            afficher_produits_disponibles()
        elif choix == "9":
            trier_commandes_par_date()
      
        elif choix == "10":
            print("Au revoir!")
            break
        else:
            print(" Choix invalide!")


if __name__ == "__main__":

    menu()

