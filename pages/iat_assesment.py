import json
import os
import shutil
from pages.utils.iat_create_html import *
from pages.utils.constants import *
from pages.utils.salesforce_access import *
from pages.utils.test_account_names import *
from pages.utils.dates_info import *
from pages.utils.global_styles import *

import streamlit as st
from decouple import config
from datetime import datetime

st.set_page_config(initial_sidebar_state="collapsed")
set_global_styles()

IAT_TEMPLATE_FOLDER = "4_Industrial Automation (IAT)"

# Store a variable in session_state
if "salesforce" not in st.session_state:
    st.session_state.salesforce = connect_to_salesforce()

def validate_email(mail):
    
    invalid_email_found = False
    for email in INVALID_EMAILS:
        if email in mail:
            print("Correo Inválido")
            invalid_email_found = True
            return False
        
    if not invalid_email_found:
        print("Correo Válido")
        return True
    
def validate_fields(fields):
    required_fields = ["project_name",
                       "contact_name",
                       "contact_email",
                       "customer_name",
                       "date"]

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
load_ibtest_logo()
st.title(":mechanical_arm: Industrial Automation Test Assesment")

info = dict()
YEAR = str(datetime.today().year)

# Crear un formulario
with st.form(key='iat_assessment'):

    cols = st.columns([2, 1, 1])
    with cols[0]:
        info["project_name"] = st.text_input(
            'Name or Project Reference', placeholder="Enter the name of the project", )
    with cols[1]:
        info["date"] = st.date_input('Date').strftime("%Y-%m-%d")
    with cols[2]:
        info["project_start_date"] = st.date_input(
            'Project Start Date').strftime("%Y-%m-%d")

    col1, col2 = st.columns([1, 2])
    with col1:
        info["contact_name"] = st.text_input(
            'Contact Name', placeholder="Enter your name")
        info["customer_name"] = st.selectbox("Accounts", options=get_account_names_from_local_file(), index=None)
        info['country'] = st.selectbox('Country', options=COUNTRIES_DICT.keys())
        
        info["contact_phone"] = st.text_input(
            'Phone Number', placeholder="Enter your phone number")
        info["duplicated"] = st.radio(
            'Duplicated Project', YES_NO, index=1, horizontal=True)

    with col2:
        info["contact_email"] = st.text_input(
            'Email', placeholder='Enter your email address')
        #info["customer_name"] = st.text_input(
        #    'Customer Name or Plant', placeholder="Enter the name of the customer or Plant", )
        info["customer_name2"] = st.text_input('If Account does not exist, write here', placeholder="Enter Customer name")
        info["cad_files_and_program"] = st.radio(
            "If it's Duplicated, Do you have the CAD and PLC Program files?", YES_NO, index=1, horizontal=True)

    # Milestone
    st.markdown('<h2>Milestones</h2>', unsafe_allow_html=True)
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
            info["qty_nests"] = st.text_input("How Many Nests?")

        info['plc_programming_standard'] = st.radio(
            IAT_MILESTONES[3], YES_NO, index=1, horizontal=True)
        info["sow_ergonomic_spec"] = st.radio(
            IAT_MILESTONES[4], YES_NO, index=1, horizontal=True)
        ncols = st.columns(2)
        with ncols[0]:
            info["layout"] = st.radio(
                IAT_MILESTONES[5], YES_NO, index=1, horizontal=True)
        with ncols[1]:
            info["dimensions"] = st.text_input("Dimensions")

    with cols[1]:
        info["product_manufacturing_sheet"] = st.radio(
            IAT_MILESTONES[6], YES_NO, index=1, horizontal=True)

        ncols = st.columns(2)
        with ncols[0]:
            info["traceability"] = st.radio(
                IAT_MILESTONES[7], YES_NO, index=1, horizontal=True)
        with ncols[1]:
            info["traceability_name"] = st.text_input(
                "Traceability System Name")

        with ncols[0]:
            info["estimated_cycle_time"] = st.radio(
                IAT_MILESTONES[8], YES_NO, index=1, horizontal=True)
        with ncols[1]:
            info["cycle_time"] = st.text_input(
                "Estimated Cycle Time (Include Time units, min, sec, msec)")

        with ncols[0]:
            info["special_handling"] = st.radio(
                IAT_MILESTONES[9], YES_NO, index=1, horizontal=True)
        with ncols[1]:
            info["special_handling_info"] = st.text_input(
                "Special Handling Info")

        info["customer_has_samples"] = st.radio(
            IAT_MILESTONES[10], YES_NO, index=1, horizontal=True)

    cols = st.columns(2)
    with cols[0]:
        info["station_type"] = st.selectbox(
            "Type of Station or Service?", IAT_STATION_TYPES)
    with cols[1]:
        info["station_type_info"] = st.text_area(
            "Station or Service Type details")

    cols = st.columns(2)
    with cols[0]:
        info["process_type"] = st.selectbox(
            "Type of Process?", IAT_PROCESS_TYPES)
    with cols[1]:
        info["process_type_info"] = st.text_area(
            "Process Type information details")

    cols = st.columns(2)
    with cols[0]:
        info["uut_handle_mode"] = st.selectbox(
            "How will the Unit be Handled?", IAT_UNIT_HANDLE_MODES)
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

    # Upload Files
    st.header('Upload Files')
    uploaded_files = st.file_uploader(
        "Upload your files to share with us.", accept_multiple_files=True)
    
    st.markdown('<p style="margin-bottom: 2px;">CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Drawings (2d, 3d)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Gerber files</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">PLC, HMI, Robot programming standards (Templates)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Test Spec (pdf, doc)"</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Product Spec.</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Product manufacturing sheet.</p>', unsafe_allow_html=True)

    # Sección 2: Preferencias|
    st.markdown("<h4>Additional Comments</h4>", unsafe_allow_html=True)

    info["preferent_hardware"] = st.text_area("Preferent Hardware required? Describe the brands.")
    info["acceptance_criteria"] = st.text_area("Acceptance Criteria.")
    info["general_info_requirement"] = st.text_area("Briefly describe your need and what is the most important to you in the project:")
    info["travel"] = st.text_input("Travel (Indicate the place of Delivery).")
    info["entity_po"] = st.text_input("Entity from which PO will come:")

    comments = st.text_area(label="Additional Comments", placeholder='Write your comments here...')
    info["additional_comments"] = comments
    
    # Botón de envío
    enviar = st.form_submit_button('Submit', help='Submit form', type='primary')

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
            # Create the folder for the opportunity information
            # Only if all needed fields are filled
            try:
                
                country = info.get("country", "Mexico")
                if info["customer_name"] == "Other":
                    info["customer_name"] = info["customer_name2"]
                    
                UPLOAD_FILES_FOLDER = os.path.join(PATH_FILE, COUNTRIES_DICT[country], f"{info['customer_name']}", f"{info['project_name']}")
                if os.path.exists(UPLOAD_FILES_FOLDER):
                    st.error(f"Oppotunity with name {info['project_name']} already created, please contact Sales Manager to update your requirement.")
                    st.stop()
                    
                os.makedirs(UPLOAD_FILES_FOLDER, exist_ok=True)
                shutil.copytree(TEMPLATE_IAT, UPLOAD_FILES_FOLDER, dirs_exist_ok=True)
                
                # PATH = f"C:/Users/c_ang/Innovative Board Test SAPI de CV/admin - iBtest Assesment/ict_assesment_{current_datetime}.json"
                # PATH =  f"{PATH_FILE}/ict_assesment_{current_datetime}.json"
                ALL_INFO_SHARED_PATH = os.path.join(UPLOAD_FILES_FOLDER, "1_Customer_Info", "3_ALL_Info_Shared")
                PATH = os.path.join(UPLOAD_FILES_FOLDER, "IAT_Assesment.json")
                with open(PATH, 'w') as file:
                    json.dump(info, file, indent=4)

                html_data = json_to_html(info)
                if html_data:
                    PATH_HTML = os.path.join(UPLOAD_FILES_FOLDER, "IAT_Assesment.html")
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
                result["success"] = True

                if result['success']:
                    st.success("Opportunity created successfully!")
                else:
                    st.error("Error creating Opportunity")
                    st.error("\n".join(result['errors']))

            except Exception as e:
                st.error(f'Error trying to send Form! {e}')
                st.error('Please, Try again.')
                st.error('If problem persists, pleas contact Administrator.')


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
