# from enum import Enum

# class YesNo(Enum):
#     Yes = "Yes",
#     No = "No"

# class FixtureType(Enum):
#     Offline = "OffLine",
#     InLine = "InLine"

# class Options(Enum):
#     NA = "NA",
#     Required = "Required",
#     Optional = "Optional"

# class ActivationTypes(Enum):
#     VacuumBox = "Vacuum Box",
#     HoldDownGates = "Hold Down Gates",
#     Pneumatic = "Pneumatic",
#     InlineTestFixture = "Inline Test Fixture"

# class WellTypes(Enum):
#     SingleWell = "Single Well",
#     DualWell = "Dual Well",
#     DualStage = "Dual Stage"

# class SizeTypes(Enum):
#     SmallKit = "Small Kit",
#     LargeKit = "Large Kit",
#     SmallExtended = "Small Extended",
#     LargeExtended = "Large Extended"

#TEMPLATE_ICT = "/Users/c_angel/Downloads/TEMPLATE_ICT"
#TEMPLATE_FCT = "/Users/c_angel/Downloads/TEMPLATE_FCT"
#TEMPLATE_IAT = "/Users/c_angel/Downloads/TEMPLATE_IAT"

ICT_PROJECTS_FOLDER = "1_In_Circuit Test (ICT)"
FCT_PROJECTS_FOLDER = "2_Functional Test (FCT)"
IAT_PROJECTS_FOLDER = "4_Industrial Automation (IAT)"

CUSTOMER_INFO   = "1_Customer_Info"
ALL_INFO_SHARED = "7_ALL_Info_Shared"

#PATH_FILE = "/Users/c_angel/Library/CloudStorage/OneDrive-Bibliotecascompartidas:InnovativeBoardTestSAPIdeCV/admin - iBtest Assesment/"
#PATH_FILE = "C:/Users/MyUser/OneDrive - Innovative Board Test SAPI de CV/iBtest Assesment"
#PATH_FILE_Q = "/Users/c_angel/OneDrive - Innovative Board Test SAPI de CV/01_2025"

YES_NO = ['Yes', 'No']

FIXTURE_TYPES = ['OffLine', 'InLine']

REQ_OPTIONS = ['NA', 'Required', 'Optional']

ACTIVATION_TYPES = ['Vacuum box',
                    'Hold down gates',
                    'Pneumatic',
                    'Inline Test Fixture']

WELL_TYPES = ['Single well',
              'Dual well',
              'Dual stage']

SIZE_TYPES = ['Small Kit',
              'Large Kit',
              'Small Extended',
              'Large Extended']

OPTIONS = ['Logistic data will be flashed?',
           'It has the config file and codeword data of the 3070?',
           'Do you have Test Spec?',
           'Do you have Fixture SOW?',
           'Panel Test? Specify Qty boards on the panel',
           'Individual test? Specify Nest Qty']

COUNTRIES_DICT = {'Mexico': 'MX',
                  'USA': 'US',
                  'Canada': "CAD",
                  'Europe': 'EUR', 
                  'Asia': 'ASIA', 
                  'Other': 'OTHER'
            }

# IAT
IAT_MILESTONES = ['Drawings (2D, 3D) .step files, .cad?',
                  'Process Step?',
                  'Nest?',
                  'PLC, HMI, Robot programming standards (Templates)?',
                  'SOW and Ergonomic Specification?',
                  'Layout?',
                  'Product Manufacturing Sheet?',
                  'Traceability?',
                  'Estimated process cycle time?',
                  'Is any special handling og the unit needed?',
                  'Do you have samples?']

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