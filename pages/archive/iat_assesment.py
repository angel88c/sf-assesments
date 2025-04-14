import json
import os
import shutil
from pages.utils.iat_create_html import *
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
    # Upload Files
    st.header('Are you sharing files?')
    uploaded_files = st.file_uploader(".", label_visibility="hidden", accept_multiple_files=True)
    
    st.markdown('<p style="margin-bottom: 1px;">*CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Drawings (2d, 3d)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Gerber files</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">PLC, HMI, Robot programming standards (Templates)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Test Spec (pdf, doc)"</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Product Spec.</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 1px;">Product manufacturing sheet.</p>', unsafe_allow_html=True)
    
    return uploaded_files

# Título de la aplicación
load_ibtest_logo()
st.title("Industrial Automation Test Assesment")

info = dict()
YEAR = str(datetime.today().year)
BU = "IAT"
PROJECTS_FOLDER = "4_Industrial Automation (IAT)"

# Crear un formulario
with st.form(key='iat_assessment'):
    
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
    
    info["duplicated"] = st.radio(
        r'*Duplicated Project', YES_NO, index=1, horizontal=True)
    info["cad_files_and_program"] = st.radio(
        r"*If it's Duplicated, Do you have the CAD and PLC Program files?", YES_NO, index=1, horizontal=True)


    uploaded_files = upload_files()

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
    
    st.markdown("<h4>Additional Information</h4>", unsafe_allow_html=True)
    info["travel"] = st.text_input(r"*Travel (Indicate the place of Delivery).", placeholder="San Juan del Río")
    info["entity_po"] = st.text_input(r"*The entity that the PO will come from.", placeholder="Queretaro")
    info["additional_comments"] = st.text_area(label="Additional Comments", placeholder='Write your comments here...')
        
    # Botón de envío
    enviar = st.form_submit_button('Submit', help='Submit form', type='primary')

    # Acciones al enviar el formulario
    if enviar:
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # valid_email = validate_email(info['contact_email'])
        # if not valid_email:
        #     st.error("Error!! Only Corporate emails are valid")
        #     st.stop()
            
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
                st.write(UPLOAD_FILES_FOLDER)
                if os.path.exists(UPLOAD_FILES_FOLDER):
                    st.error(f"Oppotunity with name {info['project_name']} already created, please contact Sales Manager to update your requirement.")
                    st.stop()
                    
                os.makedirs(UPLOAD_FILES_FOLDER, exist_ok=True)
                shutil.copytree(config("TEMPLATE_IAT"), UPLOAD_FILES_FOLDER, dirs_exist_ok=True)
                
                # PATH = f"C:/Users/c_ang/Innovative Board Test SAPI de CV/admin - iBtest Assesment/ict_assesment_{current_datetime}.json"
                # PATH =  f"{PATH_FILE}/ict_assesment_{current_datetime}.json"
                ALL_INFO_SHARED_PATH = os.path.join(UPLOAD_FILES_FOLDER, "1_Customer_Info", "3_ALL_Info_Shared")
                #PATH = os.path.join(UPLOAD_FILES_FOLDER, "IAT_Assesment.json")
                #with open(PATH, 'w') as file:
                #    json.dump(info, file, indent=4)

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
                #result["success"] = True

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
