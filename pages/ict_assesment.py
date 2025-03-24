import json
import os
import shutil
from pages.utils.ict_create_html import *
from pages.utils.constants import *
from pages.utils.salesforce_access import *
from pages.utils.dates_info import *
from pages.utils.test_account_names import *
from pages.utils.global_styles import *

import streamlit as st
from decouple import config
from datetime import datetime
from PIL import Image

st.set_page_config(initial_sidebar_state="collapsed")

set_global_styles()

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
                       "fixture_type",
                       "date",
                       "contact_email"
                    ]

    error_strings = []
    for required_field in required_fields:
        if required_field in fields:
            if fields[required_field] == "":
                error_strings.append(
                    f"El campo {required_field} es obligatorio.")

    if error_strings:
        return error_strings

    return []

load_ibtest_logo()
st.title("In Circuit Test Assesment")

info = dict()
YEAR = str(datetime.today().year)

# Crear un formulario
with st.form(key='ict_assesment'):
    col1, col2 = st.columns(2)
    with col1:
        info["project_name"] = st.text_input(
            'Name or Project Reference', placeholder="Enter the name of the project", )
        info["contact_name"] = st.text_input(
            'Contact', placeholder="Enter your name")
        info['country'] = st.selectbox('Country', options=COUNTRIES_DICT.keys())
        #info["customer_name"] = st.text_input(
        #    'Customer Name or Plant', placeholder="Enter the name of the customer or Plant", )
        #st.selectbox("Accounts", options=ACCOUTS, index=None )
        info["customer_name"] = st.selectbox("Accounts", options=get_account_names_from_local_file(), index=None)
        
        info["contact_phone"] = st.text_input(
            'Phone Number', placeholder="Enter your phone number")
       
    with col2:
        info["date"] = st.date_input('Date').strftime("%Y-%m-%d")
        info["contact_email"] = st.text_input('Email')
        info["is_duplicated"] = st.radio(
            'Duplicated Fixture?', YES_NO, index=1, horizontal=True)
        info["customer_name2"] = st.text_input('If Account does not exist, write here', placeholder="Enter Customer name")
        info["fixure_type"] = st.radio(
            'Fixture Type', FIXTURE_TYPES, horizontal=True)

    info["inline_bottom_side"] = st.text_input(
        'For InLine systems, which is the bottom side')

    st.header('Upload Files')
    uploaded_files = st.file_uploader(
        "Upload your files to share with us.", accept_multiple_files=True)

    st.markdown('<p style="margin-bottom: 2px;">CAD files (Odb ++, *.cad, *.neu, *.fab, *.pad, *.asc, *.ipc, etc)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Gerber files</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Schematics (pdf)</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Test Spec (pdf, doc)"</p>', unsafe_allow_html=True)
    st.markdown('<p style="margin-bottom: 2px;">Board directory (.tar.gz, .tar)</p>', unsafe_allow_html=True)

    
    # Sección 2: Preferencias|
    st.header("Feature Fixture")

    col1, col2, col3 = st.columns(3)
    with col1:
        info['activation_type'] = st.radio(
            'Activation Type', ACTIVATION_TYPES, help="")
    with col2:
        info['well_type'] = st.radio('Well Type', WELL_TYPES)
    with col3:
        info['size_type'] = st.radio('Size Type', SIZE_TYPES)

    st.divider()

    info['flash_programming'] = st.radio(
        'Flash Programming?', REQ_OPTIONS,
        horizontal=True,
        help="If some device will be programmed at ICT, mark as desired")

    col1, col2 = st.columns(2)
    with col1:
        info['quantity_devices'] = st.number_input(
            "How many devices should be programmed?", placeholder="Enter the number of devices to program", min_value=0, value=0)

    devices = []
    with col2:
        devices.append(st.text_input('Device 1 Part Number'))
        devices.append(st.text_input('Device 2 Part Number'))
        devices.append(st.text_input('Device 3 Part Number'))
        devices.append(st.text_input('Device 4 Part Number'))

    info["program_devices"] = devices
    info["programmer_brand"] = st.text_input(
        'What Programmer (Brand) do you want us to use?',
        help="Preferred Programmer Brand, e.g. FlashRunner 2.0, Phyton, Algocraft, Segger, etc.")
    info['versions'] = st.number_input(
        "How many versions?", placeholder="Enter the number of versions to consider", value=0)

    st.text("Select what applies")

    cols = st.columns(2)
    with cols[0]:
        info['logistic_data'] = st.radio(
            OPTIONS[0], YES_NO, index=1, horizontal=True)
        info['config_file'] = st.radio(
            OPTIONS[1], YES_NO, index=1, horizontal=True)
        info['test_spec'] = st.radio(
            OPTIONS[2], YES_NO, index=1, horizontal=True)
        info['fixture_sow'] = st.radio(
            OPTIONS[3], YES_NO, index=1, horizontal=True)

    with cols[1]:
        info['panel_test'] = st.radio(
            OPTIONS[4], YES_NO, index=1, horizontal=True)
        # if info['panel_test'] == 'Yes':
        info['quantity_panel'] = st.number_input(
            'Quantity Boards on Panel?', value=0)
        info['individual_test'] = st.radio(
            OPTIONS[5], YES_NO, index=1, horizontal=True)
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
    info['custom_tests'] = st.radio(
        'Apply Some custom tests?', YES_NO, index=1, horizontal=True)
    info['custom_tests_info'] = st.text_input('Specify More information')

    info['switch_probe_on_connector'] = st.radio(
        'Switch probe on connector required?', YES_NO, index=1, horizontal=True)
    info['color_test'] = st.radio(
        'Color/intensity LED test required and preferred sensor?', YES_NO, index=1, horizontal=True)
    info['color_test_info'] = st.text_input('More information')

    info['fixture_supplier'] = st.radio(
        'Fixture supplier preferred', YES_NO, index=1, horizontal=True)
    info['fixture_supplier_info'] = st.text_input(
        'Specify the preferred Fixture Vendor', placeholder='Circuit Check, Rematek, Arcadia, Juarez Technology, QxQ, etc.')

    col1, col2 = st.columns(2)
    with col1:
        info['clock_module'] = st.radio(
            'Clock Mode for Frequency measurement', REQ_OPTIONS, horizontal=True)
        info['boundary_scan'] = st.radio(
            'Boundary Scan Test', REQ_OPTIONS, horizontal=True)
        info['testjet'] = st.radio(
            'Testjet', REQ_OPTIONS, horizontal=True)
    with col2:
        info['silicon_nails'] = st.radio(
            'Silicon nails and CET', REQ_OPTIONS, horizontal=True)
        info['board_presence'] = st.radio(
            'Board Presence', REQ_OPTIONS, horizontal=True)
        info['travel_place'] = st.text_input(
            'Travel (Indicate the place to delivery)')

    # Sección 3: Comentarios Adicionales
    st.markdown("<h4>Additional Comments</h4>", unsafe_allow_html=True)
    comments = st.text_area(
        label_visibility='hidden', label="a", placeholder='Write your comments here...')

    info["additional_comments"] = comments

    # Botón de envío
    enviar = st.form_submit_button(
        'Submit', help='Sumbit form', type='primary')

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
                
                UPLOAD_FILES_FOLDER = os.path.join(config("PATH_FILE"), COUNTRIES_DICT[country], f"{info['customer_name']}", f"{info['project_name']}")
                if os.path.exists(UPLOAD_FILES_FOLDER):
                    st.error(f"Oppotunity with name {info['project_name']} already created, please contact Sales Manager to update your requirement.")
                    st.stop()
                
                os.makedirs(UPLOAD_FILES_FOLDER, exist_ok=True)
                shutil.copytree(config("TEMPLATE_ICT"), UPLOAD_FILES_FOLDER, dirs_exist_ok=True)
                
                # PATH = f"C:/Users/c_ang/Innovative Board Test SAPI de CV/admin - iBtest Assesment/ict_assesment_{current_datetime}.json"
                # PATH =  f"{PATH_FILE}/ict_assesment_{current_datetime}.json"
                ALL_INFO_SHARED_PATH = os.path.join(UPLOAD_FILES_FOLDER, "1_Customer_Info", "7_ALL_Info_Shared")
                PATH = os.path.join(UPLOAD_FILES_FOLDER, "ICT_Assesment.json")
                with open(PATH, 'w') as file:
                    json.dump(info, file, indent=4)

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
                    "Path__c": config("PATH_TO_SHAREPOINT")
                }

                if uploaded_files:
                    for file in uploaded_files:
                        save_path = os.path.join(ALL_INFO_SHARED_PATH, file.name)
                        with open(save_path, "wb") as f:
                            f.write(file.getbuffer())
                            
                #raise ValueError("Not uploaded to salesforce yet")
            
                st.write(new_opp)
                result =  st.session_state.salesforce.__getattr__('Opportunity').create(new_opp)
                result["success"] = True

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
