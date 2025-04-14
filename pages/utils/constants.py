
YES_NO = ['Yes', 'No']

REQ_OPTIONS = ['NA', 'Required', 'Optional']

ACTIVATION_TYPES = {'Vacuum box': "OffLine",
                    'Hold down gates': "OffLine",
                    'Pneumatic': "OffLine",
                    'InLine Test Fixture': "InLine",
                  }
WELL_TYPES = ['Single well',
              'Dual well',
              'Dual stage']

SIZE_TYPES = ['Small Kit',
              'Large Kit',
              'Small Extended',
              'Large Extended']

OPTIONS = ['(*) Will logistic data be flashed?',
           "What kind of info will be stored?",
           '(*) Do you have the config file and codeword data of the 3070?',
           '(*) Do you have Test Spec?',
           '(*) Do you have Fixture SOW?',
           '(*) Panel Test? Specify qty boards on the panel',
           '(*) Individual Test? Specify Nest qty']

COUNTRIES_DICT = {'Mexico': 'MX',
                  'USA': 'USA',
                  'Canada': "CAD",
                  'Europe': 'EUR', 
                  'Asia': 'ASIA', 
                  'Other': 'OTHER'
            }

# IAT
IAT_MILESTONES = [r'*Drawings (2D, 3D) .step files, .cad?',
                  r'*Process Spec?',
                  r'Nest?',
                  r'*PLC, HMI, Robot programming standards (Templates)?',
                  r'*SOW and Ergonomic Specification?',
                  r'Layout?',
                  r'Product Manufacturing Sheet?',
                  r'Traceability?',
                  r'Estimated process cycle time?',
                  r'Is any special handling on the unit needed?',
                  r'Do you have samples?']

IAT_STATION_TYPES = ['Select',
                     'Other',
                     'Refurbish',
                     'Engineering Service',
                     'Equipment Modification',
                     'Cell',
                     'Stand Alone',
                     'Add New Model']

IAT_PROCESS_TYPES = ['Select',
                     'Other',
                     'Testing',
                     'AOI',
                     'Assembly',
                     'Screwing Station',
                     'Dispensing Machine']

IAT_UNIT_HANDLE_MODES = ['Select',
                         'Other',
                         'Magazine',
                         'Human',
                         'Robot or Cobot',
                         'Axis System',
                         'Conveyor',
                         'Automatic',
                         'Manual']

IAT_DEVICES_UNDER_PROCESS = ['Select',
                             'Housing',
                             'PCB',
                             'Other']


FCT_HARDWARE_OPTIONS = ["Select Option", "NI", "Keysight", "BK", "Chroma", "GW"]
FCT_SYSTEM_TYPES = ["Select Option", "Flexicore", "Venturi", "Viper", "SLU", "ECUTS", "iBFlash", "None"]
FCT_PROCESS_TYPES = ["Offline", "Inline", "Rotaty", "Automated Process"]
FCT_PRODUCT_FINISH = ["Select Option", "PCB", "Assembly"]
FCT_TEST_STRATEGIES =  ["Select Option", "Panel", "Depanelized"]
FCT_FIXTURE_VENDORS = ["Select Option", "iBtest", "CCI", "Rematek", "JT", "Arcadia", "Joule", "Other"]
FCT_CONNECTION_INTERFACES = ["Select Option", "MACPANEL", "INGUN", "VPC", "Harting", "iBtest suggestion", "Other"]
FCT_STATION_TYPES = ["Select Option", "EOL", "Flash", "FVT", "HIPOT", "Vision", "Communication", "Chamber", "Other"]
FCT_STUDIES_OPTIONS = ["FEA", "SGA", "MSA", "GRR", "R&R", "Targeting", "Clearance"]

INVALID_EMAILS =  ["@gmail.com",
                   "@hotmail.com",
                   "@live.com.mx",
                   "@yahoo.com.mx",
                   "@yahoo.com"]