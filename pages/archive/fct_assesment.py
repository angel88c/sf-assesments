import json
import os
import shutil
from pages.utils.fct_create_html import *
from pages.utils.constants import *
from pages.utils.salesforce_access import *
from pages.utils.test_account_names import *
from pages.utils.dates_info import *
from pages.utils.global_styles import *
from pages.utils.validations import *

import streamlit as st
from decouple import config
from datetime import datetime

st.set_page_config(initial_sidebar_state="collapsed")
set_global_styles()

# Store a variable in session_state
if "salesforce" not in st.session_state:
    st.session_state.salesforce = connect_to_salesforce()
    
    
def upload_files():
    #upload files
    st.header('Are you sharing files?')
    uploaded_files = st.file_uploader(".", label_visibility="hidden", accept_multiple_files=True)
    
    st.markdown('<p style="margin-bottom: 1px;">*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Gerber files</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Schematics (pdf)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Test Spec (pdf, doc)"</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">BOMS</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">SOW</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Drawings (2d, 3d)</p>', unsafe_allow_html=True)

    return uploaded_files

# Título de la aplicación
load_ibtest_logo()
st.title("Functional Test Assesment")

info = dict()
YEAR = str(datetime.today().year)
BU = "FCT"
PROJECTS_FOLDER = "2_Functional Test (FCT)"

