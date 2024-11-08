import json

with open('match.json', 'r') as f:
    data = json.load(f)

def calculer_point(data1):
    point = {}
    
    for journee in data1["Journees"]:
        for match in journee["Matchs"]:
            equipe1 = match["club1"]
            equipe2 = match["club2"]
            gagnant = match["gagnant"]
            
            if equipe1 not in point:
                point[equipe1] = 0
            if equipe2 not in point:
                point[equipe2] = 0
            
            if gagnant == "nul":
                point[equipe1] +=1
                point[equipe2] +=1
            else:
                point[gagnant] +=3
    print(point)
