"""
ICT Assessment Module

This module provides the In Circuit Test assessment functionality.
It extends the base assessment class with ICT-specific form fields and processing.
"""

import streamlit as st

# Set page configuration - must be the first Streamlit command
st.set_page_config(initial_sidebar_state="collapsed")

from pages.utils.base_assessment_refactored import BaseAssessment
from pages.utils.ict_create_html import json_to_html
from pages.utils.constants import (
    YES_NO, REQ_OPTIONS, ACTIVATION_TYPES, 
    WELL_TYPES, SIZE_TYPES, OPTIONS
)
from pages.utils.global_styles import subtitle_h2, subtitle_h3, subtitle_h4

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
    '*BOM': False,
    'Gerber files': False,
    'Schematics (pdf)': False,
    'Test Spec (pdf, doc)': False,
    'Fixture SOW': False,
    'Board directory (.tar.gz, .tar)': False,
}

def create_ict_specific_sections(info):
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
        subtitle_h3("Feature Fixture")
        info["inline_bottom_side"] = st.text_input(
            'For InLine systems, which is the bottom side?', placeholder="Bottom side of PCB for Test System, e. g. Conenctor Side, main uc side, Layer")

    
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
        

    with st.expander("Flash Programming", expanded=False):
        
        with st.container(border=True):
            info['flash_programming'] = st.radio(
                'Flash Programming?', REQ_OPTIONS,
                horizontal=True)
            
            col1, col2 = st.columns(2)
            with col1:
                info["programmer_brand"] = st.text_input(
                    'What Programmer (Brand) do you want us to use?', placeholder="FlashRunner 2.0, FRCube, Phyton, Algocraft, Segger, etc.")
            
                info['logistic_data'] = st.radio(
                    OPTIONS[0], YES_NO, index=1, horizontal=True)
            
            with col2:
                text_enter = st.text_input("Part Numbers of devices to program.", placeholder="TC387, PIC16F628, MC9S12EXBP")
                devices = text_enter.split(",")
                info["program_devices"] = devices
                info["quantity_devices"] = len(devices)
                info["program_devices"] = devices

                info["items_for_logistic_data"] = st.text_input(
                    OPTIONS[1], placeholder="Part Number, Serial Number, Security Key etc.")
    
    with st.container(border=True):
        subtitle_h3("Test Specifications")
        info['test_spec'] = st.radio(
            OPTIONS[3], YES_NO, index=1, horizontal=True)
        info['fixture_sow'] = st.radio(
            OPTIONS[4], YES_NO, index=1, horizontal=True)
        info['config_file'] = st.radio(
            OPTIONS[2], YES_NO, index=1, horizontal=True)
    
    with st.container(border=True):
        subtitle_h3("Panelized or depanelized?")
        col1, col2 = st.columns(2)
        with col1:
            info['panel_test'] = st.radio(OPTIONS[5], YES_NO, index=1, horizontal=True)
            info['individual_test'] = st.radio(OPTIONS[6], YES_NO, index=1, horizontal=True)
        
        with col2:
            info['quantity_panel'] = st.number_input('Quantity Boards on Panel?', min_value=1)
            info['quantity_nest'] = st.number_input('Specify Nest Qty?', min_value=1)

    
    with st.container(border=True):
        subtitle_h3("Additional Requirements")
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                info['automatic_scanner'] = st.radio('Automatic Scanner', REQ_OPTIONS, index=2, horizontal=True)                
                info["scanner_brand"] = st.text_input("Preferred Scanner Brand", placeholder="Keyence, Cognex, Microscan, Steren, etc.")
                info['board_presence'] = st.radio(r'*Board Presence', REQ_OPTIONS, horizontal=True)
                
            with col2:
                info['window_and_holder'] = st.radio('Window and Holder for Scanner?', YES_NO, index=1, horizontal=True)
                info['switch_probe_on_connector'] = st.radio(r'*Switch probe on connector required?', YES_NO, index=1, horizontal=True)
                 
                
            col1, col2 = st.columns(2)
            with col1:
                info['custom_tests'] = st.radio(r'* Apply Some custom tests?', YES_NO, index=1, horizontal=True)                
            with col2:
                info['custom_tests_info'] = st.text_input('Specify Custom Test', placeholder="CAN Communication, CyberSecurity, LIN, etc.")
            

            col1, col2 = st.columns(2)    
            with col1:  info['color_test'] = st.radio('Color/intensity LED test required and preferred sensor?', YES_NO, index=1, horizontal=True)
            with col2:  info['color_test_info'] = st.text_input('Specify Sensor', placeholder="Color Test, Feasa Led Analyzer/Optimistic.")

            info['clock_module'] = st.radio(r'*Clock Mode for Frequency measurement', REQ_OPTIONS, horizontal=True)
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                info['testjet'] = st.radio('Testjet/VTEP/NanoVTEP', REQ_OPTIONS, horizontal=True)
            with col2:
                info["ics_with_testjet"] = st.text_input("Which ICs are considered to have Testjet/VTEP/NanoVTEP?", placeholder="IC100, IC200")
            
        
        with st.expander("Boundary Scan and Silicon Nails", expanded=False):
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    info['boundary_scan'] = st.radio(r'*Boundary Scan Test?', REQ_OPTIONS, horizontal=True)
                    info['silicon_nails'] = st.radio(r'*Silicon nails and CET?', REQ_OPTIONS, horizontal=True)
                with col2:
                    info["required_ics"] = st.text_input("Which ICs are considered in the chain?", placeholder="MC9S12XEBP")
            
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
        assessment_type="ICT",
        title="In Circuit Test Assessment",
        projects_folder="1_In_Circuit Test (ICT)"
    )
    
    # Render the form with ICT-specific sections
    ict_assessment.render_form(
        file_types=ICT_FILE_TYPES,
        html_converter=json_to_html,
        additional_sections=create_ict_specific_sections
    )

if __name__ == "__main__":
    main()
