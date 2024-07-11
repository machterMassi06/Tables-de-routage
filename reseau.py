import random
import connexite
import networkx as nx
import matplotlib.pyplot as plt
import Djikstra

class Noeud:
    ''' cette classe modelise les objets qui sont des noeuds (sommets)'''
    
    def __init__(self, identifiant,tier2=False):
        ''' notre graphe il est Non oriente donc on parle de liste des voisins d'un noeud '''
        self.id = identifiant # numero de noeud 
        self.estTier2=tier2
        self.voisins = []
        self.table_routage = {}
    
    # les deux methodes suivantes sont implementés afin de pouvoir mettre des objets 'Noeud' comme clé de dictionnaire  
    def __hash__(self):
        '''Fournit le hachage pour l'objet Noeud'''
        return hash(self.id)

    def __eq__(self, autrenoeud):
        '''Vérifie si deux objets Noeud sont égaux : sont egaux si il ont le meme id '''
        if isinstance(autrenoeud, type(self)):
            return self.id == autrenoeud.id
        return False
    
    def ajouter_voisin(self, voisin, temps_communication):
        ''' permet l'ajout d'un noeud voisin ainsi que le poid de l'arete
        dans la liste des voisins '''
        
        self.voisins.append((voisin, temps_communication))

    def distance(self,noeud):
        ''' retourne la distance entre ce sommet(self) et son voisin(noeud)'''

        for voisin,temps_communication in self.voisins:
            if voisin == noeud:
                return temps_communication
    
    def mes_voisins(self):
        ''' return la liste des voisins '''
        if self.voisins : 
            voisins,_=zip(*self.voisins)#unzip list(v,w)
        else:
            voisins=[]
        return list(voisins)
    
    def est_mon_voisin(self,noeud):
        ''' verifié si un noeud donné est un voisin '''
        
        for voisin,t in self.voisins:
            if noeud == voisin:
                return True
        return False
    
    def nb_voisins_tier2(self):
        ''' retourne le nombre de voisins qui sont tier2 '''
        
        return len([ v for v in self.mes_voisins() if v.estTier2==True])

