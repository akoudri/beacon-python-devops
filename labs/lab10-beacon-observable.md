# Lab 10 — Beacon observable

**Durée :** ~45 min · **Mode :** auto-rythmé
**Objet :** logs structurés + métriques exposées

---

## Contexte

Un service en production doit pouvoir être interrogé sur ce qu'il fait. Ce lab rend Beacon
**observable** : des logs structurés exploitables, et des métriques exposées sur un endpoint
`/metrics`. Cadrage essentiel : Beacon **expose** des métriques brutes ; ce sont Prometheus
(collecte) et Grafana (affichage) qui les exploitent. On ne construit pas de tableau de bord
en Python.

## Prérequis

- `pip install prometheus-client`.
- Le cœur de Beacon (sondes) des modules précédents.

---

## SOCLE — à réaliser par tous

### Énoncé

1. **Logs structurés.** Remplacer tout `print` par le module `logging` :
   - un logger nommé (`beacon`) ;
   - un événement par sonde, avec le contexte en champs (cible, statut, latence) ;
   - des niveaux cohérents (`info` / `warning` / `error`) ;
   - **aucun secret** journalisé.
2. **Métriques.** Avec `prometheus_client` :
   - un `Counter` du nombre de sondes, labellisé par statut ;
   - un `Histogram` des latences ;
   - alimenter ces métriques à chaque sonde.
3. **Exposition.** Démarrer le serveur de métriques (`start_http_server`) et vérifier que
   `GET /metrics` renvoie bien les compteurs et l'histogramme attendus.

### Critères de réussite (socle)

- [ ] Plus aucun `print` : les événements passent par `logging`.
- [ ] `/metrics` expose `beacon_probes_total` (par statut) et l'histogramme de latence.
- [ ] Les métriques évoluent de façon cohérente après plusieurs sondes.
- [ ] Aucun secret n'apparaît dans les logs ni dans les métriques.

---

## EXTENSION — pour aller plus loin

1. **Labels pertinents.** Ajouter des dimensions utiles (par cible, par type de sonde) sans
   exploser la cardinalité.
2. **Gauge.** Exposer `beacon_targets_up`, valeur instantanée recalculée à chaque cycle.
3. **Logs JSON.** Brancher un formatter qui émet chaque ligne en JSON, prête pour une stack de logs.
4. **Survol OpenTelemetry.** Explorer comment des traces compléteraient logs et métriques.

---

## Pièges & indices

- `Counter` ne fait que croître ; pour une valeur qui monte et descend (cibles up), c'est une
  `Gauge`. Pour une distribution (latence), un `Histogram`.
- Attention à la **cardinalité** des labels : un label à forte variabilité (une URL complète,
  un identifiant) fait exploser le nombre de séries.
- Le logging structuré n'est pas qu'esthétique : c'est ce qui rend les logs **requêtables**.
  Un message libre n'est pas exploitable à grande échelle.
- `/metrics` ne « montre » rien à un humain : c'est une surface machine, scrutée par Prometheus.

## Livrable

- Beacon doté de logs structurés et d'un `/metrics` fonctionnel.
- Beacon est désormais conteneurisé **et** observable. Plus tard, un pipeline CI vérifiera
  sa qualité et construira son image automatiquement à chaque changement.
