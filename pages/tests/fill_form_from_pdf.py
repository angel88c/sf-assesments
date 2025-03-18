from pypdf import PdfReader, PdfWriter

def get_selectbox_fields(pdf_path):
    reader = PdfReader(pdf_path)
    selectbox_fields = {}

    # Loop through all pages
    for page_num, page in enumerate(reader.pages):
        if "/Annots" in page:
            for annot in page["/Annots"]:
                annot_obj = annot.get_object()
                if "/FT" in annot_obj and annot_obj["/FT"] == "/Ch":  # Dropdown field
                    field_name = annot_obj.get("/T", "Unnamed Field")
                    selected_value = annot_obj.get("/V", "No Selection")
                    options = annot_obj.get("/Opt", [])  # Get available options

                    # Convert option list to readable format
                    if isinstance(options, list):
                        options = [opt.get_object() if hasattr(opt, "get_object") else opt for opt in options]

                    selectbox_fields[field_name] = {
                        "selected": selected_value,
                        "options": options
                    }

    return selectbox_fields

def get_checkbox_fields(pdf_path):
    reader = PdfReader(pdf_path)
    checkbox_fields = {}

    # Loop through all pages
    for page_num, page in enumerate(reader.pages):
        if "/Annots" in page:
            for annot in page["/Annots"]:
                annot_obj = annot.get_object()
                if "/FT" in annot_obj and annot_obj["/FT"] == "/Btn":  # Check if it's a button (checkbox/radio)
                    field_name = annot_obj.get("/T", "Unnamed Field")
                    field_value = annot_obj.get("/V", "Off")  # Default to "Off" if not checked
                    checkbox_fields[field_name] = field_value

    return checkbox_fields

def fill_pdf_form(input_pdf, output_pdf, field_values):
    # Load the PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Get the form fields
    fields = reader.get_form_text_fields()
    fields["Check Box19"] = "Off"
    fields["Check Box20"] = "Off"
    #print(fields)
    #return

    # Update field values
    for key, value in field_values.items():
        if key in fields:
            fields[key] = value

    # Apply updated form fields
    #print(fields)
    writer.append(reader)
    writer.update_page_form_field_values(writer.pages[0], fields)

    # Save to a new PDF
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    print(f"✅ PDF form filled and saved as: {output_pdf}")

# Example Usage
field_values = {'Name': "Gargantua",
                'Date': "2025-09-18",
                'Project': "Frontier",
                'Contact': "Alberto G",
                'Email': "alberto@gmail.com",
                'How many': "3",
                'Dimensions': "1x1",
                'process time': "56",
                'Handling': "Yes",
                'More information1': "123",
                'More information2': "124",
                'More information3': "125",
                'More information4': "126", 
                'More information5': "127", 
                'More information6': "128",
                'Preferent hardware': "PLC Wago", 
                'PO': "na",
                'Additional comment': None,
                'travel': "no",
                'most important of  the project': "Never and ever",
                'Check Box19': "/Off",
                'Check Box20': "/Off"
            }

PDF_FILE = "/Users/c_angel/Downloads/IAT_System Assessment_Rev03.pdf"
#fields = get_checkbox_fields(PDF_FILE)

fields = get_selectbox_fields(PDF_FILE)
print(fields)

fill_pdf_form(PDF_FILE, "filled_form.pdf", field_values)
