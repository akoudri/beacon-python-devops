"""Tests de la sonde cloud sous moto : aucun appel AWS réel."""

import boto3
import pytest
from moto import mock_aws

from beacon.cloud import ResourceState, probe_cloud
from beacon.probe import ProbeResult
from beacon.report import build_report

# AMI factice reconnue par moto (région eu-west-3).
_FAKE_AMI = "ami-12345678"
_REGION = "eu-west-3"


@mock_aws
def test_probe_cloud_known_instance() -> None:
    ec2 = boto3.client("ec2", region_name=_REGION)
    reservation = ec2.run_instances(ImageId=_FAKE_AMI, MinCount=1, MaxCount=1)
    instance_id = reservation["Instances"][0]["InstanceId"]

    state = probe_cloud(ec2, instance_id)
    assert isinstance(state, ResourceState)
    assert state.resource_id == instance_id
    assert state.state == "running"


@mock_aws
def test_probe_cloud_unknown_instance_returns_unknown() -> None:
    ec2 = boto3.client("ec2", region_name=_REGION)
    state = probe_cloud(ec2, "i-doesnotexist0000")
    # Ressource introuvable -> état explicite, pas d'exception remontée.
    assert state.state == "unknown"


@mock_aws
def test_cloud_state_in_unified_report() -> None:
    ec2 = boto3.client("ec2", region_name=_REGION)
    reservation = ec2.run_instances(ImageId=_FAKE_AMI, MinCount=1, MaxCount=1)
    instance_id = reservation["Instances"][0]["InstanceId"]
    state = probe_cloud(ec2, instance_id)

    probes = [ProbeResult("api", "up", 1.0, "t")]
    report = build_report(probes, [state])

    assert report["cloud"]["total"] == 1
    assert report["cloud"]["results"][0]["state"] == "running"
    assert report["probes"]["up"] == 1
