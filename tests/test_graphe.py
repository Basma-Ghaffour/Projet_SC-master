import pytest
from Final.graphe import (
    initialisation,
    construction_intermediaire,
    finalisation,
    graph_fin,
)
import networkx as nx
from Final.contraintes import cost_t, var_personnel_final, contr_final


Liste = [
    ("Janvier", 3),
    ("Fevrier", 0),
    ("Mars", 4),
    ("Avril", 6),
    ("Mai", 7),
    ("Juin", 4),
    ("Juillet", 6),
    ("Aout", 2),
    ("Septembre", 3),
]


def test_initialisation_graphe():
    graphe = nx.DiGraph()
    graphe.add_node("Janvier", var="na", nb_pers=3, cost=0, cond="na", mois="Janvier")
    assert initialisation(Liste)[0].nodes == graphe.nodes


def test_initialisation_graphe2():
    graphe = nx.DiGraph()
    graphe.add_node("Janvier", var="na", nb_pers=3, cost=0, cond="na", mois="Janvier")
    graphe2 = initialisation(Liste)[0]
    assert nx.get_node_attributes(graphe, "var") == nx.get_node_attributes(
        graphe2, "var"
    )
    assert nx.get_node_attributes(graphe, "nb_pers") == nx.get_node_attributes(
        graphe2, "nb_pers"
    )
    assert nx.get_node_attributes(graphe, "cost") == nx.get_node_attributes(
        graphe2, "cost"
    )
    assert nx.get_node_attributes(graphe, "cond") == nx.get_node_attributes(
        graphe2, "cond"
    )
    assert nx.get_node_attributes(graphe, "mois") == nx.get_node_attributes(
        graphe2, "mois"
    )


def test_initialisation_liste_indice():
    assert initialisation(Liste)[1] == {"Janvier": ["Janvier"]}


Liste_2 = [
    ("Janvier", -3),
    ("Fevrier", 0),
    ("Mars", 4),
    ("Avril", 6),
    ("Mai", 7),
    ("Juin", 4),
    ("Juillet", 6),
    ("Aout", 2),
    ("Septembre", 3),
]
Liste_3 = [
    ("Janvier", 3),
    ("Fevrier", 0),
    ("Mars", 4),
    ("Avril", -6),
    ("Mai", 7),
    ("Juin", 4),
    ("Juillet", 6),
    ("Aout", 2),
    ("Septembre", 3),
]
Liste_4 = [("Janvier", 3), ("Fevrier", 2), ("Mars", 3)]


def test_initialisation_val_error():
    with pytest.raises(ValueError):
        initialisation(Liste_2)
    with pytest.raises(ValueError):
        initialisation(Liste_3)


# --> graphe p 1/3 en utilisant les fonctions
graphe_p1 = initialisation(Liste_4)[0]


# --> situation graphe p 1/3 sans utiliser de fonction
graphe = nx.DiGraph()
graphe.add_node("Janvier", var="na", nb_pers=3, cost=0, cond="na", mois="Janvier")
i = 1
Liste_indice = {"Janvier": ["Janvier"]}


# test sur 3 mois uniquement


def test_construction_inter_val_error():
    with pytest.raises(ValueError):
        construction_intermediaire(Liste_indice, Liste_3, graphe_p1, i)


Liste_5 = [("Janvier", 3), ("Fevrier", 2)]
Liste_6 = [("Janvier", 3)]


def test_construction_inter_taille_list():
    test1 = construction_intermediaire(Liste_indice, Liste_5, graphe_p1, 1)[0]
    test2 = construction_intermediaire(Liste_indice, Liste_6, graphe_p1, 1)[0]
    assert test1.number_of_edges() == test2.number_of_edges()
    assert test1.number_of_nodes() == test2.number_of_nodes()
    assert nx.get_node_attributes(test1, "var") == nx.get_node_attributes(test2, "var")
    assert nx.get_node_attributes(test1, "nb_pers") == nx.get_node_attributes(
        test2, "nb_pers"
    )
    assert nx.get_node_attributes(test1, "cond") == nx.get_node_attributes(
        test2, "cond"
    )
    assert nx.get_node_attributes(test1, "mois") == nx.get_node_attributes(
        test2, "mois"
    )
    assert nx.get_node_attributes(test1, "cost") == nx.get_node_attributes(
        test2, "cost"
    )


