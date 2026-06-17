# Lab 8 — Déployer Beacon

**Durée :** ~45 min · **Mode :** auto-rythmé
**Objet :** déploiement et planification via Ansible

---

## Contexte

Beacon est un outil complet, mais il vit encore sur le poste de développement. Ce lab le
déploie sur un hôte cible et l'y planifie, à l'aide d'un **playbook Ansible** — déclaratif et
idempotent. C'est aussi l'occasion de toucher au seul vrai pont profond entre Python et le
config management : les modules custom.

## Prérequis

- Ansible installé sur le poste de contrôle.
- Un hôte cible accessible en SSH : une VM, ou un simple conteneur faisant office d'hôte.

---

## SOCLE — à réaliser par tous

### Énoncé

1. Définir un inventaire minimal avec un groupe `monitors` pointant l'hôte cible.
2. Écrire un playbook qui :
   - installe Beacon sur l'hôte (module `pip`, ou dépôt du paquet) ;
   - dépose le fichier de configuration des cibles à un emplacement standard ;
   - planifie l'exécution périodique de `beacon check` (module `cron`).
3. Exécuter le playbook, puis **le rejouer** : la seconde exécution ne doit signaler aucun
   changement (idempotence vérifiée).

### Critères de réussite (socle)

- [ ] Le playbook installe Beacon et planifie la sonde sur l'hôte cible.
- [ ] Une seconde exécution rapporte `changed=0` : l'idempotence est acquise.
- [ ] La configuration est déposée de façon déclarative, pas par script impératif.
- [ ] Aucun secret n'est inscrit dans le playbook ni dans l'inventaire versionné.

---

## EXTENSION — pour aller plus loin

1. **Module ou filtre custom.** Écrire un petit module Ansible (ou un filtre) en Python, et
   l'utiliser dans le playbook. Observer où Python entre réellement dans Ansible.
2. **Secrets côté hôte.** Fournir le token d'authentification via l'environnement de l'hôte
   (ou Ansible Vault), jamais en clair dans le playbook.
3. **Paramétrage par inventaire.** Externaliser les valeurs (intervalle, chemin de config)
   en variables de groupe/hôte.
4. **Plusieurs hôtes.** Étendre le groupe `monitors` à plusieurs cibles et déployer en une passe.

---

## Pièges & indices

- Penser **état désiré**, pas procédure : on décrit ce qui doit être vrai sur l'hôte, et
  Ansible converge. C'est ce qui rend le rejouage sûr.
- L'idempotence est la propriété à vérifier : un playbook qui « refait tout » à chaque
  exécution est un playbook à corriger.
- Un module Ansible custom est un programme Python qui lit des arguments et renvoie un résultat
  JSON via `exit_json` — c'est le point de jonction réel entre les deux mondes.
- Le YAML du playbook **n'est pas** du Python, et c'est voulu : le déclaratif reste déclaratif.

## Livrable

- Inventaire + playbook déployant et planifiant Beacon, idempotents.
- Beacon est désormais structuré, testé, packagé, observant le réseau et le cloud, **et
  déployé**. Les prochains modules le mettront en production : conteneur, métriques, logs et pipeline CI.
