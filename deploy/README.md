# Déploiement de Beacon (Ansible)

Playbook idempotent qui installe Beacon, dépose sa configuration et planifie la
sonde périodique sur les hôtes du groupe `monitors`.

## Prérequis

Construire le paquet **avant** de lancer le playbook (il copie le wheel sur
l'hôte) :

```bash
python -m build --wheel        # produit dist/beacon-0.1.0-py3-none-any.whl
```

## Lancer

```bash
cd deploy
ansible-playbook -i inventory.ini playbook.yml
```

Rejouer pour vérifier l'idempotence — la seconde exécution doit afficher
`changed=0` :

```bash
ansible-playbook -i inventory.ini playbook.yml
```

## Fichiers

| Fichier                     | Rôle                                                 |
| --------------------------- | ---------------------------------------------------- |
| `inventory.ini`             | Groupe `monitors` (ici `localhost`).                 |
| `group_vars/monitors.yml`   | Variables (chemins, planification cron).             |
| `playbook.yml`              | État désiré : install + config + cron.               |
| `library/beacon_status.py`  | Module custom (extension) : lit l'état via la CLI.   |

## Secrets

Aucun secret dans l'inventaire ni le playbook. Le token d'authentification est
fourni par l'environnement de l'hôte (ou Ansible Vault), jamais en clair.
