# Opportunity Owner Selection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let users select any active Salesforce user as owner of every opportunity created from ICT, IAT, or FCT.

**Architecture:** Add an active-user query and cached lookup to the Salesforce service. The shared refactored assessment form renders a mandatory selector from that lookup and forwards the selected User ID to the service, which sends it as `OwnerId`.

**Tech Stack:** Python 3, Streamlit, simple-salesforce, pytest, unittest.mock.

## Global Constraints

- Query only `User` records where `IsActive = true`, ordered by `Name`.
- Show names in the selector and transmit Salesforce User IDs.
- Never substitute the API-authenticated owner on a user-query or assignment failure.
- Change only the shared refactored base class, which covers ICT, IAT, and FCT.

---

## File Structure

- Modify `services/salesforce_service.py`: active-user lookup, its cache wrapper, and `OwnerId` payload support.
- Modify `pages/utils/base_assessment_refactored.py`: mandatory selector and owner propagation.
- Create `tests/test_salesforce_service.py`: unit tests for the Salesforce query and payload.
- Create `tests/test_base_assessment_refactored.py`: shared-flow owner propagation test.

### Task 1: Add the Salesforce owner lookup and API payload

**Files:**

- Modify: `services/salesforce_service.py:140-260`
- Create: `tests/test_salesforce_service.py`

**Interfaces:**

- Produces `SalesforceService.get_active_users() -> Dict[str, str]`, mapping User ID to name.
- Produces cached `get_active_user_dict() -> Dict[str, str]`, returning `{}` if the Salesforce lookup fails.
- Changes `create_opportunity(..., account_id: Optional[str] = None, owner_id: Optional[str] = None) -> Dict`.

- [ ] **Step 1: Write failing tests**

```python
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
```

- [ ] **Step 2: Confirm the tests fail**

Run: `pytest tests/test_salesforce_service.py -v`

Expected: FAIL because `get_active_users` and the `owner_id` parameter do not exist.

- [ ] **Step 3: Implement the query, cache wrapper, and payload field**

Add this retry-protected method beside `get_accounts`:

```python
@retry_on_timeout(max_retries=3, base_delay=2.0, max_delay=30.0)
def get_active_users(self) -> Dict[str, str]:
    query = "SELECT Id, Name FROM User WHERE IsActive = true ORDER BY Name ASC"
    result = self.client.query_all(query)
    return {record["Id"]: record["Name"] for record in result["records"]}
```

Extend `create_opportunity` with `owner_id: Optional[str] = None` and, after the existing account block, add:

```python
if owner_id:
    opportunity_data["OwnerId"] = owner_id
```

Add this module-level wrapper beside `get_unique_account_dict`:

```python
@st.cache_data(ttl=600)
def get_active_user_dict() -> Dict[str, str]:
    try:
        return get_salesforce_service().get_active_users()
    except SalesforceError as error:
        logger.error("Failed to get active Salesforce users: %s", error)
        return {}
```

- [ ] **Step 4: Confirm the tests pass**

Run: `pytest tests/test_salesforce_service.py -v`

Expected: PASS; the query filters active users and the request payload contains `OwnerId`.

- [ ] **Step 5: Commit the completed task**

```bash
git add services/salesforce_service.py tests/test_salesforce_service.py
git commit -m "feat: support selected Salesforce opportunity owner"
```

### Task 2: Render the shared selector and forward its value

**Files:**

- Modify: `pages/utils/base_assessment_refactored.py:18, 75-140, 290-335`
- Create: `tests/test_base_assessment_refactored.py`

**Interfaces:**

- Consumes `get_active_user_dict() -> Dict[str, str]`.
- Consumes `SalesforceService.create_opportunity(..., owner_id: Optional[str]) -> Dict`.
- Produces `self.info["owner_id"]`, the selected Salesforce User ID.

- [ ] **Step 1: Write the failing propagation test**

```python
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
```

- [ ] **Step 2: Confirm the test fails**

Run: `pytest tests/test_base_assessment_refactored.py -v`

Expected: FAIL because the shared creation method does not forward `owner_id`.

- [ ] **Step 3: Add the required shared selector**

Import `get_active_user_dict` beside `get_unique_account_dict`. In `create_customer_info_section`, build the selector from the active-user map:

```python
active_users = get_active_user_dict()
users_by_name = {name: user_id for user_id, name in active_users.items()}
self.info["owner_id"] = st.selectbox(
    r"*Opportunity Owner",
    options=list(users_by_name.keys()),
    index=None,
    placeholder="Select an owner",
)
if self.info["owner_id"]:
    self.info["owner_id"] = users_by_name[self.info["owner_id"]]
```

Put it inside the existing shared customer-information container. When the lookup is empty, show `st.error("Unable to load active Salesforce users. Please try again.")` and leave the owner unset. In `_create_salesforce_opportunity`, pass `owner_id=self.info["owner_id"]` to `create_opportunity`.

- [ ] **Step 4: Confirm the targeted tests pass**

Run: `pytest tests/test_salesforce_service.py tests/test_base_assessment_refactored.py -v`

Expected: PASS; the selected user ID reaches the Salesforce payload as `OwnerId`.

- [ ] **Step 5: Commit the completed task**

```bash
git add pages/utils/base_assessment_refactored.py tests/test_base_assessment_refactored.py
git commit -m "feat: add opportunity owner selector to assessments"
```

### Task 3: Regression verification

**Files:**

- Modify: none
- Test: `tests/test_salesforce_service.py`, `tests/test_base_assessment_refactored.py`

**Interfaces:**

- Consumes the service and shared assessment interfaces from Tasks 1 and 2.
- Produces verified owner assignment for ICT, IAT, and FCT through their common base class.

- [ ] **Step 1: Run the regression suite**

Run: `pytest tests/test_salesforce_service.py tests/test_base_assessment_refactored.py -v`

Expected: PASS without Salesforce, SharePoint, or credentials.

- [ ] **Step 2: Check syntax**

Run: `python -m py_compile services/salesforce_service.py pages/utils/base_assessment_refactored.py`

Expected: exit code 0.

- [ ] **Step 3: Inspect the final worktree**

Run: `git diff --check HEAD~2..HEAD && git status --short`

Expected: no whitespace errors; unrelated existing changes remain untouched.