# -->graphe p 2/3 sans utiliser de fonction
graphe_t = nx.DiGraph()
graphe_t.add_node("Janvier", var="na", nb_pers=3, cost=0, cond="na", mois="Janvier")
var = [-1, 0, 1]
i = 2
for v in var:
    graphe_t.add_node(i, var=v, nb_pers=3 + v, cost=cost_t(3 + v, 2, v), mois="Fevrier")
    graphe_t.add_edge("Janvier", i, weight=cost_t(3 + v, 2, v))
    i = i + 1


def test_construction_inter_3_premier_mois_nb_nodes():
    graphe3 = construction_intermediaire(Liste_indice, Liste_4, graphe_p1, 1)[0]
    assert graphe3.number_of_nodes() == graphe_t.number_of_nodes()


def test_contruction_inter_3_premier_mois_nb_edges():
    graphe3 = construction_intermediaire(Liste_indice, Liste_4, graphe_p1, 1)[0]
    assert graphe3.number_of_edges() == graphe_t.number_of_edges()


def test_contruction_inter_3_premier_mois_attribue_node():
    graphe3 = construction_intermediaire(Liste_indice, Liste_4, graphe_p1, 1)[0]
    assert nx.get_node_attributes(graphe3, "var") == nx.get_node_attributes(
        graphe_t, "var"
    )
    assert nx.get_node_attributes(graphe3, "nb_pers") == nx.get_node_attributes(
        graphe_t, "nb_pers"
    )
    assert nx.get_node_attributes(graphe3, "cond") == nx.get_node_attributes(
        graphe_t, "cond"
    )
    assert nx.get_node_attributes(graphe3, "mois") == nx.get_node_attributes(
        graphe_t, "mois"
    )
    assert nx.get_node_attributes(graphe3, "cost") == nx.get_node_attributes(
        graphe_t, "cost"
    )


def test_contruction_inter_3_premier_mois_attribue_edge():
    graphe3 = construction_intermediaire(Liste_indice, Liste_4, graphe_p1, 1)[0]
    assert nx.get_edge_attributes(graphe3, "weight") == nx.get_edge_attributes(
        graphe_t, "weight"
    )


def test_contruction_inter_3_premier_mois_voisins():
    graphe3 = construction_intermediaire(Liste_indice, Liste_4, graphe_p1, 1)[0]
    assert list(graphe3.neighbors("Janvier")) == list(graphe_t.neighbors("Janvier"))
    assert list(graphe3.neighbors(2)) == list(graphe_t.neighbors(2))
    assert list(graphe3.neighbors(3)) == list(graphe_t.neighbors(3))
    assert list(graphe3.neighbors(4)) == list(graphe_t.neighbors(4))


# -->graphe complet sur 3 mois sans utiliser de fonction
graphe_f = nx.DiGraph()
graphe_f.add_node("Janvier", var="na", nb_pers=3, cost=0, cond="na", mois="Janvier")
var = [-1, 0, 1]
i = 2
for v in var:
    graphe_f.add_node(i, var=v, nb_pers=3 + v, cost=cost_t(3 + v, 2, v), mois="Fevrier")
    graphe_f.add_edge("Janvier", i, weight=cost_t(3 + v, 2, v))
    i = i + 1
graphe_f.add_node("Mars", mois="Mars")
for j in [2, 3, 4]:
    vart = var_personnel_final(list(graphe_f.nodes[j].values())[1], Liste_4)
    cost = contr_final(vart)
    if cost != "contrainte non respecter":
        graphe_f.add_edge(j, "Mars", weight=cost)
        i = i + 1


# --> graphe p 2/3 en utilisant les fonction
graphe_p2, Liste_indice_p2, i = construction_intermediaire(
    Liste_indice, Liste_4, graphe_p1, 1
)


def test_finalisation_value_error():
    with pytest.raises(ValueError):
        finalisation(Liste_indice_p2, Liste_3, graphe_p2)
    with pytest.raises(ValueError):
        finalisation(Liste_indice_p2, Liste_3, graphe_p2)


def test_finalisation_3_p_mois_nb_nodes():
    graphe3 = finalisation(Liste_indice_p2, Liste_4, graphe_p2)[1]
    assert graphe3.number_of_nodes() == graphe_f.number_of_nodes()


