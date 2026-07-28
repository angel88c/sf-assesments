# Opportunity owner selection final-fix report

## Implemented findings

1. `SalesforceService.create_opportunity` now requires an `owner_id` argument
   for normal calls, rejects `None`, empty, and whitespace-only values before
   contacting Salesforce, and always includes `OwnerId` in normal payloads.
   `allow_default_owner=True` is an explicit legacy-only escape hatch.
2. Duplicate active-user names are retained.  Duplicate labels include the
   Salesforce ID (for example, `Ana Garcia (005A)`) and map to the correct ID.
3. Owner UI, validation, and propagation apply by default only to ICT, IAT, and
   FCT.  The FIX page explicitly opts out, preserving its legacy default-owner
   Salesforce request and its IAT business-unit value.
4. Salesforce unit tests patch `get_settings` before service construction and
   use mocked clients; they do not require real credentials or settings.
5. ICT, IAT, and FCT owner propagation are covered by one parametrized shared
   base-class test.

## Verification

Executed successfully:

```text
$ python3 -m py_compile services/salesforce_service.py pages/utils/base_assessment_refactored.py pages/fix_assessment.py
$ pytest tests/test_salesforce_service.py tests/test_base_assessment_refactored.py -v
============================== 15 passed in 0.43s ==============================
$ git diff --check
```

The attempted full `pytest -q` run could not collect the pre-existing
`test_sharepoint_access.py`: it performs live Azure tenant discovery and failed
with DNS resolution for `login.microsoftonline.com`.  This is external to the
owner-selection tests; no owner test contacts Salesforce, SharePoint, or Azure.

## Self-review

- Correctness: blank owners are rejected before `Opportunity.create`; selected
  owners are sent as `OwnerId`; duplicate names remain selectable.
- Scope: only the intended assessment forms select/require owners; FIX uses an
  explicit opt-out rather than an implicit fallback.
- Security: no credentials, secrets, or external requests were introduced.
- Performance: the existing cached active-user lookup remains one query per
  cache interval; label creation is linear in active users.
- Quality: focused diff check is clean; no unrelated worktree files were staged.

## Commit

`f7f60f26ad2864b4f2a78fc6f0232de414479154` (`fix: complete opportunity owner safeguards`)
