import random

def pp(s,visi):
    ''' procedure parcours en profondeur (pp) ,
    prend comme argument :
    sommet de depart ,dictionnaire {sommet:booleén(visite ou non)}
    -> fait le pp a partir de s 
    '''
    visi[s]=True 
    for (v,_) in s.voisins:
        if not visi[v]:
            pp(v,visi)

def connexe(graphe):
    ''' argument:graphe en question --> True si Connexe ,False sinon 
    ->si tous les sommets du réseau ont été visités cela signifie que le
    réseau est connexe.Sinon, cela signifie qu'il existe au moins un sommet qui n'est pas accessible à
    partir du sommet de départ choisi, cad le réseau est non connexe.
'''
    # initialisation de tt les sommets a Non Vu(non visité :) 
    visites={noeud:False for noeud in graphe.noeuds}
    # le sommet de depart tiré aleat 
    x=random.randint(0,len(graphe.noeuds)-1)
    sommet_depart=graphe.noeuds[x]
    # lancer le pp
    pp(sommet_depart,visites)
    return all(visites.values())# voir si tout les sommet ont ete visité ou non 
