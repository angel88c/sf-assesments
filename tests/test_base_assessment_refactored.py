from unittest.mock import Mock

from pages.utils.base_assessment_refactored import BaseAssessment


def test_create_opportunity_forwards_selected_owner(monkeypatch):
    assessment = BaseAssessment.__new__(BaseAssessment)
    assessment.info = {"project_name": "Project A", "owner_id": "005A"}
    assessment.assessment_type = "ICT"
    assessment.salesforce_service = Mock()
    assessment._get_sharepoint_url = Mock(return_value="https://example.test/project")
    monkeypatch.setattr(
        "pages.utils.base_assessment_refactored.get_unique_account_dict",
        lambda: {"001A": "ACME"},
    )

    assessment._create_salesforce_opportunity(
        {"customer_in_list": True, "customer_name": "ACME"}, "project-path"
    )

    assert assessment.salesforce_service.create_opportunity.call_args.kwargs["owner_id"] == "005A"
