# Quiz de positionnement — Python pour le DevOps

**À compléter à l'inscription · ~20 min · auto-évalué**

Ce questionnaire n'est pas un examen : il sert à **se situer** avant la formation. Les
résultats permettent à chacun de savoir s'il est prêt, et au formateur de calibrer le rythme.
Répondre sans aide extérieure : un score honnête est plus utile qu'un bon score.

> La formation présuppose un **plancher** : savoir lire et écrire une fonction, une boucle,
> une condition, manipuler listes et dictionnaires, et lancer un script depuis un terminal.
> Les questions 1 à 6 vérifient ce plancher.

---

## Partie A — Fondations (plancher)

**Q1.** Que renvoie `len(["a", "b", "c"])` ?
- A. `"3"`
- B. `3`
- C. `["a", "b", "c"]`
- D. une erreur

**Q2.** Comment parcourir un à un les éléments d'une liste `cibles` ?
- A. `for c in cibles:`
- B. `for c of cibles:`
- C. `foreach cibles as c:`
- D. `while cibles:`

**Q3.** Soit `config = {"host": "localhost", "port": 8080}`. Comment lire le port ?
- A. `config.port`
- B. `config->port`
- C. `config["port"]`
- D. `config(port)`

**Q4.** Que vaut `x` à la fin ?
```python
x = 5
if x > 3:
    x = x + 1
```
- A. `5`
- B. `6`
- C. `3`
- D. `True`

**Q5.** Quelle définition renvoie la somme de deux arguments ?
- A. `def somme(a, b): print(a + b)`
- B. `def somme(a, b): return a + b`
- C. `function somme(a, b) { return a + b }`
- D. `def somme(a, b) => a + b`

**Q6.** Comment exécuter le fichier `beacon.py` depuis un terminal ?
- A. `run beacon.py`
- B. `python beacon.py`
- C. `exec beacon.py`
- D. `beacon.py --run`

---

## Partie B — Niveau attendu (intermédiaire)

**Q7.** Quelle structure permet de réagir à une erreur sans planter le programme ?
- A. `try: ... except ...:`
- B. `if error: ...`
- C. `catch { ... }`
- D. `on error: ...`

**Q8.** Que produit `[n * 2 for n in range(3)]` ?
- A. `[2, 4, 6]`
- B. `[0, 1, 2]`
- C. `[0, 2, 4]`
- D. `6`

**Q9.** Soit `d = {"a": 1}`. Que renvoie `d.get("z", 0)` ?
- A. `0`
- B. `None`
- C. une `KeyError`
- D. `"z"`

**Q10.** Pourquoi écrire `with open("f.txt") as f:` plutôt que `f = open("f.txt")` ?
- A. C'est plus rapide
- B. Le fichier se ferme automatiquement, même en cas d'erreur
- C. C'est obligatoire en Python 3
- D. Cela ouvre le fichier en écriture

**Q11.** Que valent respectivement `"5" + "5"` et `5 + 5` ?
- A. `10` et `10`
- B. `"55"` et `"55"`
- C. `"55"` et `10`
- D. une erreur dans les deux cas

---

## Partie C — Au-delà du plancher (confirmé)

*Ces questions ne sont pas requises pour suivre ; elles aident à repérer les profils avancés.*

**Q12.** Quelle est la différence principale entre `yield` et `return` dans une fonction ?
- A. Aucune, ce sont des synonymes
- B. `yield` produit des valeurs paresseusement (générateur), `return` rend une valeur et termine
- C. `yield` est plus rapide
- D. `yield` n'existe que dans les classes

**Q13.** À quoi sert un décorateur, par exemple `@functools.cache` au-dessus d'une fonction ?
- A. À commenter la fonction
- B. À envelopper la fonction pour modifier ou compléter son comportement
- C. À la rendre privée
- D. À la documenter automatiquement

**Q14.** Dans `def probe(url: str) -> bool:`, que représentent `: str` et `-> bool` ?
- A. Des contraintes vérifiées à l'exécution qui lèvent une erreur si violées
- B. Des annotations de type, indicatives, non imposées au runtime par défaut
- C. Des valeurs par défaut
- D. Des commentaires ignorés par tout outil

**Q15.** Que permettent `*args` et `**kwargs` dans une signature de fonction ?
- A. De recevoir un nombre variable d'arguments positionnels et nommés
- B. De multiplier les arguments
- C. De rendre les arguments obligatoires
- D. Rien, c'est une erreur de syntaxe

---

## Grille d'interprétation

Compter 1 point par bonne réponse, puis lire le **profil**. La réussite des **questions 1 à 6**
prime sur le score total.

**Échec d'une ou plusieurs questions de la Partie A (Q1–Q6), ou score total < 6/15 → sous le plancher.**
La formation ira trop vite. Le bon préalable est un module « Python fondamentaux » avant de
rejoindre ce parcours. À signaler à l'organisation : inscrire cette personne en l'état lui
rendrait un mauvais service.

**Partie A réussie et score total entre 6 et 10/15 → au niveau attendu.**
C'est le profil cible. Le **parcours de pré-travail J0** comblera les points encore flous
(exceptions, compréhensions, fichiers) avant le premier jour.

**Score total ≥ 11/15, Partie C en grande partie réussie → profil confirmé.**
Le pré-travail sera une révision rapide. Viser systématiquement les **extensions** des labs
pour rester engagé.

> **Lecture côté formateur — détecter la bimodalité.** Si la distribution du groupe se scinde
> nettement (une part sous 8, une part au-dessus de 12), un compromis unique mécontentera les
> deux bords : envisager **deux sessions distinctes** plutôt qu'un rythme moyen.

