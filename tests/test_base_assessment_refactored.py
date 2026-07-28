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


def test_process_submission_blocks_side_effects_when_owner_is_not_selected(monkeypatch):
    assessment = BaseAssessment.__new__(BaseAssessment)
    assessment.assessment_type = "ICT"
    assessment.info = {
        "project_name": "Project A",
        "contact_name": "Ana Garcia",
        "date": "2026-07-28",
        "contact_email": "ana@acme.com",
        "owner_id": None,
    }
    assessment._create_project_structure = Mock()
    assessment._save_html_report = Mock()
    assessment._create_salesforce_opportunity = Mock()
    error = Mock()
    monkeypatch.setattr("pages.utils.base_assessment_refactored.st.error", error)

    result = assessment.process_form_submission([], Mock())

    assert result is False
    assessment._create_project_structure.assert_not_called()
    assessment._save_html_report.assert_not_called()
    assessment._create_salesforce_opportunity.assert_not_called()
    error.assert_called_once_with("❌ Validation Error: An opportunity owner must be selected")


def test_process_submission_blocks_side_effects_when_active_user_lookup_is_empty(monkeypatch):
    assessment = BaseAssessment.__new__(BaseAssessment)
    assessment.assessment_type = "ICT"
    assessment.info = {
        "project_name": "Project A",
        "contact_name": "Ana Garcia",
        "date": "2026-07-28",
        "contact_email": "ana@acme.com",
    }
    assessment._create_project_structure = Mock()
    assessment._save_html_report = Mock()
    assessment._create_salesforce_opportunity = Mock()
    error = Mock()
    monkeypatch.setattr("pages.utils.base_assessment_refactored.st.error", error)

    result = assessment.process_form_submission([], Mock())

    assert result is False
    assessment._create_project_structure.assert_not_called()
    assessment._save_html_report.assert_not_called()
    assessment._create_salesforce_opportunity.assert_not_called()
    error.assert_called_once_with("❌ Validation Error: An opportunity owner must be selected")