class Graphe:
    ''' cette classe modelise des objets graphe '''
    
    def __init__(self):
        ''' le graphe est represente par la liste de ses noeuds ( instances de classe Noeud)'''
        self.noeuds = []

    def ajouter_noeud(self, noeud):
        ''' ajout d'un noeud dans la liste des noeuds '''
        self.noeuds.append(noeud)

    def generer_reseau(self):
        ''' Generation de resaux d’interconnexion d'un graphe de 100 noeuds,
        - Les liens et les temps de communication sur chacun de ces liens vont etre
        crees de maniere aleatoire selon des regles donné (voir sujet)'''
        
        # Génération du backbone (Tier 1)
        
        backbone = [Noeud(i) for i in range(1,11)]
        for i in range(len(backbone)):
            for j in range(i+1, len(backbone)):
                if random.random() < 0.75:  # 75% de chance de création du lien
                    temps_communication = random.randint(5, 10)
                    backbone[i].ajouter_voisin(backbone[j], temps_communication)
                    backbone[j].ajouter_voisin(backbone[i], temps_communication)

        # Génération des opérateurs de niveau 2 (Tier 2) 20 operateurs
                    
        tier2 = [Noeud(i,True) for i in range(11, 31)]
        for noeud2 in tier2:
            # Connecter à 1 ou 2 nœuds du backbone
            # tiré aleatoirement 
            x_backbone=random.randint(1,2)
            while x_backbone>0:
                j=random.randint(0,9)
                if not(noeud2.est_mon_voisin(backbone[j])):
                    temps_communication = random.randint(10, 20)
                    noeud2.ajouter_voisin(backbone[j], temps_communication)
                    backbone[j].ajouter_voisin(noeud2, temps_communication)
                    x_backbone-=1
                    
            # on tire 2 ou 3 operateurs niv 2 aleatoirement 
            x_tier2=random.randint(2,3)
            
            while noeud2.nb_voisins_tier2()<x_tier2:
                j=random.randint(0,19)
                # si le noeud n'est pas deja son voisin (graphe simple);
                # la derniere condition pour eviter les boucle (s,s)
                if not noeud2.est_mon_voisin(tier2[j]) and  tier2[j].nb_voisins_tier2()<3 and tier2[j]!=noeud2:
                    temps_communication = random.randint(10, 20)
                    noeud2.ajouter_voisin(tier2[j], temps_communication)
                    tier2[j].ajouter_voisin(noeud2, temps_communication)
        
        
        # Génération des opérateurs de niveau 3 (Tier 3)
        tier3=[Noeud(i) for i in range(31,101)]
        for noeud3 in tier3:
            # relié l'operateur tier3 a 2 opé tier2 tiré aleat 
            # avec des lien evalué entre 20 et 50 
            while len(noeud3.mes_voisins())<2:
                j=random.randint(0,19)
                if not(noeud3.est_mon_voisin(tier2[j])):
                    temps_communication = random.randint(20,50) # evaluation de l'arete
                    tier2[j].ajouter_voisin(noeud3, temps_communication)
                    noeud3.ajouter_voisin(tier2[j], temps_communication)

        # Ajout des nœuds(tous les operateurs) au graphe
        self.noeuds=backbone+tier2+tier3

                
                
    def generer_tables_routage(self):
        ''' Methode qui lance en chaque noeud le calcule des tables de routages des noeuds de graphe.
            --> calcule la table de routage d’un noeud pour chaque destination possible (les 99 autres noeuds),
            en utilisant biensur Djikstra pour avoir le plus court chemin en temps de communication'''
        
        
        for source in self.noeuds:
            # recuperer l'arborescence de pcc depuis noeud source
            resultats_dijkstra = Djikstra.Djikstra(source, self)
            
            table_routage = {}
            
            for info in resultats_dijkstra:
                # info un tuple contient (noeud, distance, pere)
                if info[0] != source: 
                    destination = info[0] # distination
                    distanceMin=info[1] # distance min en unites 
                    pere = info[2] 
                    chemin=[]
                    while pere != source:
                        chemin.append(pere)
                        pere = [x[2] for x in resultats_dijkstra if x[0] == pere][0]
                        
                    if chemin!=[]:
                        table_routage[destination] = (chemin[-1],distanceMin)# Le prochain nœud à atteindre
                    else:
                        # donc le pc chemin c'est l'arete directe entre eux 
                        table_routage[destination] = ("fin",distanceMin)
            source.table_routage = table_routage
            
    def reconstruire_chemin(self,source, destination):
        ''' methode de reconstruction de chemin entre une source et une destionation de message.
            Rq: la reconstitution de chemin se fait sans refaire le calcul de plus court chemin
            mais juste en exploitant les tables de routage deja etablies'''
        
        distanceMin=source.table_routage.get(destination)[1]
        chemin = [source.id]
        noeud_actuel = source

        while noeud_actuel != destination:
            if noeud_actuel.table_routage.get(destination)[0] == "fin":
                break
            prochain_noeud = noeud_actuel.table_routage[destination][0]
            chemin.append(prochain_noeud.id)
            noeud_actuel = prochain_noeud

        chemin.append(destination.id)
        return chemin,distanceMin
    
    def main(self):
        '''    Methode principale Main 
            elle nous permette de generer le reseau de 100 noeuds et voir si il connexe , si
            c'est le cas alors on lance le calcule des tables de routages,sinon on genere un autre
            reseau '''
        self.generer_reseau()
        while connexite.connexe(self)==False:
            # generer un autre reseau aleatoire si il n'est pas connexe
            self.generer_reseau()
            
        # reseau connexe ,on lance le calcule des tables de routage    
        self.generer_tables_routage()
        


    
    