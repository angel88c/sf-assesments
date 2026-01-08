"""
FCT Assessment Module

This module provides the Functional Test assessment functionality.
It extends the base assessment class with FCT-specific form fields and processing.
"""

import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

from pages.utils.global_styles import subtitle_h3
from pages.utils.base_assessment_refactored import BaseAssessment
from pages.utils.constants import (
    YES_NO, FCT_HARDWARE_OPTIONS, FCT_SYSTEM_TYPES, FCT_PROCESS_TYPES,
    FCT_PRODUCT_FINISH, FCT_TEST_STRATEGIES, FCT_FIXTURE_VENDORS,
    FCT_CONNECTION_INTERFACES, FCT_STATION_TYPES, FCT_STUDIES_OPTIONS, FCT_FILE_TYPES
)
from pages.utils.fct_create_html import json_to_html
from pages.utils.auth import require_authentication
    

def _render_milestones_section(info):
    with st.container(border=True):
        subtitle_h3("Milestones")
        col1, col2 = st.columns([1, 1.5])
        with col1:
            info['cad_files'] = st.radio(r'*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)', horizontal=True, options=YES_NO)
            info['gerber_files'] = st.radio(r'*Gerber Files', horizontal=True, options=YES_NO)
            info['schematics'] = st.radio(r'*Schematics', horizontal=True, options=YES_NO)
            info['boms'] = st.radio(r'*BOMs of each version', horizontal=True, options=YES_NO)
            info['traceability_system'] = st.radio(r'*Traceability System', horizontal=True, options=YES_NO)
            info['sow'] = st.radio(r'*SOW', horizontal=True, options=YES_NO)
            info["product_finish"] = st.selectbox(r"*Specify how the product will be test", FCT_PRODUCT_FINISH)
            info["test_strategy"] = st.selectbox(r"*Test strategy", FCT_TEST_STRATEGIES)
            info["connection_interface"] = st.selectbox(r"*Connection Interface", FCT_CONNECTION_INTERFACES)
        with col2:
            info['drawings'] = st.radio('Drawings (2D, 3D)', horizontal=True, options=YES_NO)
            info['test_spec'] = st.radio('Test Spec', horizontal=True, options=YES_NO)
            info['parallel_testing'] = st.radio('Parallel Testing?', horizontal=True, options=YES_NO)
            info['security_specification'] = st.radio('Security Specification', horizontal=True, options=YES_NO)
            info["traceability_system_name"] = st.text_input("Traceability System Name", placeholder="ITAC, MES, etc.")
            info["ergonomy_specifications"] = st.text_input("Ergonomy Specifications", placeholder='Ergonomy Specifications')
            info['osp_finish'] = st.radio('In the case of PCB, Does the product have OSP finish on TPs?', horizontal=True, index=1, options=YES_NO)
            info['quantity_uut'] = st.number_input(r"*How many units under test?", min_value=1)
            info['fixture_vendor'] = st.selectbox('Specify the preferred Fixture Vendor', FCT_FIXTURE_VENDORS)

def _render_system_assessment_section(info):
    with st.container(border=True):
        subtitle_h3("FCT System Assessment")
        info["studies_necessaries"] = st.multiselect(label=r"*Select the studies necessaries (MSA, GRR...)", options=FCT_STUDIES_OPTIONS, placeholder="You can select multiple")
        col1, col2 = st.columns(2)
        with col1:
            info["qty_microstrains"] = st.text_input("How many uS (microstrains)?", placeholder="600")
            info["hardware_option"] = st.selectbox("Preferent Hardware", FCT_HARDWARE_OPTIONS)
            info["system_type"] = st.selectbox(r"*System Type", FCT_SYSTEM_TYPES)
            info["station_type"] = st.selectbox(r"*Station Type", FCT_STATION_TYPES)
            info["process_type"] = st.selectbox(r"*Process Type:", FCT_PROCESS_TYPES)
            info["scanner_brand"] = st.selectbox("Scanner:", ["Keyence", "Cognex", "Microscan", "Other"])
        with col2:
            info["rosettes"] = st.text_input("How many Rosettes?", placeholder="8")
            info["fixture_needs"] = st.text_area("Describe the needs of the Fixture:", placeholder="Kit ingun\nMass interconnect\nPneumatic fixture, etc.")
            info["dm_position"] = st.text_area("Specified DM or barcode position and scanner model:", height=150)
            info['modifications_customer'] = st.radio('Does the customer want to make modifications to the system or test procedure by himself??', YES_NO, index=1, horizontal=True)
            info["test_sequencer"] = st.selectbox(r"*Test Sequencer", ["Select Option", "LabView", "TestStand", "CVI", "TestExec", "Other"])

