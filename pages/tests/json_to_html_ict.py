import json
from datetime import datetime
import streamlit as st

# Cargar el JSON proporcionado
data = {
    "project_name": "Fedora",
    "contact_name": "Angel Browwn",
    "contact_phone": "3335985518",
    "fixure_type": "Offline",
    "date": "2025-02-19",
    "contact_email": "angel.brown@ict.com",
    "is_duplicated": "No",
    "inline_bottom_side": "Top A",
    "activation_type": "Vacuum box",
    "well_type": "Single well",
    "size_type": "Small kit",
    "flash_programming": "Required",
    "quantity_devices": 2,
    "program_devices": ["R78LF", "PIC16F", "", ""],
    "programmer_brand": "",
    "versions": 0,
    "logistic_data": "No",
    "config_file": "No",
    "test_spec": "No",
    "fixture_sow": "No",
    "panel_test": "No",
    "quantity_panel": 0,
    "individual_test": "No",
    "quantity_nest": 0,
    "automatic_scanner": "NA",
    "window_and_holder": "No",
    "custom_tests": "No",
    "custom_tests_info": "",
    "switch_probe_on_connector": "No",
    "color_test": "No",
    "color_test_info": "",
    "fixture_supplier": "No",
    "fixture_supplier_info": "",
    "clock_module": "NA",
    "boundary_scan": "NA",
    "testjet": "NA",
    "silicon_nails": "NA",
    "board_presence": "NA",
    "travel": ""
}


def json_to_html(data):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ICT Report</title>
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
                    <h2 class="mb-1 text-primary">ICT Report</h2>
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
                    {key_value('Fixture Supplier', data['fixture_supplier'])}
                    {key_value('Supplier Info', data['fixture_supplier_info'])}
                    
                    <!-- Fixture Types -->
                    <div class="section-title">Uploaded File Types</div>
                    {
                        ''.join([key_value(f"Type {i+1}", file_type) for i, file_type in enumerate(data["file_types"])])
                        if data.get("file_types") else key_value("File Types", "None")
                    }

                    <!-- Technical Specs -->
                    <div class="section-title">Technical Specifications</div>
                    {key_value('Fixture Type', data['fixure_type'])}
                    {key_value('Activation Type', data['activation_type'])}
                    {key_value('Well Type', data['well_type'])}
                    {key_value('Size Type', data['size_type'])}
                    {key_value('Flash Programming', data['flash_programming'])}
                    {key_value('Device Quantity', data['quantity_devices'])}
                    {key_value('Versions', data['versions'] or 'None')}

                    <!-- Programming -->
                    <div class="section-title">Programming</div>
                    {key_value('Devices to Program', format_list(data['program_devices']))}
                    {key_value('Programmer Brand', data['programmer_brand'] or 'None')}
                    {key_value('Duplicated', data['is_duplicated'])}

                    <!-- Testing -->
                    <div class="section-title">Testing Configuration</div>
                    {key_value('Panel Test', data['panel_test'])}
                    {key_value('Panel Quantity', data['quantity_panel'])}
                    {key_value('Individual Test', data['individual_test'])}
                    {key_value('Custom Tests', data['custom_tests'])}
                    {key_value('Color Test', data['color_test'])}

                    <!-- Additional Info -->
                    <div class="section-title">Additional Information</div>
                    {key_value('Automatic Scanner', data['automatic_scanner'])}
                    {key_value('Boundary Scan', data['boundary_scan'])}
                    {key_value('Travel Place', data['travel'] or 'None')}

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
    file_name="ict_report.html",
    mime="text/html"
)
