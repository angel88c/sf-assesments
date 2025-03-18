import json
import os
import shutil
from pages.lib.fct_create_html import *
from pages.lib.constants import *
from pages.lib.salesforce_access import *
from pages.lib.dates_info import *

import streamlit as st
from decouple import config
from datetime import datetime

st.set_page_config(initial_sidebar_state="collapsed")


FCT_TEMPLATE_FOLDER = "2_Functional Test (FCT)"

# Store a variable in session_state
if "salesforce" not in st.session_state:
    st.session_state.salesforce = connect_to_salesforce()
    
def validate_fields(fields):
    required_fields = ["project_name",
                       "contact_name",
                       "date",
                       "contact_email"]

    error_strings = []
    for required_field in required_fields:
        if required_field in fields:
            if fields[required_field] == "":
                error_strings.append(
                    f"El campo {required_field} es obligatorio.")

    if error_strings:
        return error_strings

    return []

# Título de la aplicación
st.title("Functional Test Assesment")

info = dict()
YEAR = str(datetime.today().year)

# Crear un formulario
with st.form(key='fct_assesment'):
    # Sección 1: Información Personal
    # st.header("Contact Information")

    col1, col2 = st.columns(2)
    with col1:
        info["project_name"] = st.text_input(
            'Name or Project Reference', placeholder="Enter the name of the project", )
        info["contact_name"] = st.text_input(
            'Contact', placeholder="Enter your name")
        info["contact_email"] = st.text_input('Email')
        info['country'] = st.selectbox('Country', options=COUNTRIES_DICT.keys())
        
        info["is_duplicated"] = st.radio(
            'Duplicated Project?', YES_NO, index=1, horizontal=True)

    with col2:
        info["date"] = st.date_input('Date').strftime("%Y-%m-%d")
        info["project_start_date"] = st.date_input(
            'Project Start Date').strftime("%Y-%m-%d")
        info["customer_name"] = st.text_input(
            'Customer Name or Plant', placeholder="Enter the name of the customer or Plant", )

        info["contact_phone"] = st.text_input(
            'Phone Number', placeholder="Enter your phone number")

    st.header('Upload Files')
    uploaded_files = st.file_uploader(
        "Upload your files to share with us.", accept_multiple_files=True)

    # Sección 2: Preferencias|
    # st.header("Required Internal Departments")

    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     info['activation_type'] = st.radio(
    #         'Activation Type', ACTIVATION_TYPES, help="")
    # with col2:
    #     info['well_type'] = st.radio('Well Type', WELL_TYPES)
    # with col3:
    #     info['size_type'] = st.radio('Size Type', SIZE_TYPES)

    st.divider()

    col1, col2 = st.columns([1, 1.5])
    with col1:
        info['cad_files'] = st.radio('CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)', horizontal=True, options=YES_NO)
        info['gerber_files'] = st.radio('Gerber Files', horizontal=True, options=YES_NO)
        info['schematics'] = st.radio('schematics', horizontal=True, options=YES_NO)
        info['boms'] = st.radio('BOMs of each version', horizontal=True, options=YES_NO)
        info['traceability_system'] = st.radio( 'Trazability System', horizontal=True, options=YES_NO)
        info['sow'] = st.radio('SOW', horizontal=True, options=YES_NO)
        info["product_finish"] = st.selectbox("Specify how the product will be test", FCT_PRODUCT_FINISH)
        info["test_strategy"] = st.selectbox("Test strategy", FCT_TEST_STRATEGIES)
        info["connection_interface"] = st.selectbox("Connection Interface", FCT_CONNECTION_INTERFACES)
    with col2:
        info['drawings'] = st.radio('Drawings (2D, 3D)', horizontal=True, options=YES_NO)
        info['test_spec'] = st.radio('Test Spec', horizontal=True, options=YES_NO)
        info['parallel_testing'] = st.radio('Parallel Testing?', horizontal=True, options=YES_NO)
        info['security_specification'] = st.radio('Security Specification', horizontal=True, options=YES_NO)

        info["traceability_system_name"] = st.text_input(
            label=".", label_visibility="hidden", placeholder='Traceability system')
        info["ergonomy_specifications"] = st.text_input(
            label=".", label_visibility="hidden", placeholder='Ergonomy Specifications')

        info['osp_finish'] = st.radio(
            'In the case of PCB, Does the product have OSP finish on TPs?', horizontal=True, index=1, options=YES_NO)

        info['quantity_uut'] = st.number_input("How many units under test?", min_value=0, value=0)
        info["fixture_vendor"] = st.selectbox("Fixture Vendor required (if apply):", FCT_FIXTURE_VENDORS)

    st.divider()
    st.markdown("<h4>FCT System Assesment</h4>", unsafe_allow_html=True)


    info["studies_necessaries"] = st.multiselect(
        label="Select the studies necessaries (MSA, GRR...)", options=FCT_STUDIES_OPTIONS)

    col1, col2 = st.columns(2)
    with col1:
        info["qty_microstrains"] = st.text_input("How many uS (microstrains)?")

    with col2:
        info["rosettes"] = st.text_input("How mmany Rosettes?")

    info["fixture_needs"] = st.text_area("Describe the needs of the Fixture:")

    st.divider()

    col1, col2 = st.columns(2)

    cols = st.columns(2)
    with cols[0]:
        pass

    with col1:
        info["hardware_option"] = st.selectbox("Preferent Hardware", FCT_HARDWARE_OPTIONS)
        info["system_type"] = st.selectbox("System Type", FCT_SYSTEM_TYPES)
        info["station_type"] = st.selectbox("Station Type", FCT_STATION_TYPES)
        info["process_type"] = st.selectbox("Process Type:", FCT_PROCESS_TYPES)

    with col2:
        info["dm_position"] = st.text_area(
            "Specified DM or barcode position and scanner model:", height=300)

    col1, col2 = st.columns(2)
    with col1:
        info["scanner_brand"] = st.selectbox(
            "Scanner:", ["Keyence", "Cognex", "Microscan", "Other"])
        info['modifications_customer'] = st.radio(
            'Does the customer want to make modifications to the system or test procedure by himself??', YES_NO, index=1, horizontal=True)

    with col2:
        info["test_sequencer"] = st.selectbox("Test Sequencer", [
                                              "Select Option", "LabView", "TestStand", "CVI", "TestExec", "Other"])

    st.divider()
    st.markdown("<h4>Testing System Specifications</h4>",
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        info["dimensions"] = st.radio("Expected dimensions for the testing system (limited space, height)?", YES_NO, horizontal=True, index=1)
        info["test_execution_conditions"] = st.radio("Test Execution under specific conditions (High/Low Temperature, Humidity,control cabin or chamber, etc.)?", YES_NO, horizontal=True, index=1)

    with col2:
        info["dimensions_spec"] = st.text_input(label=".", placeholder="Specify", key="dim_spec")
        info["test_execution_conditions_spec"] = st.text_input(label=".", placeholder="Specify", key="test_exec_cond")

    st.divider()
    st.markdown("<h4>Product and Testing System Requirements</h4>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        info["single_product"] = st.radio(
            "The System will only be used for a single product or different products?", YES_NO, horizontal=True, index=1)
        info["self_test_required"] = st.radio(
            "Self-Test required for product and testing system?", YES_NO, horizontal=True, index=1)
        info["certification_required"] = st.radio(
            "Certifications Required?", YES_NO, horizontal=True, index=1)

    with col2:
        info["single_product_info"] = st.text_input(
            label=".", placeholder="Specify", key="single_product_info")
        info["self_test_required_info"] = st.text_input(
            # , key="test_exec_cond")
            label=".", placeholder="Specify", key="self_test_required_info")
        info["certification_required_info"] = st.text_input(
            # , key="test_exec_cond")
            label=".", placeholder="Specify", key="certification_info")
        info["certifications_option"] = st.selectbox(
            "Other Certifications:", ["Other", "CE", "EMV", "VDE", "Calibration", "UL"])

        # Sección 3: Comentarios Adicionales
    st.markdown("<h4>Additional Comments</h4>", unsafe_allow_html=True)
    info["additional_comments"] = st.text_area(label="Additional Comments")

    # Botón de envío
    enviar = st.form_submit_button(
        'Enviar', help='Enviar el formulario', type='primary')

    # Acciones al enviar el formulario
    if enviar:

        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        errors_validation = validate_fields(info)
        if errors_validation:
            for error in errors_validation:
                st.error(error)
        else:
            #
            try:
                country = info.get("country", "Mexico")
                UPLOAD_FILES_FOLDER = os.path.join(PATH_FILE, COUNTRIES_DICT[country], f"{info['project_name']}")
                
                if os.path.exists(UPLOAD_FILES_FOLDER):
                    st.error(f"Oppotunity with name {info['project_name']} already created, please contact Sales Manager to update your requirement.")
                    st.stop()
                    
                os.makedirs(UPLOAD_FILES_FOLDER, exist_ok=True)
                shutil.copytree(TEMPLATE_FCT, UPLOAD_FILES_FOLDER, dirs_exist_ok=True)
                
                # PATH = f"C:/Users/c_ang/Innovative Board Test SAPI de CV/admin - iBtest Assesment/ict_assesment_{current_datetime}.json"
                # PATH =  f"{PATH_FILE}/ict_assesment_{current_datetime}.json"
                ALL_INFO_SHARED_PATH = os.path.join(UPLOAD_FILES_FOLDER, "1_Customer_Info", "3_ALL_Info_Shared")
                PATH = os.path.join(UPLOAD_FILES_FOLDER, "FCT_Assesment.json")
                with open(PATH, 'w') as file:
                    json.dump(info, file, indent=4)

                html_data = json_to_html(info)
                if html_data:
                    PATH_HTML = os.path.join(UPLOAD_FILES_FOLDER, "FCT_Assesment.html")
                    with open(PATH_HTML, 'w') as file:
                        file.write(html_data)

                opportunity_name = info["project_name"]
                stage_name = "New Request"
                
                new_opp = {
                    "Name": opportunity_name,
                    "StageName": stage_name,
                    "CloseDate": get_last_weekday_of_next_month().strftime("%Y-%m-%d"),
                    "Assessment_Date__c": datetime.now().strftime("%Y-%m-%d"),
                    "Path__c": config("PATH_TO_SHAREPOINT")
                }

                if uploaded_files:
                    for file in uploaded_files:
                        save_path = os.path.join(ALL_INFO_SHARED_PATH, file.name)
                        with open(save_path, "wb") as f:
                            f.write(file.getbuffer())
                
                #raise ValueError("Not sending to salesforce at moment")

                st.write(new_opp)
                result = st.session_state.salesforce.__getattr__('Opportunity').create(new_opp)
                # result["success"] = True

                if result['success']:
                    st.success("Opportunity created successfully!")
                else:
                    st.error("Error creating Opportunity")
                    st.error("\n".join(result['errors']))

            except Exception as e:
                st.error(f'¡Error al enviar el formulario! {e}')
                st.error('Por favor, intenta de nuevo.')
                st.error('Si el problema persiste, contacta al administrador.')

    # Footer personalizado
    # footer = """
    # <style>
    # .footer {
    #     position: fixed;
    #     left: 0;
    #     bottom: 0;
    #     width: 100%;

    #     text-align: center;
    #     padding: 10px;
    #     font-size: 14px;
    # }
    # </style>
    # <div class="footer">
    #     <p>© 2025 iBtest. All rights reserved.</p>
    #     <p>Contact: sales@ibtest.com | Phone: +123 456 789</p>
    # </div>
    # """

    # st.markdown(footer, unsafe_allow_html=True)
