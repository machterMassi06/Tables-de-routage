import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk # juste pour creer une fenetre et des champs de saisie 
import reseau
# vous avez qu'a exucuter ce module

class Application:
    def __init__(self, master):
        self.master = master
        self.master.title("Application : Tables de routage")

        # Création de l'instance du graphe generer aleatoirement selon les regles donnée
        # dans le module reseau.py
        self.graphe = reseau.Graphe()
        # lancer le main de la classe Graphe dans reseau.py
        self.graphe.main()

        # Création du canevas pour afficher le graphe
        self.graph_frame = tk.Frame(self.master)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Création de la figure Matplotlib
        self.figure = plt.figure(figsize=(12, 8))
        self.ax = self.figure.add_subplot(111)

        # Création d'un cadre pour les paramètres
        self.param_frame = tk.Frame(self.master)
        self.param_frame.pack(pady=8)

        # Étiquettes et champs de saisie pour les paramètres
        tk.Label(self.param_frame, text="Nœud de départ :",font=("Helvetica",12)).grid(row=0, column=0, padx=5)
        self.sommet_source = tk.Entry(self.param_frame)
        self.sommet_source.grid(row=0, column=1, padx=5)
        
        tk.Label(self.param_frame, text="Nœud d'arrivée :",font=("Helvetica",12)).grid(row=1, column=0, padx=5)
        self.sommet_dest = tk.Entry(self.param_frame)
        self.sommet_dest.grid(row=1, column=1, padx=5)
        
        # Bouton pour afficher le plus court chemin
        tk.Button(self.param_frame, text="Afficher le plus court chemin",font=("Helvetica",12), command=self.afficher_pcc).grid(row=2, columnspan=2, pady=5)
        
        # Étiquettes pour afficher le plus court chemin et la distance minimale
        self.pcc_label = tk.Label(self.param_frame, text="",font=("Helvetica",12))
        self.pcc_label.grid(row=1, column=4, columnspan=2, padx=5, pady=5)

        self.distmin_label = tk.Label(self.param_frame, text="",font=("Helvetica",12))
        self.distmin_label.grid(row=2, column=4, columnspan=2, padx=5, pady=5)

        # affichage du graphe sur la fentre avec networkx
    
        self.G, self.couleurs_noeud = self.afficher_graphe()
        self.pos = nx.spring_layout(self.G)
        self.Visual()# lancer le visual pour visualiser le graphe

        # Intégration de la figure dans la fenêtre Tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def afficher_graphe(self):
        '''Création du graphe initial.'''
        G = nx.Graph()
        # parcourrir les noeud de notre graphe 
        for noeud in self.graphe.noeuds:
            G.add_node(noeud.id)
        # ajouter un noeud ses voisin 
        for noeud in self.graphe.noeuds:
            for voisin, temps_communication in noeud.voisins:
                G.add_edge(noeud.id, voisin.id, weight=temps_communication)
        
        # Attribution des couleurs aux différents groupes de nœuds(au != tiers)
        tier1 = [noeud.id for noeud in self.graphe.noeuds if 1 <= noeud.id <= 10]
        tier2 = [noeud.id for noeud in self.graphe.noeuds if 11 <= noeud.id <= 30]
        tier3 = [noeud.id for noeud in self.graphe.noeuds if noeud.id>30]
        neoud_couleurs = ['violet' for _ in tier1] + ['yellow' for _ in tier2] + ['blue' for _ in tier3]

        return G, neoud_couleurs

    def Visual(self):
        '''Visualisation du graphe.'''
        # Dessin des nœuds
        nx.draw_networkx_nodes(self.G, self.pos, node_color=self.couleurs_noeud, node_size=500, alpha=0.8, ax=self.ax)

        # Dessin des arêtes
        nx.draw_networkx_edges(self.G, self.pos, width=1.0, alpha=0.5, ax=self.ax)

        # Affichage des étiquettes(chaque noeud avec son chiffre de 1 a 100) des nœuds
        nx.draw_networkx_labels(self.G, self.pos, font_size=10, font_family='sans-serif', ax=self.ax)

    def afficher_pcc(self):
        ''' Methode qui affiche le plus court chemin de noeud source choisie vers la destination'''
        
        # recuperer les sommet de depart et arrivée saisie par l'utilisateur 
        start_node_id = int(self.sommet_source.get())
        end_node_id = int(self.sommet_dest.get())

        try:
            # Reconstitution du chemin le plus court entre les deux nœuds sélectionnés
            pcc, distmin = self.graphe.reconstruire_chemin(self.graphe.noeuds[start_node_id - 1], self.graphe.noeuds[end_node_id - 1])
            # Mise à jour des étiquettes pour afficher le plus court chemin et la distance minimale
            self.pcc_label.config(text="Chemin le plus court : " + str(pcc))
            self.distmin_label.config(text="Distance minimale : " + str(distmin))
            # Rafraichissement de l'affichage
            self.ax.clear()
            self.Visual()
            # afficher le plus court chemin sur l'interface avec des aretes en rouge
            nx.draw_networkx_edges(self.G, self.pos, edgelist=[(pcc[i], pcc[i+1]) for i in range(len(pcc)-1)], width=3.0, alpha=0.8, edge_color='red', ax=self.ax)
            self.canvas.draw()
        except Exception as e:
            pass

if __name__=="__main__":
    
# lancement d'application
    fenetre = tk.Tk()
    app = Application(fenetre)
    fenetre.mainloop()


