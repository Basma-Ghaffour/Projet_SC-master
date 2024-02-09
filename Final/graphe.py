"""Description.
libraire qui crée le "graphe" correspondant à la situation afin de donner
le déploiement optimal du personnel en minimisant les coûts pour la firme."""

import Final.contraintes as ct
import networkx as nx
from typing import List, Tuple, Dict, Union


def initialisation(Liste: List[Tuple[str, int]]) -> Tuple[nx.Graph, dict, int]:
    """Fonction que fait la tout première partie de la construction du "graphe".
    Crée un "graphe" avec la librairie networkx, ensuite crée le tout premier
    noeux et le premier élément de la liste des indice.
    """
    for val in Liste:
        if val[1] < 0:
            raise ValueError(
                "le deuxième élément du couple "
                + str(val)
                + " est inférieur à zéro et on ne peut avoir de personnel ou"
                + "de contrainte négative."
            )
    graphe = nx.DiGraph()
    graphe.add_node(
        Liste[0][0], var="na", nb_pers=Liste[0][1], cost=0, cond="na", mois=Liste[0][0]
    )
    Liste_indice = {}
    Liste_indice[Liste[0][0]] = [Liste[0][0]]
    i = 0
    i = i + 1
    return graphe, Liste_indice, i


def construction_intermediaire(
    Liste_indice: Dict, Liste: List[Tuple[str, int]], graphe: nx.Graph, i: int
) -> Tuple[nx.Graph, Dict, int]:
    """Fonction qui réalise la construction intermédiraire. Se base sur une "graphe",
    une liste déja crée dans l'initalisation. Puis génère les arrete et noeux et
    s'arrete à la création des noeux qui correspondent au états possible de l'avant
    dernier noeux."""
    for elem in Liste:
        if elem[1] < 0:
            raise ValueError(
                "le deuxième élément du couple "
                + str(elem)
                + " est inférieur à zéro et on ne peut avoir de personnel ou de"
                + "contrainte négative."
            )
    for k in range(0, len(Liste) - 2):  # boucle sur tout les mois sauf les deux dernier
        liste_idc = []
        for j in Liste_indice[
            Liste[k][0]
        ]:  # boulce sur tout état possible du mois dans lequel on se trouve
            for variation in ct.var_personnel(
                list(graphe.nodes[j].values())[1]
            ):  # boucle pour toute les variation de personnel possible
                pers = list(graphe.nodes[j].values())[1]
                cost = ct.cost_t(pers + variation, Liste[k + 1][1], variation)
                if cost != "Contrainte non respecter":
                    i = i + 1
                    graphe.add_node(
                        i,
                        var=variation,
                        nb_pers=pers + variation,
                        cost=cost,
                        mois=Liste[k + 1][0],
                    )
                    graphe.add_edge(j, i, weight=cost)
                    liste_idc.append(i)
        Liste_indice[Liste[k + 1][0]] = liste_idc
    return graphe, Liste_indice, i


def finalisation(
    Liste_indice: Dict, Liste: List[Tuple[str, int]], graphe: nx.Graph
) -> Tuple[Dict, nx.Graph, List[Union[int, str]]]:
    """Fonction qui finalise la construction du graphe, qui nous génère les dernieres arretes
    qui lient l'avant dernier mois au dernier mois et ainsi finalise la contruction du "graphe".
    """
    for val in Liste:
        if val[1] < 0:
            raise ValueError(
                "le deuxième élément du couple "
                + str(val)
                + " est inférieur à zéro et on ne peut avoir"
                + "de personnel ou de contrainte négative."
            )
    graphe.add_node(Liste[-1][0], mois=Liste[-1][0])
    res = []
    for j in Liste_indice[Liste[-2][0]]:
        vart = ct.var_personnel_final(list(graphe.nodes[j].values())[1], Liste)
        cost = ct.contr_final(vart)
        if cost != "contrainte non respecter":
            graphe.add_edge(j, Liste[-1][0], weight=cost)
            res.append(cost)
        else:
            res.append(cost)
    return Liste_indice, graphe, res


def graph_fin(
    Liste: List[Tuple[str, int]]
) -> Tuple[Dict, nx.Graph, List[Union[str, int]]]:
    """Fonction qui nous crée le graphe en fonction d'une liste qui correspond à la liste des
    mois pour lequel on veut minimiser les coûts"""
    for val in Liste:
        if val[1] < 0:
            raise ValueError(
                "le deuxième élément du couple "
                + str(val)
                + " est inférieur à zéro et on ne peut avoir"
                + "de personnel ou de contrainte négative."
            )
    if len(Liste) < 2:
        raise ValueError("La taille de la liste doit être supérieur à 1.")
    graphe, Liste_indice, i = initialisation(Liste)
    graphe_s, Liste_indice_s = construction_intermediaire(
        Liste_indice, Liste, graphe, i
    )[:-1]
    Liste_indice_t, graphe_t, res_t = finalisation(Liste_indice_s, Liste, graphe_s)
    return Liste_indice_t, graphe_t, res_t
