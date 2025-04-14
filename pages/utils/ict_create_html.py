import streamlit as st
from datetime import datetime

def json_to_html(data):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Complete ICT Assesment Report</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
            body {{ font-family: 'Inter', sans-serif; }}
        </style>
    </head>
    <body class="bg-gray-50 min-h-screen p-8">
        <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-sm p-6">
            
            <!-- Header -->
            <div class="mb-6 border-b pb-4">
                <h1 class="text-2xl font-bold text-gray-800">
                    <span class="text-blue-600">Project Name:</span>  {data['project_name']}
                </h1>
                <div class="mt-2 text-sm text-gray-500">
                    Date: {data['date']}
                </div>
            </div>

            <!-- All Data Sections -->
            <div class="space-y-6">
                
                <!-- Dynamic Sections -->
                {contact_section(data)}
                {technical_section(data)}
                {programming_section(data)}
                {testing_section(data)}
                {additional_section(data)}
                {miscellaneous_section(data)}

                <!-- Footer -->
                <div class="pt-4 mt-6 text-sm text-gray-400 border-t">
                    Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def key_value(key, value):
    return f"""
    <div class="flex gap-4 py-2 border-b border-gray-100">
        <div class="w-1/3 font-medium text-gray-600">{key}</div>
        <div class="flex-1 text-gray-700">{value}</div>
    </div>
    """

def format_list(items):
    return ", ".join(filter(None, items)) if any(items) else "None"

def contact_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Contact Information</h3>
        {key_value('Quotation Required Date', data['quotation_required_date'])}
        {key_value('Contact Name', data['contact_name'])}
        {key_value('Phone Number', data['contact_phone'])}
        {key_value('Email Address', data['contact_email'])}
        {key_value('Fixture Supplier', data['fixture_supplier'])}
        <!-- Fixture Types -->
        <div class="section-title text-lg font-semibold text-gray-700">Uploaded File Types</div>
        {
            ''.join([key_value(file_type, "Yes") for file_type, value in data.get("file_types", {}).items() if value])
            if data.get("file_types") and any(data["file_types"].values()) else key_value("File Types", "None")
        }
    </div>
    """

def technical_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Technical Configuration</h3>
        {key_value('Fixture Type', data['fixure_type'])}
        {key_value('Activation Type', data['activation_type'])}
        {key_value('Well Type', data['well_type'])}
        {key_value('Size Type', data['size_type'])}
        {key_value('Inline Bottom Side', data['inline_bottom_side'])}
        {key_value('Flash Programming', data['flash_programming'])}
        {key_value('Quantity Devices', data['quantity_devices'])}
    </div>
    """

def programming_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Programming Details</h3>
        {key_value('Program Devices', format_list(data['program_devices']))}
        {key_value('Programmer Brand', data['programmer_brand'])}
        {key_value('Versions', data['versions'])}
        {key_value('Is Duplicated', data['is_duplicated'])}
    </div>
    """

def testing_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Testing Setup</h3>
        {key_value('Logistic Data', data['logistic_data'])}
        {key_value('Config File', data['config_file'])}
        {key_value('Test Spec', data['test_spec'])}
        {key_value('Fixture SOW', data['fixture_sow'])}
        {key_value('Panel Test', data['panel_test'])}
        {key_value('Panel Quantity', data['quantity_panel'])}
        {key_value('Individual Test', data['individual_test'])}
        {key_value('Nest Quantity', data['quantity_nest'])}
        {key_value('Automatic Scanner', data['automatic_scanner'])}
        {key_value('Window & Holder', data['window_and_holder'])}
        {key_value('Switch Probe', data['switch_probe_on_connector'])}
        {key_value('Color Test', data['color_test'])}
        {key_value('Color Test Info', data['color_test_info'])}
        
    </div>
    """

def additional_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Additional Components</h3>
        {key_value('Clock Module', data['clock_module'])}
        {key_value('Boundary Scan', data['boundary_scan'])}
        {key_value('TestJet', data['testjet'])}
        {key_value('ICs for Testjet', data['ics_with_testjet'])}
        {key_value('ICs for BS Chain', data['required_ics'])}
        {key_value('Silicon Nails', data['silicon_nails'])}
        {key_value('Board Presence', data['board_presence'])}
    </div>
    """

def miscellaneous_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Miscellaneous</h3>
        {key_value('Custom Tests', data['custom_tests'])}
        {key_value('Custom Tests Info', data['custom_tests_info'])}
        {key_value('Travel Place', data['travel'])}
        {key_value('Additional Comments', data['additional_comments'])}
    </div>
    """