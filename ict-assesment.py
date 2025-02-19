
import requests
import json
import streamlit as st
from simple_salesforce import Salesforce
from decouple import config
from datetime import datetime

def connect_to_salesforce():
    try:
        sf_info = dict()
        # Obtener credenciales desde el archivo .env
        sf_info["username"] = config('SALESFORCE_USERNAME')
        sf_info["password"] = config('SALESFORCE_PASSWORD')
        sf_info["security_token"] = config('SALESFORCE_SECURITY_TOKEN')
        sf_info["consumer_key"] = config('SALESFORCE_CONSUMER_KEY')
        sf_info["consumer_secret"] = config('SALESFORCE_CONSUMER_SECRET')

        # Conectar a Salesforce
        sf = Salesforce(
            username=sf_info["username"],
            password=sf_info["password"],
            security_token=sf_info["security_token"],
            consumer_key=sf_info["consumer_key"],
            consumer_secret=sf_info["consumer_secret"]
        )

        #st.success("Conexión exitosa a Salesforce!")
        #st.write(sf)

        redirect_uri = config("REDIRECT_URL")  #f'https://login.salesforce.com/services/oauth2/callback'
        token_url = config("TOKEN_URL")        #f'https://login.salesforce.com/services/oauth2/token'
        payload = {
            'grant_type': 'password',
            'client_id': sf_info["consumer_key"],
            'client_secret': sf_info["consumer_secret"],
            'username': sf_info["username"],
            'password': sf_info["password"] + sf_info["security_token"]
        }

        response = requests.post(token_url, data=payload)
        token_data = response.json()
        # if "access_token" in token_data:
        #     st.success("Token de acceso obtenido exitosamente!")
        #     st.write(token_data["access_token"])

        return sf

    except Exception as e:
        st.error(f"Error al conectar a Salesforce: {e}")
        return None
    
def add_device(value):
    if not "devices" in st.session_state:
        st.session_state.devices = value

# Título de la aplicación
st.title("ICT Assesment")

sf = connect_to_salesforce()

info = dict()

