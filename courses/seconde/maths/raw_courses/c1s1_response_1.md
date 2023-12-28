# Nombres Entiers

## Notations ℕ et ℤ

### Définitions
- **Nombres entiers naturels (ℕ)**: L'ensemble des nombres entiers naturels, noté ℕ, comprend tous les nombres entiers non négatifs (0, 1, 2, 3, ...).
- **Nombres entiers relatifs (ℤ)**: L'ensemble des nombres entiers relatifs, noté ℤ, inclut tous les nombres entiers naturels ainsi que leurs opposés négatifs (-1, -2, -3, ...) et le zéro.

### Exemples
- 5 ∈ ℕ et 5 ∈ ℤ car 5 est un nombre entier naturel et donc aussi un entier relatif.
- -3 ∉ ℕ mais -3 ∈ ℤ car -3 est un entier négatif, donc pas naturel, mais c'est un entier relatif.

## Multiples et Diviseurs

### Définitions
- **Multiple**: Un nombre entier a est un multiple d'un autre nombre entier b si a peut être exprimé comme b multiplié par un entier k. Cela s'écrit a = b × k.
- **Diviseur**: Un nombre entier b est un diviseur d'un autre nombre entier a si a peut être divisé par b sans laisser de reste. Cela signifie qu'il existe un entier k tel que a = b × k.

### Propriétés
- Si b est un diviseur de a, alors a est un multiple de b.
- Tout nombre entier est un multiple de 1 et de lui-même.
- Tout nombre entier a au moins deux diviseurs distincts: 1 et lui-même.

### Exemples
- 15 est un multiple de 3 car 15 = 3 × 5.
- 4 est un diviseur de 20 car 20 = 4 × 5.

## Nombres Pairs et Impairs

### Définitions
- **Nombre pair**: Un nombre entier est pair s'il est un multiple de 2.
- **Nombre impair**: Un nombre entier est impair s'il n'est pas un multiple de 2.

### Exemples
- 6 est pair car 6 = 2 × 3.
- 7 est impair car il n'existe pas d'entier k tel que 7 = 2 × k.

## Nombres Premiers

### Définitions
- **Nombre premier**: Un nombre entier supérieur à 1 est premier s'il a exactement deux diviseurs distincts: 1 et lui-même.

### Exemples
- 5 est un nombre premier car ses seuls diviseurs sont 1 et 5.
- 4 n'est pas un nombre premier car il a trois diviseurs: 1, 2 et 4.

## Résultats Fractionnaires et Forme Irréductible

### Définitions
- **Fraction irréductible**: Une fraction est dite irréductible si son numérateur et son dénominateur n'ont aucun diviseur commun autre que 1.

### Propriétés
- Toute fraction peut être simplifiée en une fraction irréductible en divisant le numérateur et le dénominateur par leur plus grand diviseur commun (PGCD).

### Exemples
- La fraction 8/12 peut être simplifiée en 2/3 car 4 est le PGCD de 8 et 12.

## Démonstrations

### Somme de Multiples
- **Propriété**: La somme de deux multiples d'un nombre entier a est également un multiple de a.
- **Démonstration**: Soient m = a × k et n = a × l deux multiples de a. Alors m + n = a × k + a × l = a × (k + l), qui est un multiple de a.

### Carré d'un Nombre Impair
- **Propriété**: Le carré d'un nombre impair est toujours impair.
- **Démonstration**: Soit n un nombre impair, alors n = 2k + 1 pour un certain entier k. Le carré de n est n² = (2k + 1)² = 4k² + 4k + 1 = 2(2k² + 2k) + 1, qui est de la forme 2m + 1, donc impair.

## Algorithmes et Théorie des Nombres

### Algorithmes
- Pour déterminer si un entier naturel est multiple d'un autre, on divise le premier par le second et on vérifie s'il y a un reste.
- Pour trouver le plus grand multiple de a inférieur ou égal à b, on divise b par a et on prend la partie entière du résultat multipliée par a.
- Pour déterminer si un entier naturel est premier, on vérifie s'il n'a pas de diviseurs autres que 1 et lui-même, ce qui peut être fait en testant la divisibilité par tous les entiers jusqu'à la racine carrée de ce nombre.

### Applications Pratiques
La théorie des nombres a de nombreuses applications pratiques, notamment en cryptographie, en théorie des codes, et en informatique.

## Remarques
- Lorsqu'on travaille avec des nombres entiers, il est important de faire attention aux signes, surtout lorsqu'on travaille avec l'ensemble ℤ.
- La notion de nombre premier est fondamentale en mathématiques et a des implications profondes dans divers domaines de la science et de la technologie.