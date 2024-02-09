""""
librairie pour les coût et les contraintes utiliser par la librairie graphe pour
faire le "graphe" qui corrspond à la situation et qui permettra de donner
le déploiement optimal du personnel."""

from sympy import Abs
from typing import Union
from typing import List, Tuple


def var_personnel(pers: int) -> List[int]:
    """
    Fonction qui à partir du nombre de personnel que l'on a initialement nous donne une liste
    des variations  de personnel possible.

    Argument:

    pers: le nombre de personnel que l'on a.

    Exemple:
    >>> var_personnel(3)
    >>> [-1,0,1]
    """
    if pers < 0:
        raise ValueError("le nombre de personnel que l'on a doit être positif ou nul")
    liste_var_personnel = []
    borne_1 = int(3)
    borne_2 = int((1 / 3) * pers)
    if borne_1 <= borne_2:
        for i in range(-borne_1, borne_1 + 1):
            liste_var_personnel.append(i)
    else:
        for i in range(-borne_2, borne_2 + 1):
            liste_var_personnel.append(i)
    return liste_var_personnel


def var_personnel_final(pers: int, Liste: List[Tuple[str, int]]) -> Union[int, str]:
    """
    Fonction qui nous donne si cela est possible le nombre de personnel que l'on doit
    ajouter ou enlever pour respecter la condition du personnel qui doit exactement
    être présent au dernier mois.
    Si cela est impossible la fonction nous indique que la variation est impossible et
    que la contrainte est donc non respecter.

    Argument:

    pers:le nombre de personnel que l'on a.
    Liste: correspond à la liste de tuple comprenant le nom du mois et la condition
    associé à ce mois, dans l'ordre chronologique.

    Exemple:

    >>> var_personnel_final(2,[("Janvier",3),("Fevrier",2),("Mars",10)])
    >>> 'contrainte non respecter'
    """
    if pers < 0:
        raise ValueError("le nombre de personnel que l'on a doit être positif ou nul")
    var_pers_psbl = var_personnel(pers)
    var_final = int(Liste[-1][1] - pers)
    if var_final in var_pers_psbl:
        return var_final
    else:
        return "contrainte non respecter"


def cost_1(var: int) -> int:
    """
    Fonction qui nous donne que coût associer à la variation du personnel.

    Argument:

    var: la variation du personnel

    Exemple:

    >>> cost_1(-3)
    >>> 480

    """
    cost1 = Abs(var) * 160
    return cost1


def cost_2(pers: int, contr: int) -> int:
    """
    Fonction qui nous donne le coût liée à la présence de personne surnuméraire.

    Arguments:

    pers: le nombre de personne que l'on a.
    contr: la condition de personne minimal que l'on devrais avoir.

    Exemple:

    >>> cost_2(3,2)
    >>> 200

    """
    if pers < 0 or contr < 0:
        raise ValueError("Les arguments doivent être des entiers positif ou nul")
    pers_snum = int(pers - contr)
    if pers_snum != pers:
        if pers_snum > 0:
            return 200 * pers_snum
        else:
            return 0
    else:
        return 0


def cost_3(pers: int, contr: int) -> Union[str, int]:
    """Fonction qui nous donne le coût liée aux personne manquantes. Nous renvoient un message si
    la contrainte ne peut pas être respecter

    Arguments:

    pers: le nombre de personne que l'on a.
    contr: la condition de personne minimal que l'on devrais avoir.

    Exemple:

    >>> cost_3(2,3)
    >>> 'Contrainte non respecter'

    """
    if pers < 0 or contr < 0:
        raise ValueError(
            "Les arguments doivent être des entiers et doivent être non négatif"
        )
    if pers < contr:
        if pers * (125 / 100) < contr:
            return "Contrainte non respecter"
        elif pers * (125 / 100) >= contr:
            return 200 * int(contr - pers)
    return 0


def cost_t(pers: int, contr: int, var: int) -> Union[str, int]:
    """
    Fonction qui nous renvoie le coût total si notre contraintes de personnel présent
    sur le site minimal est respecter.

    Arguments:

    pers: le nombre de personne que l'on a.
    contr: la condition de personne minimal que l'on devrais avoir.
    var: la variation du personnel

    Exemple:

    >>> cost_t(3,3,1)
    >>> 160

    """
    if pers < 0 or contr < 0:
        raise ValueError(
            "Les arguments doivent être des entiers et doivent être non négatif"
        )
    c3 = cost_3(pers, contr)
    if contr == 0:
        return cost_1(var)
    elif c3 != "Contrainte non respecter":
        if isinstance(c3, int):
            return cost_1(var) + cost_2(pers, contr) + c3
        return "Contrainte non respecter"
    return "Contrainte non respecter"


def contr_final(var: Union[int, str]) -> Union[str, int]:
    """Fonction qui nous donne le coût pour le dernier mois si la contrainte de personnel
    présent sur le site du dernier mois est respecter sinon nous renvoie un message pour
    nous indiquer que la contrainte n'est pas respecter.

    Arguments:

    var: variation du personnel que l'on peut faire entre l'avant dernier et le dernier mois.

    Exemple:

    >>> contr_final(5)
    >>> 800

    >>> contr_final("contrainte non respecter")
    >>> 'contrainte non respecter'

    """
    if isinstance(var, str):
        return "contrainte non respecter"
    else:
        return cost_1(var)
