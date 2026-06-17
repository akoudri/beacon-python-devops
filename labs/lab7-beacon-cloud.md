# Lab 7 — Beacon regarde le cloud

**Durée :** ~45 min · **Mode :** auto-rythmé
**Module Beacon visé :** lecture de l'état cloud (`probe_cloud`)

---

## Contexte

Beacon sait sonder le réseau. Il va maintenant remonter l'état de **ressources cloud** via
un SDK, et l'intégrer à son rapport — au même titre que ses sondes réseau. Point important :
Beacon **lit** l'infrastructure ; il ne la provisionne pas (ça, c'est Terraform).

L'exemple est pris sur AWS (boto3) ; la logique se transpose à Azure et GCP.

## Prérequis

- `pip install boto3 moto`.
- **Aucun compte cloud requis pour le socle** : les tests s'appuient sur `moto`, qui simule
  les services AWS en mémoire.

---

## SOCLE — à réaliser par tous

### Énoncé

1. Initialiser un client SDK proprement, **sans clé en dur** (le SDK résout les credentials
   via l'environnement, un profil ou un rôle).
2. Écrire `probe_cloud(client, resource_id)` qui :
   - interroge l'état d'une ressource (par ex. l'état d'une instance) ;
   - renvoie un objet structuré `ResourceState(resource_id, state, checked_at)`,
     dans le même esprit que `ProbeResult` ;
   - traite le cas « ressource introuvable » par un état explicite (`unknown`), pas une
     exception remontée.
3. Intégrer ces états au rapport agrégé de Beacon, à côté des sondes réseau.
4. Écrire un test sous `@mock_aws` (moto) : créer une ressource fictive, la sonder,
   asserter l'état remonté — **sans aucun appel réel**.

### Critères de réussite (socle)

- [ ] Aucun credential n'apparaît dans le code.
- [ ] `probe_cloud` renvoie un `ResourceState`, jamais une exception brute.
- [ ] Le test moto passe sans compte ni réseau, en quelques dizaines de millisecondes.
- [ ] L'état cloud apparaît dans le rapport unifié de Beacon.

---

## EXTENSION — pour aller plus loin

1. **Pagination.** Sur de gros volumes, utiliser un paginator plutôt que de tout charger d'un coup.
2. **Filtrage côté API.** Restreindre par tag via les `Filters` du SDK, au lieu de filtrer en Python.
3. **Permissions.** Gérer proprement une erreur d'autorisation (`ClientError`) : la signaler
   sans faire échouer toute la collecte.
4. **Compte réel.** Pour qui dispose d'un environnement sandbox : exécuter la même sonde
   contre un vrai service, en lecture seule.

---

## Pièges & indices

- Ne pas filtrer en Python ce que l'API sait filtrer : `Filters` réduit le volume transféré
  et le temps de traitement.
- `moto` se règle au niveau du test (`@mock_aws`) : à l'intérieur, tout appel boto3 est
  intercepté. Inutile de modifier le code de production.
- Garder `probe_cloud` cohérent avec les sondes réseau : un état structuré, pas une chaîne libre.
- En production, privilégier un **rôle** plutôt qu'une clé : aucun secret à gérer du tout.

## Livrable

- `probe_cloud` + son test moto, état cloud intégré au rapport.
- Conserver l'ensemble : le Lab 8 déploie Beacon sur un hôte via Ansible.