def _render_system_specifications_section(info):
    with st.container(border=True):
        subtitle_h3("Testing System Specifications")
        col1, col2 = st.columns(2)
        with col1:
            info["dimensions"] = st.radio(r"*Expected dimensions for the testing system (limited space, height)?", YES_NO, horizontal=True, index=1)
            info["test_execution_conditions"] = st.radio(r"*Test Execution under specific conditions (High/Low Temperature, Humidity,control cabin or chamber, etc.)?", YES_NO, horizontal=True, index=1)
        with col2:
            info["dimensions_spec"] = st.text_input("Specify Dimensions", placeholder="Specify", key="dim_spec")
            info["test_execution_conditions_spec"] = st.text_input("Specify Conditions", placeholder="Specify", key="test_exec_cond")

def _render_product_requirements_section(info):
    with st.container(border=True):
        subtitle_h3("Product and Testing System Requirements")
        col1, col2 = st.columns(2)
        with col1:
            info["single_product"] = st.radio(r"*The System will only be used for a single product or different products?", YES_NO, horizontal=True, index=1)
            info["self_test_required"] = st.radio(r"*Self-Test required for product and testing system?", YES_NO, horizontal=True, index=1)
            info["certification_required"] = st.radio(r"*Certifications Required?", YES_NO, horizontal=True, index=1)
        with col2:
            info["single_product_info"] = st.text_input("Specify Products", placeholder="Specify", key="single_product_info")
            info["self_test_required_info"] = st.text_input("Specify Self-Test", placeholder="Specify", key="self_test_required_info")
            info["certification_required_info"] = st.text_input("Specify Certifications", placeholder="Specify", key="certification_info")
            info["certifications_option"] = st.selectbox("Other Certifications:", ["Other", "CE", "EMV", "VDE", "Calibration", "UL"])

def _render_additional_info_section(info):
    with st.container(border=True):
        subtitle_h3("Additional Information")
        info["travel"] = st.text_input(r"*Where do you want us to deliver?", placeholder="Company name, State, Country")
        info["entity_po"] = st.text_input(r"*The entity that the PO will come from.", placeholder="Company name, State, Country")
        info["additional_comments"] = st.text_area(label="Additional Comments", placeholder='Write your comments here...')

def create_fct_specific_sections(info):
    """
    Create FCT-specific form sections by calling modular rendering functions.
    
    Args:
        info (dict): Dictionary to store form data.
    """
    _render_milestones_section(info)
    _render_system_assessment_section(info)
    _render_system_specifications_section(info)
    _render_product_requirements_section(info)
    _render_additional_info_section(info)

@require_authentication
def main():
    """Main function to run the FCT assessment."""
    # Create FCT assessment instance
    fct_assessment = BaseAssessment(
        assessment_type="FCT",
        title="Functional Test Assessment",
        projects_folder="2_Functional Test (FCT)"
    )
    
    # Render the form with FCT-specific sections
    fct_assessment.render_form(
        file_types=FCT_FILE_TYPES,
        html_converter=json_to_html,
        additional_sections=create_fct_specific_sections
    )

if __name__ == "__main__":
    main() 