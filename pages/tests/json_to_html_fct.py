import json
from datetime import datetime
import streamlit as st

# Cargar el JSON proporcionado
data = {
    "project_name": "Air Force 1",
    "contact_name": "Donald J. Trump",
    "contact_email": "donald@uus.com",
    "is_duplicated": "No",
    "date": "2025-03-07",
    "project_start_date": "2025-03-07",
    "contact_phone": "3321564977",
    "cad_files": "Yes",
    "gerber_files": "Yes",
    "schematics": "No",
    "boms": "No",
    "traceability_system": "Yes",
    "sow": "No",
    "product_finish": "Assembly",
    "test_strategy": "Depanelized",
    "connection_interface": "MACPANEL",
    "drawings": "Yes",
    "test_spec": "Yes",
    "parallel_testing": "Yes",
    "security_specification": "No",
    "traceability_system_name": "ITAC",
    "ergonomy_specifications": "NA",
    "osp_finish": "No",
    "quantity_uut": 2,
    "fixture_vendor": "Rematek",
    "studies_necessaries": [
        "MSA",
        "GRR"
    ],
    "qty_microstrains": "600",
    "rosettes": "10",
    "fixture_needs": "The fixture need to be nest interchangeable",
    "hardware_option": "NI",
    "system_type": "ECUTS",
    "station_type": "EOL",
    "Process_type": "Offline",
    "dm_position": "Centered on Top",
    "scanner_brand": "Keyence",
    "modifications_customer": "No",
    "test_sequencer": "Select Option",
    "dimensions": "No",
    "test_execution_conditions": "No",
    "dimensions_spec": "",
    "test_execution_conditions_spec": "",
    "single_product": "No",
    "self_test_required": "No",
    "certification_required": "No",
    "single_product_info": "",
    "self_test_required_info": "",
    "certification_required_info": "",
    "certifications_option": "Other",
    "additional_comments": ""
}

def json_to_html(data):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>FCT Report</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .data-row {{
                border-bottom: 1px solid #dee2e6;
                padding: 0.8rem 0;
            }}
            .data-key {{
                font-weight: 500;
                color: #2c3e50;
                padding-right: 1rem;
            }}
            .data-value {{
                color: #4a5568;
            }}
            .section-title {{
                font-size: 1.1rem;
                font-weight: 600;
                color: #1a365d;
                margin: 1.5rem 0 0.5rem;
                padding-bottom: 0.3rem;
                border-bottom: 2px solid #e2e8f0;
            }}
        </style>
    </head>
    <body class="bg-light">
        <div class="container-lg mt-4 mb-5">
            <div class="bg-white rounded-3 p-4 shadow-sm">
                <!-- Header -->
                <div class="mb-4 border-bottom pb-2">
                    <h2 class="mb-1 text-primary">FCT Report</h2>
                    <div class="text-muted small">
                        Project: {data['project_name']} | Date: {data['date']}
                    </div>
                </div>

                <!-- Main Content -->
                <div class="mx-3">
                    <!-- Contact Info -->
                    <div class="section-title">Contact Information</div>
                    {key_value('Contact Name', data['contact_name'])}
                    {key_value('Phone', data['contact_phone'])}
                    {key_value('Email', data['contact_email'])}
                    {key_value('Date', data['date'])}
                    {key_value('Probable Start Date', data['project_start_date'])}
                    {key_value('Fixture Vendor', data['fixture_vendor'])}
                    {key_value('Duplicated Project', data['is_duplicated'])}

                    <!-- Technical Specs -->
                    <div class="section-title">Technical Specifications</div>
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

                    <!-- Testing -->
                    <div class="section-title">Testing Configuration</div>
                    {key_value('How many Units Under Test?', data['quantity_uut'])}
                    {key_value('Hardware Option', data['hardware_option'])}
                    {key_value('System Type', data['system_type'])}
                    {key_value('Station Type', data['station_type'])}
                    {key_value('Process Type', data['Process_type'])}
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
                    
                    <!-- Additional Info -->
                    <div class="section-title">Additional Information</div>
                    {key_value('Aditional Comments', data['additional_comments'] or 'None')}

                    <!-- Footer -->
                    <div class="mt-4 pt-2 text-end small text-muted">
                        Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

def key_value(key, value):
    return f"""
    <div class="row data-row">
        <div class="col-4 data-key">{key}</div>
        <div class="col-8 data-value">{value or 'N/A'}</div>
    </div>
    """

def format_list(items):
    filtered = [item for item in items if item.strip()]
    return ", ".join(filtered) if filtered else "None"

# Generate and display
html_output = json_to_html(data)
st.components.v1.html(html_output, width=800, height=1000, scrolling=True)

# Download
st.download_button(
    "⬇️ Download Report",
    data=html_output,
    file_name="fct_report.html",
    mime="text/html"
)
