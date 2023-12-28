# C1S1: Nombres entiers

## 1. Nombres entiers naturels et nombres entiers relatifs

### Définitions
Les **nombres entiers naturels** sont des nombres que nous utilisons pour compter et ordonner des objets. Ils sont notés par l'ensemble symbolisé par $\mathbb{N}$. L'ensemble des nombres entiers naturels commence à 0 et continue indéfiniment vers l'infini positif. Voici les premiers nombres entiers naturels: 0, 1, 2, 3, 4, 5, ...

Les **nombres entiers relatifs** comprennent tous les nombres entiers naturels ainsi que leurs opposés négatifs et le zéro. Ils sont notés par l'ensemble symbolisé par $\mathbb{Z}$. Cela inclut donc tous les nombres positifs et négatifs sans partie décimale. Exemples de nombres entiers relatifs: -3, -2, -1, 0, 1, 2, 3.

### Propriétés
- $\mathbb{N} \subset \mathbb{Z}$, ce qui signifie que tous les nombres entiers naturels sont aussi des nombres entiers relatifs.
- L'addition ou la multiplication de deux entiers relatifs donne toujours un entier relatif.
- La soustraction de deux entiers relatifs donne également un entier relatif.

### Exemples
- 7 est un nombre entier naturel, donc il appartient à $\mathbb{N}$ et à $\mathbb{Z}$.
- -5 est un nombre entier relatif, donc il appartient à $\mathbb{Z}$ mais pas à $\mathbb{N}$.

## 2. Multiples et diviseurs

### Définitions
Un nombre entier $b$ est dit **multiple** d'un nombre entier $a$ si $b$ peut être écrit sous la forme $b = a \times k$, où $k$ est aussi un entier. Dans cette situation, on dit aussi que $a$ est un **diviseur** de $b$.

Un nombre entier est **pair** s'il est multiple de 2, c'est-à-dire qu'il peut s'écrire sous la forme $2k$ où $k$ est un entier. Un nombre entier est **impair** s'il peut s'écrire sous la forme $2k + 1$ où $k$ est un entier.

### Propriétés
- Tout nombre entier est multiple de lui-même et de 1.
- Les multiples d'un nombre entier forment une suite infinie.
- Un nombre entier a toujours un nombre fini de diviseurs.

### Exemples
- 15 est un multiple de 3 car $15 = 3 \times 5$.
- 4 est un nombre pair car $4 = 2 \times 2$.
- 7 est un nombre impair car $7 = 2 \times 3 + 1$.

### Remarques
- Tout nombre pair peut s'écrire sous la forme $2k$, où $k$ est un entier, et tout nombre impair sous la forme $2k+1$.
- Les notions de multiple et diviseur sont fondamentales en arithmétique et sont utilisées pour simplifier les fractions, par exemple.

## Démonstrations

### Somme de deux multiples
Soient $a$, $m$ et $n$ trois nombres entiers tels que $m$ et $n$ sont des multiples de $a$. Alors il existe deux entiers $k$ et $l$ tels que $m = ak$ et $n = al$. La somme de $m$ et $n$ est donc $m + n = ak + al = a(k + l)$, qui est un multiple de $a$.

### Carré d'un nombre impair
Soit $n$ un nombre impair, alors $n$ peut s'écrire sous la forme $2k + 1$. Le carré de $n$ est donc $n^2 = (2k + 1)^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1$. Puisque $2k^2 + 2k$ est un entier, on voit que $n^2$ est de la forme $2k' + 1$ où $k'$ est un entier, donc $n^2$ est impair.

## Applications pratiques

### Algorithmes
- Pour déterminer si un nombre entier $b$ est multiple d'un autre nombre entier $a$, on divise $b$ par $a$. Si le reste de la division est 0, alors $b$ est multiple de $a$.
- Pour trouver le plus grand multiple de $a$ inférieur ou égal à $b$, on divise $b$ par $a$ et on prend le quotient multiplié par $a$.
- Pour déterminer si un entier naturel $n$ est premier, on vérifie s'il a des diviseurs autres que 1 et lui-même. Si ce n'est pas le cas, $n$ est premier.

### Théorie des nombres
La théorie des nombres est la branche des mathématiques qui étudie les propriétés des nombres entiers. Elle a des applications dans des domaines variés tels que la cryptographie, la théorie des codes et l'informatique théorique.