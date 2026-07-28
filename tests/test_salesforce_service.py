from unittest.mock import Mock

from services.salesforce_service import SalesforceService


def test_get_active_users_returns_id_to_name_mapping(monkeypatch):
    service = SalesforceService()
    client = Mock()
    client.query_all.return_value = {
        "records": [{"Id": "005A", "Name": "Ana Garcia"}]
    }
    monkeypatch.setattr(service, "_sf_client", client)

    assert service.get_active_users() == {"005A": "Ana Garcia"}
    client.query_all.assert_called_once_with(
        "SELECT Id, Name FROM User WHERE IsActive = true ORDER BY Name ASC"
    )


def test_create_opportunity_sends_selected_owner_id(monkeypatch):
    service = SalesforceService()
    client = Mock()
    client.Opportunity.create.return_value = {"success": True, "id": "006A"}
    monkeypatch.setattr(service, "_sf_client", client)

    service.create_opportunity(
        name="Project A", stage_name="New Request", close_date="2026-08-31",
        assessment_date="2026-07-28", path="https://example.test/project",
        bu="ICT", account_id="001A", owner_id="005A",
    )

    assert client.Opportunity.create.call_args.args[0]["OwnerId"] == "005A"
