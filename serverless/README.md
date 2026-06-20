# Beacon en serverless

Le handler [`beacon.serverless.handler`](../beacon/serverless.py) réutilise le
cœur de Beacon — il ne réécrit aucune logique de sonde.

## Invocation locale

```bash
BEACON_CONFIG=config/targets.yaml \
  python -c "from beacon.serverless import handler; print(handler({}, None))"
```

## Déploiement (AWS SAM)

`template.yaml` déclare la fonction et un déclenchement périodique
(`rate(5 minutes)`) :

```bash
sam build
sam deploy --guided
```

Les logs d'exécution sont consultables côté plateforme (CloudWatch Logs).

## Points clés

- **Réutilisation** : `load_config` + `probe_all`, inchangés depuis le J1.
- **Cold start** : la config est lue une fois (hors handler), puis réutilisée.
- **Secrets** : le token vient de la configuration de la fonction (paramètre ou
  gestionnaire de secrets), jamais en dur.