# Crear un formulario
with st.form(key='fct_assesment'):
    
    all_accounts = get_unique_account_dict()
    
    st.write("(*) Mandatory Fields")
    col1, col2 = st.columns(2)
    with col1:
        info["project_name"] = st.text_input(r"*Name or Project Reference", placeholder="Enter the name of the project", )
        info["contact_name"] = st.text_input(r"*Contact Name", placeholder="Enter your name")
        accounts_by_name = {name: id for id, name in all_accounts.items()}
        info["customer_name"] = st.selectbox(r"*Company name", options=list(accounts_by_name.keys()), index=None, placeholder="Select from list")
        info['country']      = st.selectbox(r"*Country", options=COUNTRIES_DICT.keys())
       
    with col2:
        info["date"] = datetime.today().strftime("%Y-%m-%d")
        info["quotation_required_date"] = st.date_input('When do you need the quote? Select an ideal date', ).strftime("%Y-%m-%d")
        info["contact_email"] = st.text_input(r'*Email', placeholder="Enter your email")
        info["customer_name2"] = st.text_input("Company not listed? Write it here.", placeholder="Enter the customer name")
        info["contact_phone"] = st.text_input('Phone Number', placeholder="Enter your phone number")
        
    info["is_duplicated"] = st.radio(r'*Duplicated Project?', YES_NO, index=1, horizontal=True)
    
    uploaded_files = upload_files()

    st.divider()

    col1, col2 = st.columns([1, 1.5])
    with col1:
        info['cad_files'] = st.radio(r'*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)', horizontal=True, options=YES_NO)
        info['gerber_files'] = st.radio(r'*Gerber Files', horizontal=True, options=YES_NO)
        info['schematics'] = st.radio(r'*Schematics', horizontal=True, options=YES_NO)
        info['boms'] = st.radio(r'*BOMs of each version', horizontal=True, options=YES_NO)
        info['traceability_system'] = st.radio( r'*Traceability System', horizontal=True, options=YES_NO)
        info['sow'] = st.radio(r'*SOW', horizontal=True, options=YES_NO)
        info["product_finish"] = st.selectbox(r"*Specify how the product will be test", FCT_PRODUCT_FINISH)
        info["test_strategy"] = st.selectbox(r"*Test strategy", FCT_TEST_STRATEGIES)
        info["connection_interface"] = st.selectbox(r"*Connection Interface", FCT_CONNECTION_INTERFACES)
    with col2:
        info['drawings'] = st.radio('Drawings (2D, 3D)', horizontal=True, options=YES_NO)
        info['test_spec'] = st.radio('Test Spec', horizontal=True, options=YES_NO)
        info['parallel_testing'] = st.radio('Parallel Testing?', horizontal=True, options=YES_NO)
        info['security_specification'] = st.radio('Security Specification', horizontal=True, options=YES_NO)
        info["traceability_system_name"] = st.text_input(label=".", label_visibility="hidden", placeholder="ITAC, MES, etc.")
        info["ergonomy_specifications"] = st.text_input(label=".", label_visibility="hidden", placeholder='Ergonomy Specifications')
        info['osp_finish'] = st.radio('In the case of PCB, Does the product have OSP finish on TPs?', horizontal=True, index=1, options=YES_NO)
        info['quantity_uut'] = st.number_input(r"*How many units under test?", min_value=1)
        info["fixture_vendor"] = st.selectbox("Fixture Vendor required (if apply):", FCT_FIXTURE_VENDORS)

    st.divider()
    
    subtitle_h3("FCT System Assesment")
    info["studies_necessaries"] = st.multiselect(
        label=r"*Select the studies necessaries (MSA, GRR...)", options=FCT_STUDIES_OPTIONS, placeholder="You can select multiple")

    col1, col2 = st.columns(2)
    with col1:
        info["qty_microstrains"] = st.text_input("How many uS (microstrains)?" ,placeholder="600")

    with col2:
        info["rosettes"] = st.text_input("How many Rosettes?", placeholder="8")

    info["fixture_needs"] = st.text_area("Describe the needs of the Fixture:", placeholder="Kit ingun\nMass interconnect\nPneumatic fixture, etc.")

    st.divider()

    col1, col2 = st.columns(2)

    cols = st.columns(2)
    with cols[0]:
        pass

    with col1:
        info["hardware_option"] = st.selectbox("Preferent Hardware", FCT_HARDWARE_OPTIONS)
        info["system_type"] = st.selectbox(r"*System Type", FCT_SYSTEM_TYPES)
        info["station_type"] = st.selectbox(r"*Station Type", FCT_STATION_TYPES)
        info["process_type"] = st.selectbox(r"*Process Type:", FCT_PROCESS_TYPES)

    with col2:
        info["dm_position"] = st.text_area(
            "Specified DM or barcode position and scanner model:", height=300)

    col1, col2 = st.columns(2)
    with col1:
        info["scanner_brand"] = st.text_input("Preferred Scanner Brand", placeholder="Keyence, Cognex, Microscan, Steren, etc.")
        info['modifications_customer'] = st.radio(
            'Does the customer want to make modifications to the system or test procedure by himself??', YES_NO, index=1, horizontal=True)

    with col2:
        info["test_sequencer"] = st.selectbox(r"*Test Sequencer", [
                                              "Select Option", "LabView", "TestStand", "CVI", "TestExec", "Other"])

    st.divider()
    st.markdown("<h4>Testing System Specifications</h4>",
                unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        info["dimensions"] = st.radio(r"*Expected dimensions for the testing system (limited space, height)?", YES_NO, horizontal=True, index=1)
        info["test_execution_conditions"] = st.radio(r"*Test Execution under specific conditions (High/Low Temperature, Humidity,control cabin or chamber, etc.)?", YES_NO, horizontal=True, index=1)

    with col2:
        info["dimensions_spec"] = st.text_input(label=".", placeholder="Specify", key="dim_spec")
        info["test_execution_conditions_spec"] = st.text_input(label=".", placeholder="Specify", key="test_exec_cond")

    st.divider()
    st.markdown("<h4>Product and Testing System Requirements</h4>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        info["single_product"] = st.radio(
            r"*The System will only be used for a single product or different products?", YES_NO, horizontal=True, index=1)
        info["self_test_required"] = st.radio(
            r"*Self-Test required for product and testing system?", YES_NO, horizontal=True, index=1)
        info["certification_required"] = st.radio(
            r"*Certifications Required?", YES_NO, horizontal=True, index=1)

    with col2:
        info["single_product_info"] = st.text_input(label=".", placeholder="Specify", key="single_product_info")
        info["self_test_required_info"] = st.text_input(label=".", placeholder="Specify", key="self_test_required_info")
        info["certification_required_info"] = st.text_input(label=".", placeholder="Specify", key="certification_info")
        info["certifications_option"] = st.selectbox("Other Certifications:", ["Other", "CE", "EMV", "VDE", "Calibration", "UL"])

        # Sección 3: Comentarios Adicionales
    st.markdown("<h4>Additional Information</h4>", unsafe_allow_html=True)
    info["travel"] = st.text_input(r"*Travel (Indicate the place of Delivery).", placeholder="San Juan del Río")
    info["entity_po"] = st.text_input(r"*The entity that the PO will come from.", placeholder="Queretaro")
    info["additional_comments"] = st.text_area(label="Additional Comments", placeholder='Write your comments here...')
    
    # Botón de envío
    enviar = st.form_submit_button(
        'Submit', help='Submit form', type='primary')

    # Acciones al enviar el formulario
    if enviar:
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        valid_email = validate_email(info['contact_email'])
        if not valid_email:
            st.error("Error!! Only Corporate emails are valid")
            st.stop()
            
        errors_validation = validate_fields(info)
        if errors_validation:
            for error in errors_validation:
                st.error(error)
        else:
            #
            try:
                country = info.get("country", "Mexico")
                customer_in_list = True
                if info["customer_name"] is None or info["customer_name"] == "Other":
                    info["customer_name"] = info["customer_name2"]
                    customer_in_list = False

                #UPLOAD_FILES_FOLDER = os.path.join(config("PATH_FILE"), COUNTRIES_DICT[country], f"{info['customer_name']}", f"{info['project_name']}")
                UPLOAD_FILES_FOLDER = os.path.join(config("PATH_FILE"),
                                                   PROJECTS_FOLDER, 
                                                   COUNTRIES_DICT[country], 
                                                   f"{info['customer_name']}",
                                                   f"{info['project_name']}")
                
                if os.path.exists(UPLOAD_FILES_FOLDER):
                    st.error(f"Oppotunity with name {info['project_name']} already created, please contact Sales Manager to update your requirement.")
                    st.stop()
                    
                os.makedirs(UPLOAD_FILES_FOLDER, exist_ok=True)
                shutil.copytree(config("TEMPLATE_FCT"), UPLOAD_FILES_FOLDER, dirs_exist_ok=True)
                
                # PATH = f"C:/Users/c_ang/Innovative Board Test SAPI de CV/admin - iBtest Assesment/ict_assesment_{current_datetime}.json"
                # PATH =  f"{PATH_FILE}/ict_assesment_{current_datetime}.json"
                ALL_INFO_SHARED_PATH = os.path.join(UPLOAD_FILES_FOLDER, "1_Customer_Info", "3_ALL_Info_Shared")
                #PATH = os.path.join(UPLOAD_FILES_FOLDER, "FCT_Assesment.json")
                #with open(PATH, 'w') as file:
                #    json.dump(info, file, indent=4)

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
                    "Path__c": config("PATH_TO_SHAREPOINT"),                        
                    "BU__c": BU
                }
                
                if customer_in_list:
                    new_opp["AccountId"] = accounts_by_name.get(info["customer_name"], "")
                    
                if uploaded_files:
                    for file in uploaded_files:
                        save_path = os.path.join(ALL_INFO_SHARED_PATH, file.name)
                        with open(save_path, "wb") as f:
                            f.write(file.getbuffer())
                
                
                #st.write(new_opp)
                #raise ValueError("Not sending to salesforce at moment")

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
