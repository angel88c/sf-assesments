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
                
                {testing_section(data)}
                {additional_section(data)}

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
        {key_value('Phone', data['contact_phone'])}
        {key_value('Customer Name or Plant', data['customer_name'])}
        {key_value('Email', data['contact_email'])}
        {key_value('Date', data['date'])}
        {key_value('Fixture Vendor', data['fixture_vendor'])}
        {key_value('Duplicated Project', data['is_duplicated'])}
         <!-- File Types -->
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
        {key_value('CAD Files', data['cad_files'])}
                    {key_value('Gerber Files', data['gerber_files'])}
                    {key_value('Schematics', data['schematics'])}
                    {key_value('BOMs', data['boms'])}
                    {key_value('Traceability System', data['traceability_system'])}
                    {key_value('Traceability System Name', data['traceability_system_name'])}
                    {key_value('Statement of Work', data['sow'])}
                    {key_value('Test Spec', data['test_spec'])}
                    {key_value('Specify how the product will be tested', data['product_finish'])}
                    {key_value('Test Strategy', data['test_strategy'])}
                    {key_value('Connection Interface', data['connection_interface'])}
                    {key_value('Drawings', data['drawings'])}
                    {key_value('Parallel Testing', data['parallel_testing'])}
                    {key_value('Security Specification', data['security_specification'])}
                    {key_value('Ergonomy Specification', data['ergonomy_specifications'])}
                    {key_value('OSP Finish', data['osp_finish'])}
                    {key_value('Quantity of MicroStrains if Straing Gauge', data['qty_microstrains'])}
                    {key_value('OSP Finish', data['osp_finish'])}
                    {key_value('Studies Necessaries', format_list(data['studies_necessaries']))}
                    {key_value('Rosettes', data['rosettes'])}
                    {key_value('Fixture Specific Needs', data['fixture_needs'])}

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
       {key_value('How many Units Under Test?', data['quantity_uut'])}
                    {key_value('Hardware Option', data['hardware_option'])}
                    {key_value('System Type', data['system_type'])}
                    {key_value('Station Type', data['station_type'])}
                    {key_value('Process Type', data['process_type'])}
                    {key_value('Speficied DM or Barcode Position and Scanner model', data['dm_position'])}
                    {key_value('Scanner Brand', data['scanner_brand'])}
                    {key_value('Does the customer want to make modifications to the system or test procesdure by himself?', data['modifications_customer'])}
                    {key_value('Test Sequencer', data['test_sequencer'])}
                    {key_value('Expected dimensions for the testing system (limited space, height)?', data['dimensions'])}
                    {key_value('', data['dimensions_spec'])}
                    {key_value('Test Execution under specific conditions (High/Low Temperature, Humidity, control cabin or chamber, etc.)', data['test_execution_conditions'])}
                    {key_value('', data['test_execution_conditions_spec'])}
                    {key_value('he System will only be used for a single product or different products', data['single_product'])}
                    {key_value('', data['single_product_info'])}
                    {key_value('Self Test required for product and testing system?', data['self_test_required'])}
                    {key_value('', data['self_test_required_info'])}
                    {key_value('Certifications Required?', data['certification_required'])}
                    {key_value('', data['certification_required_info'])}
                    {key_value('Other Certification', data['certifications_option'])}
    </div>
    """
    
def additional_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Miscellaneous</h3>
        {key_value('Aditional Comments', data['additional_comments'] or 'None')}
    </div>
    """