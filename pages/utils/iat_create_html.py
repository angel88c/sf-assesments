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
        {key_value('Email', data['contact_email'])}
        {key_value('Date', data['date'])}
        {key_value('Customer Name', data['customer_name'])}
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
        {key_value('Process Spec', data['process_spec'])}
        {key_value('Nests', data['nests'])}
        {key_value('How Many Nests?', data['qty_nests'])}

    </div>
    """

def testing_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Testing Setup</h3>
        {key_value('PLC, HMI, Robot programming standards (Templates)', data['plc_programming_standard'])}
        {key_value('Sow and Ergonomic Specification', data['sow_ergonomic_spec'])}
        {key_value('Layout', data['layout'])}
        {key_value('Dimensions', data['dimensions'])}
        
        {key_value('Product Manufacturing Sheet', data['product_manufacturing_sheet'])}
        {key_value('Traceability System', data['traceability'])}
        {key_value('Traceability System Name', data['traceability_name'])}
        
        {key_value('Estimated process time or cyclic time?', data['estimated_cycle_time'])}
        {key_value('Cycle time', data['cycle_time'])}
        {key_value('Is any special handling of the unit needed?', data['special_handling'])}
        {key_value('Special Handling Info', data['special_handling_info'])}
        
        {key_value('Do you have Samples?', data['customer_has_samples'])}
        {key_value('Type of Station or Service?', data['station_type'])}
        {key_value('Type of Station Info', data['station_type_info'])}
        {key_value('Type of Proces?', data['process_type'])}
        {key_value('Type of Process Info', data['process_type_info'])}
        {key_value('How will the Unit be handled]?', data['uut_handle_mode'])}
        {key_value('More Information', data['uut_handle_mode_info'])}
        {key_value('Device under process', data['device_under_process'])}
        {key_value('Design (Drawings) are required?', data['design_required'])}
        {key_value('More Information', data['design_required_info'])}
        {key_value('Certifications required?', data['certifications_required'])}
        {key_value('More Information', data['certifications_info'])}
    </div>
    """
    
def additional_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Miscellaneous</h3>
        {key_value('Preferent Hardware required? Describe the brands', data['preferent_hardware'])}
        {key_value('Define the Acceptance Criteria.', data['acceptance_criteria'])}
        {key_value('Briefly describe your need and what is most important to you in the project', data['general_info_requirement'])}
        {key_value('Travel (Indicate the place of delivery)', data['travel'])}
        {key_value('Entity from which the PO will come?', data['entity_po'])}
        {key_value('Aditional Comments', data['additional_comments'])}

    </div>
    """