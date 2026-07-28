from unittest.mock import Mock

import pytest

from pages.utils.base_assessment_refactored import BaseAssessment, get_owner_options


def make_assessment(assessment_type, *, owner_selection_enabled=True):
    assessment = BaseAssessment.__new__(BaseAssessment)
    assessment.assessment_type = assessment_type
    assessment.owner_selection_enabled = owner_selection_enabled
    assessment.info = {"project_name": "Project A", "owner_id": "005A"}
    assessment.salesforce_service = Mock()
    assessment._get_sharepoint_url = Mock(return_value="https://example.test/project")
    return assessment


@pytest.mark.parametrize("assessment_type", ["ICT", "IAT", "FCT"])
def test_supported_assessments_forward_selected_owner(monkeypatch, assessment_type):
    assessment = make_assessment(assessment_type)
    monkeypatch.setattr(
        "pages.utils.base_assessment_refactored.get_unique_account_dict",
        lambda: {"001A": "ACME"},
    )

    assessment._create_salesforce_opportunity(
        {"customer_in_list": True, "customer_name": "ACME"}, "project-path"
    )

    assert assessment.salesforce_service.create_opportunity.call_args.kwargs["owner_id"] == "005A"


def test_duplicate_user_names_have_distinct_labels_and_keep_all_ids():
    assert get_owner_options(
        {"005A": "Ana Garcia", "005B": "Ana Garcia", "005C": "Ben Li"}
    ) == {"Ana Garcia (005A)": "005A", "Ana Garcia (005B)": "005B", "Ben Li": "005C"}


def test_fix_assessment_does_not_forward_or_require_owner(monkeypatch):
    assessment = make_assessment("IAT", owner_selection_enabled=False)
    assessment.info.pop("owner_id")
    monkeypatch.setattr(
        "pages.utils.base_assessment_refactored.get_unique_account_dict",
        lambda: {"001A": "ACME"},
    )

    assessment._validate_form_data = BaseAssessment._validate_form_data.__get__(assessment)
    assessment.info.update(
        {
            "contact_name": "Ana Garcia",
            "date": "2026-07-28",
            "contact_email": "ana@acme.com",
            "customer_name": "ACME",
        }
    )
    assessment._validate_form_data()
    assessment._create_salesforce_opportunity(
        {"customer_in_list": True, "customer_name": "ACME"}, "project-path"
    )

    kwargs = assessment.salesforce_service.create_opportunity.call_args.kwargs
    assert kwargs["allow_default_owner"] is True
    assert kwargs["owner_id"] is None


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
