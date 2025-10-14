"""
IAT Assessment Module

This module provides the Industrial Automation Test assessment functionality.
It extends the base assessment class with IAT-specific form fields and processing.
"""

import streamlit as st

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to access this page")
    st.switch_page("main.py")
    #st.stop()  # This stops execution if not authenticated

st.set_page_config(initial_sidebar_state="collapsed")

from pages.utils.global_styles import subtitle_h3
from pages.utils.base_assessment_refactored import BaseAssessment
from pages.utils.iat_create_html import json_to_html
from pages.utils.constants import (
    YES_NO, IAT_MILESTONES, IAT_STATION_TYPES, IAT_PROCESS_TYPES,
    IAT_UNIT_HANDLE_MODES, IAT_DEVICES_UNDER_PROCESS
)

# Define IAT-specific file types
# IAT_FILE_TYPES = [
#     '*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)',
#     'Drawings (2d, 3d)',
#     'Gerber files',
#     'PLC, HMI, Robot programming standards (Templates)',
#     'Test Spec (pdf, doc)',
#     'Product Spec.',
#     'Product manufacturing sheet.'
#]
IAT_FILE_TYPES = {
    '*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)': False,
    'Drawings (2d, 3d)': False,
    'Gerber files': False,
    'PLC, HMI, Robot programming standards (Templates)': False,
    'Test Spec (pdf, doc)': False,
    'Product Spec.': False,
    'Product manufacturing sheet.': False,
}

def create_iat_specific_sections(info):
    """
    Create IAT-specific form sections.
    
    Args:
        info (dict): Dictionary to store form data
    """
    st.divider()
    
    # IAT-specific form fields
    # Milestone
    with st.container(border=True):
        #st.markdown('<h2>Milestones</h2>', unsafe_allow_html=True)
        subtitle_h3("Milestones")
        cols = st.columns(2)
        with cols[0]:
            info['cad_files'] = st.radio(
                IAT_MILESTONES[0], YES_NO, index=1, horizontal=True)
            info['process_spec'] = st.radio(
                IAT_MILESTONES[1], YES_NO, index=1, horizontal=True)
            ncols = st.columns(2)
            with ncols[0]:
                info['nests'] = st.radio(
                    IAT_MILESTONES[2], YES_NO, index=1, horizontal=True)
            with ncols[1]:
                info["qty_nests"] = st.text_input("How Many Nests?", placeholder="4")

            info['plc_programming_standard'] = st.radio(
                IAT_MILESTONES[3], YES_NO, index=1, horizontal=True)
            info["sow_ergonomic_spec"] = st.radio(
                IAT_MILESTONES[4], YES_NO, index=1, horizontal=True)
            ncols = st.columns(2)
            with ncols[0]:
                info["layout"] = st.radio(
                    IAT_MILESTONES[5], YES_NO, index=1, horizontal=True)
            with ncols[1]:
                info["dimensions"] = st.text_input("Dimensions", placeholder="4cm x 2.5cm")

        with cols[1]:
            info["product_manufacturing_sheet"] = st.radio(
                IAT_MILESTONES[6], YES_NO, index=1, horizontal=True)

            ncols = st.columns(2)
            with ncols[0]:
                info["traceability"] = st.radio(IAT_MILESTONES[7], YES_NO, index=1, horizontal=True)
            with ncols[1]:
                info["traceability_name"] = st.text_input("Traceability System Name", placeholder="ITAC, MES, etc.")

            with ncols[0]:
                info["estimated_cycle_time"] = st.radio(
                    IAT_MILESTONES[8], YES_NO, index=1, horizontal=True)
            with ncols[1]:
                info["cycle_time"] = st.text_input("Estimated Cycle Time", placeholder="7.5 sec")

            with ncols[0]:
                info["special_handling"] = st.radio(
                    IAT_MILESTONES[9], YES_NO, index=1, horizontal=True)
            with ncols[1]:
                info["special_handling_info"] = st.text_input(
                    "Special Handling Info")

            info["customer_has_samples"] = st.radio(
                IAT_MILESTONES[10], YES_NO, index=1, horizontal=True)

    with st.container(border=True):
        #st.markdown('<h2>Milestones</h2>', unsafe_allow_html=True)
        subtitle_h3("Station Features")
        cols = st.columns(2)
        with cols[0]:
            info["station_type"] = st.selectbox(
                r"*Type of Station or Service?", IAT_STATION_TYPES)
        with cols[1]:
            info["station_type_info"] = st.text_area(
                "Station or Service Type details")

        cols = st.columns(2)
        with cols[0]:
            info["process_type"] = st.selectbox(
                r"*Type of Process?", IAT_PROCESS_TYPES)
        with cols[1]:
            info["process_type_info"] = st.text_area(
                "Process Type information details")

        cols = st.columns(2)
        with cols[0]:
            info["uut_handle_mode"] = st.selectbox(
                r"*How will the Unit be Handled?", IAT_UNIT_HANDLE_MODES)
        with cols[1]:
            info["uut_handle_mode_info"] = st.text_area("More information")

        info["device_under_process"] = st.selectbox(
            "Device under process?", IAT_DEVICES_UNDER_PROCESS)

        cols = st.columns(2)
        with cols[0]:
            info["design_required"] = st.radio(
                "Design (Drawings) are required?", YES_NO, index=1, horizontal=True)
        with cols[1]:
            info["design_required_info"] = st.text_area(
                "Details for Required Design")

        cols = st.columns(2)
        with cols[0]:
            info["certifications_required"] = st.radio(
                "Certifications are required?", YES_NO, index=1, horizontal=True)
        with cols[1]:
            info["certifications_info"] = st.text_area(
                "Details for Required Certifications")

        # Sección 2: Preferencias|

        info["preferent_hardware"] = st.text_area("Preferent Hardware required? Describe the brands.")
        info["acceptance_criteria"] = st.text_area("Acceptance Criteria.")
        info["general_info_requirement"] = st.text_area("Briefly describe your need and what is the most important to you in the project:")
    
    with st.container(border=True):
        st.markdown("<h4>Additional Information</h4>", unsafe_allow_html=True)
        info["travel"] = st.text_input(r"*Where do you want us to deliver?", placeholder="Company name, State, Country")
        info["entity_po"] = st.text_input(r"*The entity that the PO will come from.", placeholder="Company name, State, Country")
        info["additional_comments"] = st.text_area(label="Additional Comments", placeholder='Write your comments here...')

def main():
    """Main function to run the IAT assessment."""
    # Create IAT assessment instance
    iat_assessment = BaseAssessment(
        assessment_type="IAT",
        title="Industrial Automation Test Assessment",
        projects_folder="4_Industrial Automation (IAT)"
    )
    
    # Render the form with IAT-specific sections
    iat_assessment.render_form(
        file_types=IAT_FILE_TYPES,
        html_converter=json_to_html,
        additional_sections=create_iat_specific_sections
    )

if __name__ == "__main__":
    main() 