# Crear un formulario
with st.form(key='ict_assesment'):
    # Sección 1: Información Personal
    # st.header("Contact Information")

    col1, col2 = st.columns(2)
    with col1:
        info["project_name"] = st.text_input(
            'Name or Project Reference', placeholder="Enter the name of the project")
        info["contact_name"] = st.text_input(
            'Contact', placeholder="Enter your name")
        info["contact_phone"] = st.text_input(
            'Phone Number', placeholder="Enter your phone number")

        info["fixure_type"] = st.radio('Fixture Type', ['Offline', 'InLine'])

    with col2:
        info["date"] = st.date_input('Date').strftime("%Y-%m-%d")
        info["contact_email"] = st.text_input('Email')
        info["is_duplicated"] = st.radio('Duplicated Fixture?', ['Yes', 'No'])

    info["inline_bottom_side"] = st.text_input(
        'For InLine systems, which is the bottom side')

    # Sección 2: Preferencias|
    st.header("Feature Fixture")
    ACTIVATION_TYPES = ['Vacuum box', 'Hold down gates',
                        'Pneumatic', 'Inline Test Fixture']
    WELL_TYPES = ['Single well', 'Dual well', 'Dual stage']
    SIZE_TYPES = ['Small kit', 'Large kit', 'Small extended', 'Large extended']

    col1, col2, col3 = st.columns(3)
    with col1:
        info['activation_type'] = st.radio('Activation Type', ACTIVATION_TYPES)
    with col2:
        info['well_type'] = st.radio('Well Type', WELL_TYPES)
    with col3:
        info['size_type'] = st.radio('Size Type', SIZE_TYPES)

    # st.markdown("<h4>Flash programming?</h4>", unsafe_allow_html=True)
    st.divider()
    # st.header("Flash Programming Options")
    # info['fixture_type'] = st.radio('Fixture Type', FIXTURE_TYPES)
    info['flash_programming'] = st.radio(
        'Flash Programming?', ['Required', 'Optional', 'NA'], horizontal=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        info['quantity_devices'] = st.number_input(
            "How many devices should be programmed?", placeholder="Enter the number of devices to program", min_value=0, value=0)
    
    devices = []
    with col2: 
        devices.append(st.text_input('Device 1 part number'))
        devices.append(st.text_input('Device 2 part number'))
        devices.append(st.text_input('Device 3 part number'))
        devices.append(st.text_input('Device 4 part number'))
    
    info["program_devices"] = devices
    # if info['quantity_devices'] > 0:
    #     st.text("Devices to be programmed")
    #     cols = st.columns(info['quantity_devices'])
    #     for i in range(info['quantity_devices']):
    #         with cols[i]:
    #             info[f'device_{i}'] = st.text_input(
    #                 f'Device {i+1} part number')

    info["programmer_brand"] = st.text_input(
        'What Programmer (Brand) do you want us to use?, e.g. FlashRunner 2.0, Phyton, Algocraft, Segger, etc.')
    info['versions'] = st.number_input(
        "How many versions?", placeholder="Enter the number of versions to consider", value=0)

    OPTIONS = ['Logistic data will be flashed?',
               'It has the config file and codeword data of the 3070?',
               'Do you have Test Spec?',
               'Do you have Fixture SOW?',
               'Panel Test? Specify Qty boards on the panel',
               'Individual test? Specify Nest Qty']

    st.text("Select what applies")

    cols = st.columns(2)
    with cols[0]:
        info['logistic_data'] = st.radio(
            OPTIONS[0], ['Yes', 'No'], index=1, horizontal=True)
        info['config_file'] = st.radio(
            OPTIONS[1], ['Yes', 'No'], index=1, horizontal=True)
        info['test_spec'] = st.radio(
            OPTIONS[2], ['Yes', 'No'], index=1, horizontal=True)
        info['fixture_sow'] = st.radio(
            OPTIONS[3], ['Yes', 'No'], index=1, horizontal=True)

    with cols[1]:
        info['panel_test'] = st.radio(
            OPTIONS[4], ['Yes', 'No'], index=1, horizontal=True)
        # if info['panel_test'] == 'Yes':
        info['quantity_panel'] = st.number_input(
            'Quantity Boards on Panel?', value=0)
        info['individual_test'] = st.radio(
            OPTIONS[5], ['Yes', 'No'], index=1, horizontal=True)
        info['quantity_nest'] = st.number_input('Specify Nest Qty?', value=0)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        info['automatic_scanner'] = st.radio(
            'Automatic Scanner', ['Required', 'Optional', 'NA'], index=2, horizontal=True)
    with col2:
        info['window_and_holder'] = st.radio('Window and Holder for Scanner?', [
                                             'Yes', 'No'], index=1, horizontal=True)

    st.divider()

    st.text("Select the option")
    info['custom_tests'] = st.radio('Apply Some custom tests?', [
                                    'Yes', 'No'], index=1, horizontal=True)
    info['custom_tests_info'] = st.text_input('Specify More information')

    info['switch_probe_on_connector'] = st.radio(
        'Switch probe on connector required?', ['Yes', 'No'], index=1, horizontal=True)
    info['color_test'] = st.radio(
        'Color/intensity LED test required and preferred sensor?', ['Yes', 'No'], index=1, horizontal=True)
    info['color_test_info'] = st.text_input('More informatio')

    info['fixture_supplier'] = st.radio('Fixture supplier preferred', [
                                        'Yes', 'No'], index=1, horizontal=True)
    info['fixture_supplier_info'] = st.text_input(
        'Specicy the Brand', placeholder='Circuit Check, Rematek, Arcadia, Juarez Technology, QxQ, etc.')

    col1, col2 = st.columns(2)
    with col1:
        info['clock_module'] = st.radio('Clock Mode for Frequency measurement', [
                                        'Required', 'Optional', 'NA'], index=2, horizontal=True)
        info['boundary_scan'] = st.radio(
            'Boundary Scan Test', ['Required', 'Optional', 'NA'], index=2, horizontal=True)
        info['testjet'] = st.radio(
            'Testjet', ['Required', 'Optional', 'NA'], index=2, horizontal=True)
    with col2:
        info['silicon_nails'] = st.radio('Silicon nails and CET', [
                                         'Required', 'Optional', 'NA'], index=2, horizontal=True)
        info['board_presence'] = st.radio(
            'Board Presence', ['Required', 'Optional', 'NA'], index=2, horizontal=True)
        info['travel_place'] = st.text_input(
            'Travel (Indicate the place to delivery)')

    # Sección 3: Comentarios Adicionales
    st.markdown("<h4>Comentarios Adicionales</h4>", unsafe_allow_html=True)
    comentarios = st.text_area(
        label_visibility='hidden', label="a", placeholder='Escribe tus comentarios aquí...')

    # Botón de envío
    enviar = st.form_submit_button(
        'Enviar', help='Enviar el formulario', type='primary')

    # Acciones al enviar el formulario
    if enviar:        
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            PATH = f"C:/Users/c_ang/Innovative Board Test SAPI de CV/admin - iBtest Assesment/ict_assesment_{current_datetime}.json"
            with open(PATH, 'w') as file:
                json.dump(info, file, indent=4)    
            

            opportunity_name = info["project_name"]
            stage_name = "Quoting"
            
            new_opp = {
                "Name": opportunity_name,
                "StageName": stage_name,
                "CloseDate": datetime.now().strftime("%Y-%m-%d"),
                "Assessment_Date__c": datetime.now().strftime("%Y-%m-%d"),
                "Path__c": config("PATH_TO_SHAREPOINT")
            }
            
            st.write(new_opp)
            
            result = sf.__getattr__('Opportunity').create(new_opp)
            
            if result['success']:
                st.success("Opportunity created successfully!")
            else:
                st.error("Error creating Opportunity")
                st.error("\n".join(result['errors']))
            
        except Exception as e:
            st.error(f'¡Error al enviar el formulario! {e}')
            st.error('Por favor, intenta de nuevo.')
            st.error('Si el problema persiste, contacta al administrador.')
        # st.write(info)

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
