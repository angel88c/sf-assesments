
import streamlit as st
from datetime import datetime

def key_value(key, value):
    return f"""
    <div class="row data-row">
        <div class="col-5 data-key">{key}</div>
        <div class="col-7 data-value">{value if value != '' else 'N/A'}</div>
    </div>
    """

def dict_block(title, d):
    html = f'<div class="section-title">{title}</div>'
    for k, v in d.items():
        html += key_value(k, "Yes" if v is True else "No" if v is False else str(v))
    return html

def sqc_block(title, d):
    html = ''
    if isinstance(d, dict):
        html += f"<div class='mb-1 fw-semibold'>{title}</div>"
        html += f"<div class='ms-3'>{key_value('Status', d.get('Status', ''))}{key_value('Qty', d.get('Qty', ''))}{key_value('Comments', d.get('Comments', ''))}</div>"
    else:
        html += key_value(title, d)
    return html

def nested_dict_block(title, d):
    html = f'<div class="section-title">{title}</div>'
    for k, v in d.items():
        if isinstance(v, dict):
            html += f"<div class='mb-1 fw-semibold'>{k}</div>"
            html += f"<div class='ms-3'>{key_value('Status', v.get('Status', ''))}{key_value('Qty', v.get('Qty', ''))}{key_value('Comments', v.get('Comments', ''))}</div>"
        else:
            html += key_value(k, v)
    return html

def additional_section(data):
    return f"""
    <div class="space-y-2">
        <h3 class="text-lg font-semibold text-gray-700">Miscellaneous</h3>
        {key_value('Aditional Comments', data['additional_comments'] or 'None')}
    </div>
    """

def json_to_html(data):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Quotation Request</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .data-row {{
                border-bottom: 1px solid #dee2e6;
                padding: 0.6rem 0;
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
                <div class="mb-4 border-bottom pb-2">
                    <h2 class="text-primary">Quotation Request</h2>
                    <div class="text-muted small">Project: {data['project_name']} | Date: {data['date']}</div>
                </div>

                <div class="mx-3">
                    <div class="section-title">Basic Info</div>
                    {key_value("Contact Name", data["contact_name"])}
                    {key_value("Contact Email", data["contact_email"])}
                    {key_value("Phone", data["contact_phone"])}
                    {key_value("Customer Name", data["customer_name"] or data["customer_name2"])}
                    {key_value("Country", data["country"])}
                    {key_value("Duplicated Project", data["is_duplicated"])}
                    {key_value("Required Quotation Date", data["quotation_required_date"])}

                    {dict_block("File Types Provided", data["file_types"])}

                    <div class="section-title">Product Details</div>
                    {key_value("Product Use Type", data["product_use_type"])}
                    {key_value("Use Type Comments", data["product_use_type_comments"])}
                    {key_value("Test Type", data["test_type"])}
                    {key_value("Test Type Comments", data["test_type_comments"])}
                    {key_value("DUT Assembly Level", data["dut_assembly_level"])}
                    {key_value("DUT Comments", data["dut_assembly_level_comments"])}
                    {sqc_block("Panel Test", data["Panel Test? (Qty boards on panel)"])}
                    {sqc_block("Individual Test", data["Individual Test? (Nest Qty per well)"])}
                    {sqc_block("NPI or Design Freeze", data["Is the product NPI or design freeze?"])}
                    {key_value("Purpose", data["purpose_fixture"])}
                    {key_value("Purpose Comments", data["purpose_fixture_comments"])}
                    {key_value("PCB Side", data["pcb_side"])}
                    {key_value("Manufacture Location", data["products_manufacture"])}
                    {key_value("Activation Type", data["activation_type"])}
                    {key_value("Well Type", data["well_type"])}
                    {key_value("Size Type", data["size_type"])}
                    {key_value("Number of Versions", data["versions"])}
                    {key_value("Fixture Vendor", data["fixture_vendor"])}

                    <div class="section-title">Fixture Configuration</div>
                    {key_value("Test Points", "Yes" if data["dut_test_points"] else "No")}
                    {key_value("Test Points Comments", data["dut_test_points_comments"])}
                    {key_value("Connectors", "Yes" if data["dut_connectors"] else "No")}
                    {key_value("Connectors Comments", data["dut_connectors_comments"])}
                    {key_value("Through Hole", "Yes" if data["dut_through_hole"] else "No")}
                    {key_value("Through Hole Comments", data["dut_through_hole_comments"])}
                    {key_value("Wire Harness", "Yes" if data["dut_wire_harness"] else "No")}
                    {key_value("Wire Harness Comments", data["dut_wire_harness_comments"])}
                    {key_value("RF Coaxial", "Yes" if data["dut_rf_coaxial"] else "No")}
                    {key_value("RF Coaxial Comments", data["dut_rf_coaxial_comments"])}
                    {key_value("Other", "Yes" if data["dut_other"] else "No")}
                    {key_value("Other Comments", data["dut_other_comments"])}
                    {sqc_block("Mass Interconnect System", data["Mass Interconnect System"])}
                    {sqc_block("Harness Connectors", data["Harness connectors"])}
                    {sqc_block("Special Connectors", data["Special connectors on fixture's back"])}
                    {sqc_block("Bottom nodes to access (TPs or connectors)", data["Bottom nodes to access (TPs or connectors)"])}
                    {sqc_block("Top nodes to access (TPs or pin connectos)", data["Top nodes to access (TPs or pin connectos)"])}
                    {sqc_block("Side access connections", data["Side access connections"])}
                    {sqc_block("Specify the type of socket's tail (wiring method)", data["Specify the type of socket's tail (wiring method)"])}

                    {sqc_block("Door closed lock", data["Door closed lock"])}
                    {sqc_block("Automatic Opening", data["Automatic Opening"])}
                    {sqc_block("Counter", data["Counter"])}
                    {sqc_block("Product precense sensor", data["Product precense sensor"])}
                    {sqc_block("BoardMarkes", data["BoardMarkes"])}
                    {sqc_block("Scanner (Please specify type: DM, QR, Barcode. And specify brand preference)", data["Scanner (Please specify type: DM, QR, Barcode. And specify brand preference)"])}
                    {sqc_block("LED Test (Please specify brand preferrence, type of test Color/Intensity)", data["LED Test (Please specify brand preferrence, type of test Color/Intensity)"])}
                    {sqc_block("Instalation of special hardware on the fixture is needed (If it does please specify)", data["Instalation of special hardware on the fixture is needed (If it does please specify)"])}
                    {sqc_block("Does the fixture need internal wiring labor?", data["Does the fixture need internal wiring labor?"])}
                    {sqc_block("FEA Study?", data["FEA Study?"])}
                    {sqc_block("Strain gage study? (Please specify qty. of rossetes)", data["Strain gage study? (Please specify qty. of rossetes)"])}

                    {additional_section(data)}

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