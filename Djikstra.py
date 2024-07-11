def Djikstra(source,graphe):
    ''' calcule le pcc depuis la source vers tous les autres
        sommets de graphe.
        -> fait de ( One to All )
        -> retourne: l'arborescence de plus court chemin depuis source '''
    # Init l'ensemble des sommets deja traité 
    T={source}
    # D la liste contenat des tuples ( sommet "v" , distMin(source,v),pere(v) )
    # concraitement , D est la liste contenant l'arborce de pcc a partir de la source
    D=[(source,0.0,None)]
    infini = float("inf")
    
    for noeud in graphe.noeuds :
        if source.est_mon_voisin(noeud):
            # si l'arete (source,noeud) existe 
            D.append((noeud,source.distance(noeud),source))
        else:
            # si c'est pas son voisin ,alors "distance a Infinie" et "pere a None" 
            D.append((noeud,infini,None))
            
    # l'ensemble des sommets de graphe 
    V={v for v in graphe.noeuds }
    
    while T!=V:
        # choisir le noeud avec comme distance di minimale qui...
        #...n'est pas encore traité
        
        Dtemp=[(s,di,p) for (s,di,p) in D if  s not in T]
        Dtemp.sort(key=lambda x :x[1])
        noeud=Dtemp[0]
        # l'ajouter a la liste des noeud deja traité
        T.add(noeud[0])
        
        for v in noeud[0].mes_voisins():
            if v not in T :
                for (s,d,p) in D :
                    if s==v:
                        break
                nouvelleDist=noeud[0].distance(v)+noeud[1]
                # la distance est améliorer si elle est plus petite que d  
                if  nouvelleDist<d:
                    D[D.index((v,d,p))] = (v, nouvelleDist, noeud[0])

    return D
            
            