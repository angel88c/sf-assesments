
def validate_fields(fields):
    required_fields = ["project_name", 
                       "contact_name",
                       "fixture_type",
                       "date", 
                       "contact_email",
                       "quantity_devices",
                       "program_devices",
                       "programmer_brand",
                       "versions"
                    ]
    error_strings = []
    for required_field in required_fields:
        if required_field in fields:
            if fields[required_field] == "":
                error_strings.append(f"El campo {required_field} es obligatorio.")

    if error_strings:
        return error_strings

    return []

if __name__ == "__main__":
        
    info = {
        "project_name": "Fedora",
        "contact_name": "Federer",
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
        "program_devices": [
            "R78LF",
            "PIC16F",
            "",
            ""
        ],
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
        "travel_place": ""
    }
    
    error_strings = validate_fields(info)
    for error in error_strings:
        print(error)