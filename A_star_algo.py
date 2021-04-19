from copy import deepcopy

etat_final = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]  # etat but, soit le 0 qui symbolise la case vide
operateurs_de_transformations = {"U" : [-1, 0], "D" : [1, 0], "L" : [0, -1], "R" : [0, 1]}
# + l'état initial sera entré dans le module Main.py, le test but est implémenté ci-dessus dans la fonction main()

# Définissons une classe taquin, caractérisée par sa matrice de valeurs, la matrice du taquin antécédent, l'operation resultante et les valeurs de l'algorithme A*, F=G+H.
class Taquin :
    # Constructeur de la classe
    def __init__(self, matrice_courante, matrice_precedente, g, h, operation) :
        self.matrice_courante = matrice_courante
        self.matrice_precedente = matrice_precedente
        self.g = g  # Coût (steps), du point de départ --> à l'etat du taquin n
        self.h = h  # Coût heuristique estimé, du taquin n --> au taquin à l'etat final (calculé par la "distance de Manhattan")
        self.operation = operation

    # L'agorithme de recherche A* sélectionne le chemin qui minimise la fonction: f(taquin) = G(taquin)+H(taquin)
    # définissons une methode qui calcule ce paramètre
    def f(self) :
        return self.g + self.h


# Définissons une fonction qui retourne les coordonnées (ligne,col) d'une case dans un taquin 3*3 donné
def coordonnees(taquin, cellule) :
    for ligne in range(3) :
        if cellule in taquin[ligne] :
            return (ligne, taquin[ligne].index(cellule))


#Définissons une fonction qui renvoie la valeur de l'heuristique H qui est l'estimation à vol d'oiseau de la distance
# à quelle se trouve le but (calculé par Manhattan algo: H=|xf-x0|+|yf-y0|)
#C'est-à-dire le coût total du déplacement de chaque case de son état actuel dans un taquin i à son état final dans
# le taquin f, en négligeant la présence d'autres cases (murs) entre le chemin des 2 états qui peuvent empecher ce mouvement
def cout_heuristique(etat_courant) :
    cout = 0
    for ligne in range(3) :
        for col in range(3) :
            (ligne_final, col_final) = coordonnees(etat_final, etat_courant[ligne][col]) # Coordonnées de la case à l'état final du taquin
            cout += abs(ligne - ligne_final) + abs(col - col_final) # Formule de distance de Manhattan
    return cout

#Définissons une fonction qui renvoie une liste des nouveaux états des taquins après avoir appliqué toutes les opérations possibles {U,D,R,L} sur un taquin donné
# operations(taquin_père) --> liste(taquins_fils)
def appliquer_operations(taquin) :
    liste_taquins_transformes = []
    pos_vide = coordonnees(taquin.matrice_courante, 0)

    for operation in operateurs_de_transformations.keys() :
        new_pos = ( pos_vide[0] + operateurs_de_transformations[operation][0], pos_vide[1] + operateurs_de_transformations[operation][1] )
        if 0 <= new_pos[0] <3 and 0 <= new_pos[1] < 3 : # Vérifier la possibilité d'opération
            new_matrix = deepcopy(taquin.matrice_courante)
            # Switcher les deux cases
            new_matrix[pos_vide[0]][pos_vide[1]] = taquin.matrice_courante[new_pos[0]][new_pos[1]]
            new_matrix[new_pos[0]][new_pos[1]] = 0
            # Ajouter un Objet Taquin à la liste des taquins transformées
            liste_taquins_transformes.append(Taquin(new_matrix, taquin.matrice_courante, taquin.g + 1, cout_heuristique(new_matrix), operation))

    return liste_taquins_transformes

# Définissons une fonction qui renvoie le meilleur taquin de l'ensemble des taquins fils -meilleur c.-à-d plus petite f(n)=g(n)+h(n)
def meilleur_taquin(open_liste) : #input == dictionnaire des taquins prets à traiter de la forme {str(matrice):Objet Taquin(),...}
    first_iter = True

    for taquin in open_liste.values() :
        if first_iter or taquin.f() < bestF :
            first_iter = False
            meilleur_taquin = taquin
            bestF = meilleur_taquin.f()
    return meilleur_taquin

# Définissons une fonction qui renvoie le chemin/la branche des taquins choisis de l'état initial à l'état final
# une liste contenant des dictionnaires {'operation':opération effectuée, 'taquin':matrice résultant}
def chemin(closed_liste) : #input == dictionnaire des taquins deja choisis et parcourus de la forme {str(matrice):Objet Taquin(),...}
    taquin = closed_liste[str(etat_final)]
    branche = list()

    while taquin.operation :
        branche.append({
            'operation' : taquin.operation,
            'taquin' : taquin.matrice_courante
        })
        taquin = closed_liste[str(taquin.matrice_precedente)]
    branche.append({
        'operation' : 'taquin initial sans opération de transformation',
        'taquin' : taquin.matrice_courante
    })
    branche.reverse()

    return branche


def main(puzzle_initial) : #input == matrice (liste de 3 listes de 3 entiers entre 0 et 8)

    #Soit l'open_liste qui stocke les noeuds à traiter, en commençant par le t initial.
    # un dictionnaire sous la forme {clé0:valeur0,...} avec str(matrice) comme clé, un Objet Taquin comme valeur
    open_liste = {str(puzzle_initial) : Taquin(puzzle_initial, puzzle_initial, 0, cout_heuristique(puzzle_initial), "")}

    #Soit le close_liste qui stocke les taquins déjà choisis et traités
    closed_liste = {}

    while True :
        taquin_a_traiter = meilleur_taquin(open_liste) #I. choisir le taquin à étendre, pour continuer dans cette branche du meilleur f(n)
        closed_liste[str(taquin_a_traiter.matrice_courante)] = taquin_a_traiter #II. ajouter ce taquin à la liste closed

        if taquin_a_traiter.matrice_courante == etat_final : #III. Test-but
            return chemin(closed_liste)

        taquins_fils = appliquer_operations(taquin_a_traiter) #IV. étendre ce taquin père dans une Liste_fils
        #V. Ajouter les fils à la liste open pour être traités -avec certains conditions-:
        for t in taquins_fils :
            #conditions : on doit pas ajoutés tous les taquins à la liste open pour être traités :: car il ne sert à rien de traiter un taquin t:
            # 1. déjà traités (se trouve dans closed_liste) -peut déclencher une boucle infinie-
            # 2. s'il y a un taquin de même matrice que t, mais de meilleur f(n) que t, qui sera traitée (se trouve deja dans open_liste)
            if str(t.matrice_courante) in closed_liste.keys() or \
                str(t.matrice_courante) in open_liste.keys() and open_liste[str(t.matrice_courante)].f() < t.f() :
                continue
            open_liste[str(t.matrice_courante)] = t #si les conditions de traitement sont correctes, on ajoute le fils à la liste open

        #VI. Supprimer le taquin père (taquin_a_traiter) de la liste open
        del open_liste[str(taquin_a_traiter.matrice_courante)]
