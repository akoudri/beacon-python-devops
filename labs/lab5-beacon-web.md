# Lab 5 — Beacon sonde le web

**Durée :** ~45 min · **Mode :** auto-rythmé
**Module Beacon visé :** `probe.py` (sonde HTTP)

---

## Contexte

Jusqu'ici Beacon vérifie qu'un port TCP répond. Une sonde HTTP va plus loin : elle dit si
le **service** répond correctement (code de statut) et avec quelle latence applicative.
C'est l'information qui intéresse réellement l'exploitation.

Cible :

```python
def probe_http(target: Target) -> ProbeResult:
    ...
```

Le contrat de sortie (`ProbeResult`) ne change pas : le report et les futures métriques
restent inchangés.

## Prérequis

- `pip install httpx`.
- Une URL joignable pour tester (un `python -m http.server` local convient ;
  pour un endpoint qui renvoie un statut au choix, `httpbin` est pratique).

---

## SOCLE — à réaliser par tous

### Énoncé

1. Enrichir le `Target` d'un champ `url` (et, idéalement, `timeout`).
2. Écrire `probe_http(target)` qui :
   - démarre le chrono, émet un `GET` avec **timeout explicite** ;
   - considère `up` si le statut est `< 400`, sinon `down` ;
   - traduit toute `httpx.RequestError` (timeout, refus, DNS) en `down`,
     **sans laisser remonter l'exception** ;
   - calcule la latence en millisecondes et renvoie un `ProbeResult`.
3. Vérifier sur trois cas : service sain (2xx), service en erreur (5xx), hôte injoignable.
4. Agréger un mini-rapport : nombre de cibles `up` / `down`.

### Critères de réussite (socle)

- [ ] `probe_http` renvoie un `ProbeResult`, jamais une exception remontée.
- [ ] Un 5xx et un hôte injoignable donnent tous deux `down`, pour des raisons distinctes.
- [ ] La latence reportée est plausible.
- [ ] Le timeout est explicite (aucune sonde ne peut pendre indéfiniment).

---

## EXTENSION — pour aller plus loin

1. **Sondage concurrent.** Sonder N cibles en parallèle, via `httpx` en asynchrone ou
   `concurrent.futures.ThreadPoolExecutor`. Comparer le temps total au sondage séquentiel.
2. **Backoff.** Réessayer une fois après un court délai avant de conclure `down`.
3. **Vérification de contenu.** Au-delà du statut, valider qu'un endpoint `/health`
   renvoie le corps attendu.
4. **Statut `degraded`.** Distinguer `down` (réseau/erreur) d'un service joignable mais
   anormalement lent (latence au-dessus d'un seuil).

---

## Pièges & indices

- `raise_for_status()` lève sur 4xx/5xx : à attraper via `httpx.HTTPStatusError`, distinct
  des erreurs de transport (`httpx.RequestError`).
- Démarrer le chrono **avant** le `try` pour mesurer la latence même en échec rapide.
- Un `httpx.Client` réutilisé mutualise les connexions — utile dès qu'il y a plusieurs cibles.
- Garder `probe_http` sans effet de bord d'affichage : il renvoie une donnée, il n'imprime rien.

## Livrable

- `probe.py` enrichi d'une sonde HTTP, `Target` doté d'une `url`.
- Conserver l'ensemble : le Lab 6 ajoutera l'authentification, donc la gestion des secrets.
