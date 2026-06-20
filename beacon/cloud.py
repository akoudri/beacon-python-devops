"""Lecture de l'état de ressources cloud.

Beacon **lit** l'infrastructure (il ne la provisionne pas — ça, c'est
Terraform). L'exemple porte sur l'état d'une instance EC2 via boto3 ; la
logique se transpose à Azure et GCP.

Aucune clé n'est inscrite ici : le SDK résout ses credentials via
l'environnement, un profil ou un rôle. En production, on privilégie un rôle —
aucun secret à gérer.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from botocore.exceptions import ClientError

STATE_UNKNOWN = "unknown"


@dataclass
class ResourceState:
    """État d'une ressource cloud, dans le même esprit que `ProbeResult`."""

    resource_id: str
    state: str  # ex. "running" | "stopped" | "unknown"
    checked_at: str  # horodatage ISO 8601 (UTC)


def probe_cloud(client: Any, resource_id: str) -> ResourceState:
    """Interroge l'état d'une instance EC2 et renvoie un `ResourceState`.

    Une ressource introuvable (ou une erreur d'autorisation) produit un état
    explicite `unknown`, jamais une exception remontée : une ressource manquante
    ne doit pas faire échouer toute la collecte.
    """
    try:
        response = client.describe_instances(InstanceIds=[resource_id])
        state = _extract_state(response)
    except ClientError:
        # Ressource introuvable, ou permission insuffisante : état indéterminé.
        state = STATE_UNKNOWN

    return ResourceState(
        resource_id=resource_id,
        state=state,
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


def _extract_state(response: dict[str, Any]) -> str:
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            return str(instance["State"]["Name"])
    return STATE_UNKNOWN
