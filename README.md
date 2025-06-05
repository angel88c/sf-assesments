# iBtest Assessment Application

A Streamlit-based application for managing test assessments for iBtest. The application allows users to submit assessment forms for different types of tests: In Circuit Test (ICT), Functional Test (FCT), and Industrial Automation Test (IAT).

## Project Structure

```
sf-assessments/
├── .env                      # Environment variables
├── .streamlit/               # Streamlit configuration
├── env/                      # Python virtual environment
├── logo_ibtest.png           # iBtest logo
├── main.py                   # Main application entry point
├── pages/                    # Application pages
│   ├── ict_assessment.py     # ICT assessment page
│   ├── iat_assessment.py     # IAT assessment page
│   ├── fct_assessment.py     # FCT assessment page
│   ├── fix_assessment.py     # FIX assessment page
│   └── utils/                # Utility modules
│       ├── base_assessment.py # Base assessment class
│       ├── constants.py       # Constants and configuration
│       ├── dates_info.py      # Date utilities
│       ├── fct_create_html.py # FCT HTML report generator
│       ├── fix_create_html.py # FIX HTML report generator
│       ├── global_styles.py   # Global CSS styles
│       ├── iat_create_html.py # IAT HTML report generator
│       ├── ict_create_html.py # ICT HTML report generator
│       ├── salesforce_access.py # Salesforce integration
│       ├── test_account_names.py # Account name utilities
│       └── validations.py     # Form validation utilities
└── requirements.txt          # Python dependencies
```

## Features

- **Multiple Assessment Types**: Support for ICT, FCT, and IAT assessments
- **Form Validation**: Comprehensive validation of form inputs
- **File Upload**: Support for uploading various file types
- **Salesforce Integration**: Automatic creation of opportunities in Salesforce
- **HTML Reports**: Generation of HTML reports for each assessment
- **Responsive UI**: Modern and user-friendly interface

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/sf-assessments.git
   cd sf-assessments
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:
   ```
   SALESFORCE_USERNAME=your_username
   SALESFORCE_PASSWORD=your_password
   SALESFORCE_SECURITY_TOKEN=your_security_token
   SALESFORCE_CONSUMER_KEY=your_consumer_key
   SALESFORCE_CONSUMER_SECRET=your_consumer_secret
   TOKEN_URL=https://login.salesforce.com/services/oauth2/token
   PATH_FILE=/path/to/your/files
   PATH_TO_SHAREPOINT=/path/to/sharepoint
   TEMPLATE_ICT=/path/to/ict/template
   TEMPLATE_FCT=/path/to/fct/template
   TEMPLATE_IAT=/path/to/iat/template
   TEMPLATE_FIX=/path/to/fix/template
   ```

## Usage

1. Start the application:

   ```
   streamlit run main.py
   ```

2. Navigate to the desired assessment type:

   - ICT Assessment: `/pages/ict_assessment.py`
   - FCT Assessment: `/pages/fct_assessment.py`
   - IAT Assessment: `/pages/iat_assessment.py`
   - FIX Assessment: `/pages/fix_assessment.py`

3. Fill out the assessment form and submit.

## Development

### Code Structure

The application follows a modular design with the following components:

- **Base Assessment Class**: Provides common functionality for all assessment types
- **Assessment Pages**: Implement specific form fields and processing for each assessment type
- **Utility Modules**: Provide reusable functionality across the application

### Adding a New Assessment Type

To add a new assessment type:

1. Create a new assessment page in the `pages` directory
2. Create a new HTML report generator in the `pages/utils` directory
3. Add any new constants to `pages/utils/constants.py`
4. Update the main application to include the new assessment type

## License

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

## Contact

For questions or support, please contact the iBtest team.
