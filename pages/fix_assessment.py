"""
ICT Assessment Module

This module provides the In Circuit Test assessment functionality.
It extends the base assessment class with ICT-specific form fields and processing.
"""

import streamlit as st

# Set page configuration - must be the first Streamlit command
st.set_page_config(initial_sidebar_state="collapsed")

from pages.utils.base_assessment import BaseAssessment
from pages.utils.fix_create_html import json_to_html
from pages.utils.constants import (
    YES_NO, REQ_OPTIONS, ACTIVATION_TYPES, 
    WELL_TYPES, SIZE_TYPES, OPTIONS
)
from pages.utils.global_styles import subtitle_h2, subtitle_h3, subtitle_h4
from main import hash_password

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to access this page")
    st.switch_page("main.py")
    #st.stop()  # This stops execution if not authenticated
    
    

# Define ICT-specific file types
# ICT_FILE_TYPES = [
#     '*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)',
#     '*BOM',
#     'Gerber files',
#     'Schematics (pdf)',
#     'Test Spec (pdf, doc)',
#     'Fixture SOW',
#     'Board directory (.tar.gz, .tar)'
# ]
ICT_FILE_TYPES = {
    '*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)': False,
    'Gerber files': False,
    'Schematics (pdf)': False,
    'BOMs of each version': False,
    '2D Drawings (.dwg, .dxf, .pfd, .tif)': False,
    '3D Drawings (.step, .igs, .x_t)': False,
    'Test Spec (pdf, doc)': False,
    'Customer\'s SOW': False,
    'Physical Samples': False,
}

def generate_milestones(info, milestones):
    for item in milestones:
        st.markdown(f"**{item}**")
        col1, col2, col3= st.columns([1.5,1,3])
        with col1: 
            status = st.radio("Select", options=["Yes", "No"], key=f"{item}_status", horizontal=True)
        with col2:
            qty = st.number_input("Qty", key=f"{item}_qty", value=0)
        with col3:
            comments = st.text_input("Comments", key=f"{item}_comments")

        info[item] = {
            "Status": status,
            "Qty": qty,
            "Comments": comments
        }

def create_fix_specific_sections(info):
    """
    Create ICT-specific form sections.
    
    Args:
        info (dict): Dictionary to store form data
    """
    
    #col1, col2 = st.columns(2)
    #with col1:
    #    info["is_duplicated"] = st.radio(r'*Duplicated Fixture?', YES_NO, index=1, horizontal=True)
    #with col2:
    #    info["fixure_type2"] = st.radio(r'*Fixture Type', FIXTURE_TYPES, horizontal=True)
    
    # Sección 2: Preferencias|
    with st.container(border=True, ):
        subtitle_h3("General Product Information")
        col1, col2 = st.columns(2)
        with col1:
            info["product_use_type"] = st.radio("System will be used for", ["Single Product", "Multiple Products"], horizontal=True)
            info["test_type"] = st.selectbox("Test Type", 
                                     options=["ICT", "Flashing", 
                                              "Funtional Test", "LED Test", 
                                              "Hi-Pot", "RF Test"])
            info["dut_assembly_level"] = st.selectbox("Device Under Test (DUT) Assembly Level", 
                                     options=["Housing", "PCBA", 
                                              "Other"])

        with col2:
            info["product_use_type_comments"] = st.text_input("Comments", key="product_use_type_comments")
            info["test_type_comments"] = st.text_input("Comments", key=f"test_type_comments")
            info["dut_assembly_level_comments"] = st.text_input("Comments", key=f"dut_assembly_level_comments")

        milestones2 = [
            "Panel Test? (Qty boards on panel)",
            "Individual Test? (Nest Qty per well)",
            "Is the product NPI or design freeze?",
        ]
        generate_milestones(info, milestones2)

        col1, col2 = st.columns(2)
        with col1:
            info["purpose_fixture"] = st.selectbox("Purpose of the Fixture: Off-line or In-Line", 
                                     options=["Off-line", "In-Line", 
                                              "Conveyor Pallet"])

        with col2:
            info["purpose_fixture_comments"] = st.text_input("Comments", key="purpose_fixture_comments")

        info["pcb_side"] = st.text_input("For in-line system which side of the PCB is the bottom?")
        info["products_manufacture"] = st.text_input("How many products manufacture per year or per month?")


        col1, col2, col3 = st.columns(3)
        with col1:
            info['activation_type'] = st.radio(r'*Activation Type', options=ACTIVATION_TYPES.keys())
            info["fixure_type"] = ACTIVATION_TYPES[info["activation_type"]]
        with col2:
            info['well_type'] = st.radio(r'*Well Type', WELL_TYPES)
        with col3:
            info['size_type'] = st.radio(r'*Size Type', SIZE_TYPES)

        col1, col2 = st.columns(2)
        with col2:
            info['fixture_vendor'] = st.text_input('Specify the preferred Fixture Vendor', 
                                                     placeholder='Circuit Check, Rematek, Arcadia, Juarez Technology, QxQ, etc.')
        with col1:
            info['versions'] = st.number_input("How many versions?", 
                                               placeholder="Enter the number of versions to consider", min_value=1)
            
    with st.container(border=True):
        subtitle_h3("Fixture Configuration")
        st.markdown("**Connectivity to the DUT**")
        labels = ["Test Points", "Connectors", "Through hole", "Wire Harness", "RF Coaxial", "Other"]
        for i, label in enumerate(labels):
            col1, col2 = st.columns(2)
            with col1: 
                info[f"dut_{label.lower().replace(' ', '_')}"] = st.checkbox(label)
            with col2: 
                info[f"dut_{label.lower().replace(' ', '_')}_comments"] = st.text_input("Comments", key=f"dut_{label.lower().replace(' ', '_')}_comments")
            st.divider()

        milestones_3 = [
            "Mass Interconnect System",
            "Harness connectors",
            "Special connectors on fixture's back",
            "Bottom nodes to access (TPs or connectors)",
            "Top nodes to access (TPs or pin connectos)",
            "Side access connections",
            "Specify the type of socket's tail (wiring method)",
            "Door closed lock",
            "Automatic Opening",
            "Counter",
            "Product precense sensor",
            "BoardMarkes",
            "Scanner (Please specify type: DM, QR, Barcode. And specify brand preference)",
            "LED Test (Please specify brand preferrence, type of test Color/Intensity)",
            "Instalation of special hardware on the fixture is needed (If it does please specify)",
            "Does the fixture need internal wiring labor?",
            "FEA Study?",
            "Strain gage study? (Please specify qty. of rossetes)"
        ]

        generate_milestones(info, milestones_3)
       
    # Sección 3: Comentarios Adicionales
    with st.container(border=True):
        subtitle_h4("Additional Information")
        info["travel"] = st.text_input(r"*Where do you want us to deliver?", placeholder="Company name, State, Country")
        info["entity_po"] = st.text_input(r"*The entity that the PO will come from.", placeholder="Company name, State, Country")
        info["additional_comments"] = st.text_area(label="Additional Comments", placeholder='Write your comments here...')


def main():
    """Main function to run the ICT assessment."""
    # Create ICT assessment instance
    ict_assessment = BaseAssessment(
        assessment_type="IAT",
        title="Fix Test Assessment",
        projects_folder="1_FIX Test (FIX)"
    )
    
    # Render the form with ICT-specific sections
    ict_assessment.render_form(
        file_types=ICT_FILE_TYPES,
        html_converter=json_to_html,
        additional_sections=create_fix_specific_sections
    )

if __name__ == "__main__":
    main()
