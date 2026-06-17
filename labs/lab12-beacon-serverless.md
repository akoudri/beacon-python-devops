# Lab 12 — Beacon serverless (optionnel)

**Durée :** ~40 min · **Mode :** auto-rythmé
**Statut :** lab optionnel — sert de soupape selon le rythme du groupe

---

## Contexte

Une sonde courte et périodique est un cas d'usage typique du serverless : aucune machine à
maintenir, exécution sur planning, facturation à l'usage. Ce lab porte le cœur de Beacon dans
une **fonction** déclenchée régulièrement. C'est aussi la démonstration du dividende du J1 :
un code bien structuré se réutilise tel quel, seul le point d'entrée change.

> Ce lab est explicitement la **variable d'ajustement** de la formation : il s'aborde si le
> groupe a tenu le rythme, sinon le temps sert à consolider les labs précédents.

## Prérequis

- Le cœur de Beacon (`load_config`, `probe_http`) des jours précédents.
- Un accès à une plateforme serverless (AWS Lambda, Google Cloud Functions…), ou un
  émulateur local.

---

## SOCLE — à réaliser par tous

### Énoncé

1. Écrire un `handler(event, context)` qui **réutilise** le cœur de Beacon : charger la
   config, sonder les cibles, publier ou retourner un résumé.
2. Déployer ce handler comme une fonction.
3. La déclencher **périodiquement** (planning), pas seulement à la main.
4. Vérifier les logs d'exécution côté plateforme.

### Critères de réussite (socle)

- [ ] Le handler n'a pas réécrit la logique : il appelle `load_config` et `probe_http`.
- [ ] La fonction se déploie et s'exécute.
- [ ] Le déclenchement périodique est en place.
- [ ] Les logs d'exécution sont consultables.

---

## EXTENSION — pour aller plus loin

1. **Packaging des dépendances.** Embarquer les dépendances proprement (zip ou layer),
   de façon reproductible.
2. **Secrets.** Fournir le token via la configuration de la fonction, jamais en dur.
3. **Publication du résultat.** Écrire le résultat quelque part d'exploitable (stockage,
   file, alerte).
4. **Cold start.** Mesurer l'impact du démarrage à froid et l'atténuer (init hors handler,
   dépendances légères).

---

## Pièges & indices

- Le bénéfice du code structuré se vérifie ici : si le handler doit réécrire la logique de
  sonde, c'est que le découpage du J1 n'était pas assez net. Le handler ne fait que **câbler**.
- Garder l'initialisation coûteuse (clients, config statique) **hors** du handler, exécutée
  une fois, pour limiter le cold start.
- Penser idempotence : une réexécution (rejeu d'un événement) ne doit pas produire d'effet de
  bord indésirable.

## Livrable

- Un handler serverless réutilisant le cœur de Beacon, déclenché périodiquement.
- C'est le dernier maillon : Beacon a parcouru tout le chemin, du script local au service
  packagé, testé, déployé, observé, intégré en CI, et — désormais — exécutable sans serveur.
