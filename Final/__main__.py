"""
Application ligne de commande pour la librairie pour la librairie solution.
"""

import typer
from typing import List, Tuple
import networkx as nx
import Final.graphe as gp

application = typer.Typer()


@application.command()
def solution(Liste: List[Tuple[str, int]]):
    """La fonction solution permet d'avoir la décision de déploiement optimal de personnel.
    L'input de la fonction doit être une Liste composer de Tuple d'élément. Pour chaque
    Tuple on doit avoir comme premier élément une chaîne de charactère du nom du mois.
    Le second élément doit être un integer du nombre de personnel associer à ce mois ci.
    Le premier Tuple correspond au premier mois de la période de décision de déploiement et
    donc le second élément du premier Tuple doit être le nombre de personnel présent au
    premier mois. Le dernier Tuple de la liste correspond au mois de la fin de la période et
    le nombre de personnel associé doit correspondre au nombre de personnel qui doit être
    présent au dernier mois. Tout les Tuple entre le premier Tuple et le dernier Tuple
    correspondent aux mois entre, dans l'ordre chronologique et chaque personnel associer
    correspond à la contrainte de personnel minimal qui doit être présent sur le site. Si
    pour un mois il n'y a pas de contraintes alors il faut mettre 0.
    
    Exemple:
    
    >>> solution(Liste=[("Janvier",3),("Février",0),("Mars",2),("Avril",3)])
    Pour le mois de Janvier on à comme condition d'avoir exactement 3 personne.
    On doit déployer 3 personnes pour le mois de Février le coût associé à ce mois est de 0
    euros. On doit déployer 3 personnes pour le mois de Mars le coût associé à ce mois est de
    200 euros. Pour le mois de Avril, on doit avoir exactement 3 personnes et le coût associer
    à ce mois est de 0 euros. Au final en minimisant les coûts on aura un coût total de 200
    euros pour tous les mois.

    """
    for val in Liste:
        if val[1] < 0:
            raise ValueError(
                "Le deuxième élément du couple "
                + str(val)
                + " est inférieur à zéro et on ne peut avoir de personnel"
                + "ou de contrainte négative."
            )
    L, G, R = gp.graph_fin(Liste)
    if isinstance(G, nx.DiGraph):
        if len(list(G.predecessors(Liste[-1][0]))) == 0:
            raise ValueError(
                "Le dernier noeux du 'graphe'représentant la situation n'a aucun précdecesseurs."
                / "Cela signifie que les contraintes liées au personnel présent sur le site"
                / "ne peuvent pas être respecter."
            )
    chemin = nx.bellman_ford_path(G, Liste[0][0], Liste[-1][0], weight="weight")
    mois = Liste[0][0]
    pers = Liste[0][1]
    cout_total = 0
    print(
        f"Pour le mois de {mois} on à comme condition d'avoir exactement {pers} personne."
    )
    for ch in chemin[1:-1]:
        mois = list(G.nodes[ch].values())[3]
        pers = list(G.nodes[ch].values())[1]
        cost = list(G.nodes[ch].values())[2]
        cout_total = cout_total + cost
        print(
            f"On doit déployer {pers} personnes pour le mois de {mois}"
            f"le coût associé à ce mois est de {cost} euros."
        )
    mois = Liste[-1][0]
    pers = Liste[-1][1]
    cost = R[L[Liste[-2][0]].index(chemin[-2])]
    print(
        f"Pour le mois de {mois}, on doit avoir exactement {pers} "
        f"personnes et le coût associer à ce mois est de {cost} euros."
    )
    cout_total = cout_total + cost
    print(
        "Au final en minimisant les coûts on aura un coût total "
        f"de {cout_total} euros pour tous les mois."
    )

    if __name__ == "__main__":
        application()
