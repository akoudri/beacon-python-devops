# Lab 6 — Beacon gère ses secrets

**Durée :** ~45 min · **Mode :** auto-rythmé
**Module Beacon visé :** sonde authentifiée + gestion des credentials

---

## Contexte

Sonder une cible protégée exige un token d'authentification. Ce lab introduit ce credential
**sans jamais l'inscrire dans le code ni dans le dépôt** : il est fourni par l'environnement,
puis injecté dans l'en-tête de la requête. Le second objectif est de garantir qu'aucun secret
ne fuit dans les logs.

## Prérequis

- La sonde HTTP du Lab 5.
- Une cible nécessitant un en-tête `Authorization` (un endpoint protégé, ou simulé).

---

## SOCLE — à réaliser par tous

### Énoncé

1. Lire le token depuis l'environnement, en traitant son absence comme une erreur claire :

   ```python
   token = os.environ["BEACON_TOKEN"]   # KeyError explicite si absent
   ```

2. Construire l'en-tête et sonder la cible authentifiée :

   ```python
   headers = {"Authorization": f"Bearer {token}"}
   r = httpx.get(target.url, headers=headers, timeout=5.0)
   ```

3. Vérifier que **rien** ne fuit : ni `print(token)`, ni token dans une URL loggée, ni dans
   un message d'erreur.
4. Exporter le token dans l'environnement (`export BEACON_TOKEN=...`) avant de lancer Beacon,
   et constater que le code n'en contient aucune trace.

### Critères de réussite (socle)

- [ ] Beacon sonde une cible authentifiée avec un token lu dans l'environnement.
- [ ] Aucun secret n'apparaît dans le code source ni dans le dépôt.
- [ ] L'absence du token produit une erreur claire au démarrage, pas un échec obscur plus tard.
- [ ] Aucune sortie (logs, erreurs) ne révèle le token.

---

## EXTENSION — pour aller plus loin

1. **Hiérarchie de configuration.** Résoudre chaque paramètre selon l'ordre
   `défauts < fichier < variables d'environnement < arguments CLI`, et documenter la
   précédence.
2. **Redaction.** Écrire une fonction qui masque les secrets dans tout message journalisé
   (`Bearer ****`), et l'appliquer systématiquement.
3. **Support `.env` en développement.** Charger un `.env` via `python-dotenv` **uniquement**
   en dev ; vérifier qu'il figure bien dans `.gitignore`.
4. **`.env.example`.** Fournir un gabarit sans valeurs, versionné, documentant les clés
   attendues.

---

## Pièges & indices

- Préférer `os.environ["CLE"]` (et son `KeyError`) à `.get()` pour un secret **requis** :
  l'échec doit être immédiat et explicite.
- Le danger le plus courant n'est pas le code mais les **logs** : un token inséré dans une URL
  ou un objet journalisé fuit aussi sûrement qu'un secret commité.
- En production, ni `.env` ni valeur en dur : l'environnement provient de l'orchestrateur ou
  d'un gestionnaire de secrets (vu en cours). Le code, lui, reste identique.

## Livrable

- Sonde authentifiée fonctionnelle, aucun secret dans le dépôt.
- Beacon sait désormais sortir de la machine **proprement** : réseau réel et credentials
  maîtrisés. Plus tard, il interrogera le cloud et se déploiera via Ansible.
