import json
def stats():
    with open('match.json', 'r') as f:
        data = json.load(f)

    nom_du_club = input("Entrez le nom d'une équipe : ")

    def resultats_club(data, nom_du_club):
        resultat_club = []
        for journee in data['Journees']:
            for match in journee['Matchs']:
                if match['club1'] == nom_du_club or match['club2'] == nom_du_club:
                    resultat_club.append(match)
        return resultat_club

    def afficher_resultat(resultats):
        if not resultats:
            print("Aucun résultat trouvé pour ce club.")
        else:
            for resultat in resultats:
                print(f"{resultat['club1']} {resultat['score'][0]}-{resultat['score'][1]} {resultat['club2']} - Gagnant: {resultat['gagnant']}")

    resultat_club = resultats_club(data, nom_du_club)
    print(f"Resultat pour {nom_du_club} :")
    afficher_resultat(resultat_club)

stats()