def test_finalisation_3_p_mois_nb_edges():
    graphe3 = finalisation(Liste_indice_p2, Liste_4, graphe_p2)[1]
    assert graphe3.number_of_edges() == graphe_f.number_of_edges()


def test_finalisation_3_p_mois_attribute_nodes():
    graphe3 = finalisation(Liste_indice_p2, Liste_4, graphe_p2)[1]
    assert nx.get_node_attributes(graphe3, "var") == nx.get_node_attributes(
        graphe_f, "var"
    )
    assert nx.get_node_attributes(graphe3, "nb_pers") == nx.get_node_attributes(
        graphe_f, "nb_pers"
    )
    assert nx.get_node_attributes(graphe3, "cond") == nx.get_node_attributes(
        graphe_f, "cond"
    )
    assert nx.get_node_attributes(graphe3, "mois") == nx.get_node_attributes(
        graphe_f, "mois"
    )
    assert nx.get_node_attributes(graphe3, "cost") == nx.get_node_attributes(
        graphe_f, "cost"
    )


def test_finalisation_3_premier_mois_attribue_edge():
    graphe3 = finalisation(Liste_indice_p2, Liste_4, graphe_p2)[1]
    assert nx.get_edge_attributes(graphe3, "weight") == nx.get_edge_attributes(
        graphe_f, "weight"
    )


def test_finalisation_3_premier_mois_voisins():
    graphe3 = finalisation(Liste_indice_p2, Liste_4, graphe_p2)[1]
    assert list(graphe3.neighbors("Janvier")) == list(graphe_f.neighbors("Janvier"))
    assert list(graphe3.neighbors(2)) == list(graphe_f.neighbors(2))
    assert list(graphe3.neighbors(3)) == list(graphe_f.neighbors(3))
    assert list(graphe3.neighbors(4)) == list(graphe_f.neighbors(4))
    assert list(graphe3.neighbors("Mars")) == list(graphe_f.neighbors("Mars"))


# --> graphe final avec la fonction graph_fin (comparer avec graphe_f fait sans fonction)
graphe_fonc_fin = graph_fin(Liste_4)[1]


def test_graph_fin_value_error():
    with pytest.raises(ValueError):
        graph_fin(Liste_3)
    with pytest.raises(ValueError):
        graph_fin(Liste_3)


def test_graph_fin_3_p_mois_nb_edges():
    assert graphe_f.number_of_edges() == graphe_fonc_fin.number_of_edges()


def test_graph_fin_3_p_mois_attribute_nodes():
    assert nx.get_node_attributes(graphe_f, "var") == nx.get_node_attributes(
        graphe_fonc_fin, "var"
    )
    assert nx.get_node_attributes(graphe_f, "nb_pers") == nx.get_node_attributes(
        graphe_fonc_fin, "nb_pers"
    )
    assert nx.get_node_attributes(graphe_f, "cond") == nx.get_node_attributes(
        graphe_fonc_fin, "cond"
    )
    assert nx.get_node_attributes(graphe_f, "mois") == nx.get_node_attributes(
        graphe_fonc_fin, "mois"
    )
    assert nx.get_node_attributes(graphe_f, "cost") == nx.get_node_attributes(
        graphe_fonc_fin, "cost"
    )


def test_graph_fin_3_premier_mois_attribue_edge():
    assert nx.get_edge_attributes(graphe_f, "weight") == nx.get_edge_attributes(
        graphe_fonc_fin, "weight"
    )


def test_graph_fin_3_premier_mois_voisins():
    assert list(graphe_f.neighbors("Janvier")) == list(
        graphe_fonc_fin.neighbors("Janvier")
    )
    assert list(graphe_f.neighbors(2)) == list(graphe_fonc_fin.neighbors(2))
    assert list(graphe_f.neighbors(3)) == list(graphe_fonc_fin.neighbors(3))
    assert list(graphe_f.neighbors(4)) == list(graphe_fonc_fin.neighbors(4))
    assert list(graphe_f.neighbors("Mars")) == list(graphe_fonc_fin.neighbors("Mars"))


def test_graph_value_error_taille_list():
    with pytest.raises(ValueError):
        graph_fin(Liste_6)
