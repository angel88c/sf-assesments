import json
from datetime import datetime
import streamlit as st

# Cargar el JSON proporcionado
data = {
    "project_name": "BDU III",
    "date": "2025-03-10",
    "project_start_date": "2025-03-17",
    "contact_name": "Antonio Tirado",
    "contact_phone": "7871231315432",
    "duplicated": "No",
    "contact_email": "antonio_T@lear.com",
    "customer_name": "Lear Apodaca",
    "cad_files_and_program": "No",
    "cad_files": "No",
    "process_spec": "Yes",
    "nests": "No",
    "qty_nests": "1",
    "plc_programming_standard": "Yes",
    "sow_ergonomic_spec": "Yes",
    "layout": "Yes",
    "dimensions": "1.5m x 2m",
    "product_manufacturing_sheet": "No",
    "traceability": "Yes",
    "traceability_name": "ITAC",
    "estimated_cycle_time": "Yes",
    "cycle_time": "25 sec",
    "special_handling": "No",
    "special_handling_info": "",
    "customer_has_samples": "No",
    "station_type": "Stand Alone",
    "station_type_info": "Station like BDU Vision",
    "process_type": "Screwing Station",
    "process_type_info": "NA",
    "uut_handle_mode": "Human",
    "uut_handle_mode_info": "",
    "uut_charged_mode_info": "NA",
    "device_under_process": "Housing",
    "design_required": "No",
    "design_required_info": "",
    "certifications_required": "No",
    "certifications_info": "",
    "preferent_hardware": "PLC Wago or Siemens, Cognex Vision System, Atlas Copco Screw Driver",
    "acceptance_criteria": "10 units reporting continuously to iTAC",
    "general_info_requirement": "",
    "travel": "Apodaca, Nuevo Le\u00f3n",
    "entity_po": "Nuevo Leon",
    "additional_comments": "Considera to have a Budgetary for Mar 28"
}

def json_to_html(data):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>IAT Report</title>
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
                    <h2 class="mb-1 text-primary">IAT Report</h2>
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
                    {key_value('Customer Name', data['customer_name'])}
                    {key_value('Duplicated Project', data['duplicated'])}
                    {key_value('If Its duplicated project, do you have the CAD & PLC program files?', data['cad_files_and_program'])}

                    <!-- Technical Specs -->
                    <div class="section-title">Milestones</div>
                    {key_value('CAD Files', data['cad_files'])}
                    {key_value('Process Spec', data['process_spec'])}
                    {key_value('Nests', data['nests'])}
                    {key_value('How Many Nests?', data['qty_nests'])}
                    
                    
                    
                   

                    <!-- Testing -->
                    <div class="section-title">Testing Configuration</div>
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
                    
                    
                    <!-- Additional Info -->
                    <div class="section-title">Additional Information</div>
                    {key_value('Preferent Hardware required? Describe the brands', data['preferent_hardware'])}
                    {key_value('Define the Acceptance Criteria.', data['acceptance_criteria'])}
                    {key_value('Briefly describe your need and what is most important to you in the project', data['general_info_requirement'])}
                    {key_value('Travel (Indicate the place of delivery)', data['travel'])}
                    {key_value('Entity from which the PO will come?', data['entity_po'])}
                    {key_value('Aditional Comments', data['additional_comments'])}

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
    file_name="iat_report.html",
    mime="text/html"
)
