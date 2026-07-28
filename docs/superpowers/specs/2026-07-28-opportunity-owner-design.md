# Opportunity owner selection

## Goal

Allow the person submitting an ICT, IAT, or FCT assessment to select the Salesforce owner of the opportunity created by the application.

## Current behavior

The application creates an Opportunity without `OwnerId`. Salesforce therefore assigns the owner to the API-authenticated user (`acarreon`).

## Design

### Salesforce service

`SalesforceService` will expose a cached lookup of all active Salesforce `User` records. The lookup will query `Id` and `Name`, order by name, and return a mapping that lets the UI display a name while retaining the corresponding Salesforce ID.

`create_opportunity` will accept an `owner_id` argument and include it as `OwnerId` in the Opportunity payload. The argument is required by the shared assessment flow, so every newly created assessment opportunity has the owner explicitly selected.

### Assessment form

The shared refactored `BaseAssessment` form used by ICT, IAT, and FCT will add a mandatory `Opportunity Owner` select box. It will use the active-user lookup and store the selected user ID in `self.info`.

The selected ID will be passed unchanged through `_create_salesforce_opportunity` to `SalesforceService.create_opportunity`.

### Errors and caching

The active-owner lookup will be cached for a short period, consistent with the existing account lookup, to avoid querying Salesforce on every Streamlit rerun. Query or assignment failures will follow the existing Salesforce error path and be surfaced to the user; no fallback owner will be silently assigned.

## Scope

The change applies to ICT, IAT, and FCT through their common `pages/utils/base_assessment_refactored.py` base class. It does not alter account selection, authentication credentials, or existing Salesforce records.

## Verification

Tests will cover the active-user lookup, propagation of the selected `owner_id` into the Salesforce creation payload, and validation that the shared form passes the selected owner for all assessment types.
