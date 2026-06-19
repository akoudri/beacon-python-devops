from dataclasses import dataclass
from typing import Any
from botocore.exceptions import ClientError
from datetime import datetime, timezone

STATE_UNKNOWN = "unknown"

@dataclass
class ResourceState:
    """Etat d'une ressource Cloud"""

    resource_id : str
    state : str
    checked_at : str


def probe_cloud(client : Any, resource_id : str) -> ResourceState:
    try:
        response = client.describe_instances(InstanceIds=[resource_id])
        state = _extract_state(response)
    except ClientError:
        state = STATE_UNKNOWN

    return ResourceState(
        resource_id=resource_id,
        state=state,
        checked_at=datetime.now(timezone.utc).isoformat()
    )


def _extract_state(response: dict[str, Any]) -> str:
    for reservation in response.get("Reservations", []):
        for instance in reservation.get("Instances", []):
            return str(instance["State"]["Name"])
    return STATE_UNKNOWN