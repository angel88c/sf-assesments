from unittest.mock import Mock

import pytest
from requests.exceptions import Timeout

import services.salesforce_service as salesforce_service
from core.exceptions import SalesforceError
from services.salesforce_service import SalesforceService


def make_service(monkeypatch):
    """Build a service without loading application settings or credentials."""
    monkeypatch.setattr(salesforce_service, "get_settings", Mock())
    return SalesforceService()


def test_get_active_users_returns_id_to_name_mapping(monkeypatch):
    service = make_service(monkeypatch)
    client = Mock()
    client.query_all.return_value = {
        "records": [{"Id": "005A", "Name": "Ana Garcia"}]
    }
    monkeypatch.setattr(service, "_sf_client", client)

    assert service.get_active_users() == {"005A": "Ana Garcia"}
    client.query_all.assert_called_once_with(
        "SELECT Id, Name FROM User WHERE IsActive = true ORDER BY Name ASC"
    )


def test_get_active_user_dict_returns_empty_mapping_when_lookup_fails(monkeypatch):
    service = make_service(monkeypatch)
    client = Mock()
    client.query_all.side_effect = RuntimeError("Salesforce User lookup failed")
    monkeypatch.setattr(service, "_sf_client", client)
    monkeypatch.setattr(salesforce_service, "get_salesforce_service", lambda: service)
    salesforce_service.get_active_user_dict.clear()

    assert salesforce_service.get_active_user_dict() == {}


def test_get_active_users_retries_timeout_then_returns_users(monkeypatch):
    service = make_service(monkeypatch)
    client = Mock()
    client.query_all.side_effect = [
        Timeout("temporary timeout"),
        {"records": [{"Id": "005A", "Name": "Ana Garcia"}]},
    ]
    monkeypatch.setattr(service, "_sf_client", client)
    monkeypatch.setattr(salesforce_service.time, "sleep", lambda _: None)

    assert service.get_active_users() == {"005A": "Ana Garcia"}
    assert client.query_all.call_count == 2


def test_get_active_user_dict_returns_empty_mapping_after_retry_exhaustion(monkeypatch):
    service = make_service(monkeypatch)
    client = Mock()
    client.query_all.side_effect = Timeout("persistent timeout")
    monkeypatch.setattr(service, "_sf_client", client)
    monkeypatch.setattr(salesforce_service, "get_salesforce_service", lambda: service)
    monkeypatch.setattr(salesforce_service.time, "sleep", lambda _: None)
    salesforce_service.get_active_user_dict.clear()

    assert salesforce_service.get_active_user_dict() == {}
    assert client.query_all.call_count == 4


def test_create_opportunity_sends_selected_owner_id(monkeypatch):
    service = make_service(monkeypatch)
    client = Mock()
    client.Opportunity.create.return_value = {"success": True, "id": "006A"}
    monkeypatch.setattr(service, "_sf_client", client)

    service.create_opportunity(
        name="Project A", stage_name="New Request", close_date="2026-08-31",
        assessment_date="2026-07-28", path="https://example.test/project",
        bu="ICT", account_id="001A", owner_id="005A",
    )

    assert client.Opportunity.create.call_args.args[0]["OwnerId"] == "005A"


@pytest.mark.parametrize("owner_id", [None, "", "   "])
def test_create_opportunity_rejects_blank_owner_without_calling_salesforce(
    monkeypatch, owner_id
):
    service = make_service(monkeypatch)
    client = Mock()
    monkeypatch.setattr(service, "_sf_client", client)

    with pytest.raises(SalesforceError, match="owner"):
        service.create_opportunity(
            name="Project A",
            stage_name="New Request",
            close_date="2026-08-31",
            assessment_date="2026-07-28",
            path="https://example.test/project",
            bu="ICT",
            owner_id=owner_id,
        )

    client.Opportunity.create.assert_not_called()
