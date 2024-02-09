# Projet Supply Chain

## Description

On a une librairie solution doublée d'une interface en ligne de commande. Il n'y a qu'un seule commande `solution`. Cette commande permet d'avoir une sortie qui donne le nombre optimal de personnel à déployer chaque mois afin de minimiser les coûts pour la firme. Cette commande nous donne également le coût associé à chaque mois et le coût sur toute la période.

## Exemple

On a un exemple de l'utilisation de la commande solution dans le fichier exemple. (exemple avec les données de l'énoncé)

## Librairies

### Librairie `contraintes`

La librairie contraintes permet de prendre en compte les coûts et les contraintes qui serons ensuite utilisés pour la contruction du "graphe".

- Ajouter ou enlever une personne coute 160 euros. (pris en compte dans la fonction cost_1)
- Il y a 200 euros de frais liés à la présence de personnel surnuméraire par mois. (pris en compte dans la fonction cost_2)
- Il y a 200 euros de frais par personne manquante par mois, sachant qu'au plus 25% d'heures supplémentaires peuvent être effectuées. (pris en compte dans la fonction cost_3) Fonction qui nous donne le coût lié aux personnes manquantes. Nous renvoient un message si la contrainte ne peut pas être respectée. Cette fonction de coût est aussi une contrainte qui est prise en compte dans cette version.
- Pour des raisons syndicales, on ne peut échanger plus de 3 personnes chaque mois et 1/3 du total des présents (pris en compte dans la fonction var_personnel)
- Il y a déjà 3 personnes présent en Janvier. Il doit y en avoir exactement 3 en septembre. (prise en compte dans la fonction var_personnel_final) Si cette contrainte n'est pas respectée alors la fonction nous renvoie un message, cette fonction prend également en compte notre dernière contrainte.

### Librairie `graphe`

La librairie graphe contient 4 fonctions qui permettent la création du "Graphe", les fonctions `initialisation`, `construction_intermédiaire` et `finalisation` servent uniquement a crée le "graphe". Elle sont séparées de façon à faciliter la lecture et les tests et sont ainsi utiliseé dans la dernière fonction `graphe` qui crée le "graphe" final.

### Librairie `solution` 

C'est la librairie qui est utilisée par l'utilisateur afin d'avoir le déploiement optimal de personnel sur la période donnée. 
