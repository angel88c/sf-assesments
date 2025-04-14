import json
import os
import shutil
from pages.utils.ict_create_html import *
from pages.utils.constants import *
from pages.utils.salesforce_access import *
from pages.utils.dates_info import *
from pages.utils.test_account_names import *
from pages.utils.global_styles import *
from pages.utils.validations import *

import streamlit as st
from decouple import config
from datetime import datetime
from PIL import Image

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
    st.markdown('<p style="margin-bottom: 1px;">Board directory (.tar.gz, .tar)</p>', unsafe_allow_html=True)

    return uploaded_files


load_ibtest_logo()
st.title("In Circuit Test Assesment")

info = dict()
YEAR = str(datetime.today().year)
BU = "ICT"
PROJECTS_FOLDER = "1_In_Circuit Test (ICT)"

# Crear un formulario
with st.form(key='ict_assesment'):
    
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
        
    col1, col2 = st.columns(2)
    with col1:
        info["is_duplicated"] = st.radio(r'*Duplicated Fixture?', YES_NO, index=1, horizontal=True)
    with col2:
        info["fixure_type"] = st.radio(r'*Fixture Type', FIXTURE_TYPES, horizontal=True)
        
    info["inline_bottom_side"] = st.text_input(
        'For InLine systems, which is the bottom side?', placeholder="Bottom side of PCB for Test System, e. g. Conenctor Side, main uc side, Layer")

    uploaded_files = upload_files()

    # Sección 2: Preferencias|
    #with st.container(border=True):
    st.header("Feature Fixture")
    col1, col2, col3 = st.columns(3)
    with col1:
        info['activation_type'] = st.radio(r'*Activation Type', options=ACTIVATION_TYPES)
    with col2:
        info['well_type'] = st.radio(r'*Well Type', WELL_TYPES)
    with col3:
        info['size_type'] = st.radio(r'*Size Type', SIZE_TYPES)

    st.divider()

    info['flash_programming'] = st.radio(
        'Flash Programming?', REQ_OPTIONS,
        horizontal=True)
    
    text_enter = st.text_input("Enter the numbers of devices to program, use comma to separate them.", placeholder="TC387, PIC16F628, MC9S12EXBP")
    devices = text_enter.split(",")
    info["program_devices"] = devices
    info["quantity_devices"] = len(devices)
    
    # col1, col2 = st.columns(2)
    # with col1:
    #     info['quantity_devices'] = st.number_input(
    #         "How many devices should be programmed?", placeholder="Enter the number of devices to program", min_value=0, value=0)

    # devices = []
    # with col2:
    #     devices.append(st.text_input('Device 1 Part Number'))
    #     devices.append(st.text_input('Device 2 Part Number'))
    #     devices.append(st.text_input('Device 3 Part Number'))
    #     devices.append(st.text_input('Device 4 Part Number'))

    info["program_devices"] = devices
    info["programmer_brand"] = st.text_input(
        'What Programmer (Brand) do you want us to use?', placeholder="FlashRunner 2.0, FRCube, Phyton, Algocraft, Segger, etc.")
    info['versions'] = st.number_input(
        "How many versions?", placeholder="Enter the number of versions to consider", value=0)

    st.text("Select what applies")

    cols = st.columns(2)
    with cols[0]:
        info['logistic_data'] = st.radio(
            OPTIONS[0], YES_NO, index=1, horizontal=True)
        info["items_for_logistic_data"] = st.text_input(
            OPTIONS[1], placeholder="Part Number, Serial Number, Security Key etc.")
        info['config_file'] = st.radio(
            OPTIONS[2], YES_NO, index=1, horizontal=True)
        info['test_spec'] = st.radio(
            OPTIONS[3], YES_NO, index=1, horizontal=True)
        info['fixture_sow'] = st.radio(
            OPTIONS[4], YES_NO, index=1, horizontal=True)

    with cols[1]:
        info['panel_test'] = st.radio(
            OPTIONS[5], YES_NO, index=1, horizontal=True)
        # if info['panel_test'] == 'Yes':
        info['quantity_panel'] = st.number_input(
            'Quantity Boards on Panel?', value=0)f
        info['individual_test'] = st.radio(
            OPTIONS[6], YES_NO, index=1, horizontal=True)
        info['quantity_nest'] = st.number_input('Specify Nest Qty?', value=0)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        info['automatic_scanner'] = st.radio(
            'Automatic Scanner', REQ_OPTIONS, index=2, horizontal=True)
    with col2:
        info['window_and_holder'] = st.radio(
            'Window and Holder for Scanner?', YES_NO, index=1, horizontal=True)

    st.divider()

    st.text("Select the option")
    
    col1, col2 = st.columns(2)
    with col1:  info['custom_tests'] = st.radio(r'* Apply Some custom tests?', YES_NO, index=1, horizontal=True)
    with col2:  info['custom_tests_info'] = st.text_input('Specify', placeholder="CAN Communication, CyberSecurity, LIN, etc.")

    info['switch_probe_on_connector'] = st.radio(r'* Switch probe on connector required?', YES_NO, index=1, horizontal=True)

    col1, col2 = st.columns(2)    
    with col1:  info['color_test'] = st.radio('Color/intensity LED test required and preferred sensor?', YES_NO, index=1, horizontal=True)
    with col2:  info['color_test_info'] = st.text_input('Specify', placeholder="Color Test, Feasa Led Analyzer/Optimistic.")

    info['fixture_supplier'] = st.radio('Fixture supplier preferred', YES_NO, index=1, horizontal=True)
    info['fixture_supplier_info'] = st.text_input('Specify the preferred Fixture Vendor', placeholder='Circuit Check, Rematek, Arcadia, Juarez Technology, QxQ, etc.')

    col1, col2 = st.columns(2)
    with col1:
        info['clock_module'] = st.radio(r'*Clock Mode for Frequency measurement', REQ_OPTIONS, horizontal=True)
        info['boundary_scan'] = st.radio(r'*Boundary Scan Test', REQ_OPTIONS, horizontal=True)
        info['testjet'] = st.radio('Testjet', REQ_OPTIONS, horizontal=True)
    with col2:
        info['silicon_nails'] = st.radio(r'*Silicon nails and CET', REQ_OPTIONS, horizontal=True)
        info["rqeuired_ics"] = st.text_input("Which ICs are considered in the chain?", placeholder="MC9S12XEBP")
        info['board_presence'] = st.radio(r'*Board Presence', REQ_OPTIONS, horizontal=True)
        
    # Sección 3: Comentarios Adicionales
    st.markdown("<h4>Additional Information</h4>", unsafe_allow_html=True)
    info["travel"] = st.text_input(r"*Travel (Indicate the place of Delivery).", placeholder="San Juan del Río")
    info["entity_po"] = st.text_input(r"*The entity that the PO will come from.", placeholder="Queretaro")
    info["additional_comments"] = st.text_area(label="Additional Comments", placeholder='Write your comments here...')

    # Botón de envío
    enviar = st.form_submit_button(
        'Submit', help='Sumbit form', type='primary')

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
                
                if os.path.exists(UPLOAD_FILES_FOLDER):
                    st.error(f"Oppotunity with name {info['project_name']} already created, please contact Sales Manager to update your requirement.")
                    st.stop()
                
                os.makedirs(UPLOAD_FILES_FOLDER, exist_ok=True)
                shutil.copytree(config("TEMPLATE_ICT"), UPLOAD_FILES_FOLDER, dirs_exist_ok=True)
                
                # PATH = f"C:/Users/c_ang/Innovative Board Test SAPI de CV/admin - iBtest Assesment/ict_assesment_{current_datetime}.json"
                # PATH =  f"{PATH_FILE}/ict_assesment_{current_datetime}.json"
                ALL_INFO_SHARED_PATH = os.path.join(UPLOAD_FILES_FOLDER, "1_Customer_Info", "7_ALL_Info_Shared")
                #PATH = os.path.join(UPLOAD_FILES_FOLDER, "ICT_Assesment.json")
                #with open(PATH, 'w') as file:
                #    json.dump(info, file, indent=4)

                html_data = json_to_html(info)
                if html_data:
                    PATH_HTML = os.path.join(UPLOAD_FILES_FOLDER, "ICT_Assesment.html")
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
                    "SALES_Due_Date__c": info["quotation_required_date"],
                    "BU__c": BU
                }
                
                if customer_in_list:
                    new_opp["AccountId"] = accounts_by_name.get(info["customer_name"], "")

                if uploaded_files:
                    for file in uploaded_files:
                        save_path = os.path.join(ALL_INFO_SHARED_PATH, file.name)
                        with open(save_path, "wb") as f:
                            f.write(file.getbuffer())
                            
                st.write(new_opp)
                raise ValueError("Not uploaded to salesforce yet")
        
                result =  st.session_state.salesforce.__getattr__('Opportunity').create(new_opp)
                #result["success"] = True

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
