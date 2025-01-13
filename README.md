# Property Portfolio Forecaster & ROI Calculator

## Overview

The Property Portfolio Forecaster & ROI Calculator is a Python-based application designed to help users estimate property valuations and calculate return on investment (ROI) for renovations. The application leverages a MySQL database to store property details, renovation features, and associated costs, enabling users to make informed decisions about property investments and renovations.

**This tool allows users to:**

- Add new or existing properties and forecast their valuation after renovations.
- Track renovation costs and their impact on ROI.
- Amend existing renovation cost records for accurate forecasting and ROI calculations.

## Features

- **Property Evaluation and ROI Forecasting:**
  - Submit details of new or existing properties.
  - Add renovation features and receive a forecast of the updated property valuation.
  - Calculate ROI statistics based on added features and associated costs.

- **Renovations Tracker:**
  - Log renovation quotes and forecasts for properties.
  - Amend feature costs to reflect updated quotes or budgets, with recalculated ROI statistics.

- **User-Friendly API:**
  - Access the application programmatically through endpoints for various functionalities.

## Project Files

**Core Files**

- Property_Portfolio_Forecaster_app.py: Flask application to serve the API.
- Property_Portfolio_Forecaster_main.py: Client-side script to interact with the API.
- Property_Portfolio_&_Forecaster.sql: SQL script to set up the database, tables, and triggers.
- Db_utils.py: Utility script for database connection.
- Config.py: Configuration file containing MySQL connection details.

**Additional Folders & Content**
- API Call Snippets: Screenshots of API results.
- Error Handling Screenshots: Demonstrates error-handling procedures and messages.
- Output Extracts: Text file extracts of terminal output for sample program usage.
- SQL Snippets: Screenshots of MySQL tables and data at the time of submission.
- Testing Folder: Includes basic test files for function and API testing.
- Testing Snippet: Screenshot of successful test runs.

## System Requirements
- MySQL Workbench: Version 8.0 or higher.
- Python: Version 3.12.5 (64-bit).
- VSCode: Version 1.94.2 or higher.
- Required Python Libraries:
  - mysql.connector==9.0.0
  - flask==3.0.3
  - requests==2.32.3

## API Requirements

- Configure Config.py with MySQL user details.
- Ensure the Property_Portfolio_Forecaster_app.py script is running to access the API.

## Available API Endpoints

- Home Page: http://127.0.0.1:5001/
- Retrieve All Properties: http://127.0.0.1:5001/all_properties
- Retrieve Properties with Renovations: http://127.0.0.1:5001/all_properties_after_renovations
- Retrieve Properties by Bedroom Count: http://127.0.0.1:5001/properties_by_bedroom_nr/<bedroom_count> (e.g., <bedroom_count>=2).
- Retrieve Renovation Features: http://127.0.0.1:5001/renovation_features
- Retrieve Renovation Tracker by Property ID: http://127.0.0.1:5001/renovations_tracker/<property_id> (e.g., <property_id>=2).
- Refer to the API Call Snippets folder for examples of API responses.

## Getting Started

### Setup Instructions
- Download Project Files: Store all files in the same directory to maintain module accessibility.

**Database Setup:**
- Start MySQL.
- Open Property_Portfolio_&_Forecaster.sql in MySQL Workbench.
- Run the script to create the database and tables.

**Configure MySQL Connection:**
- Open Config.py.
- Enter your MySQL login details (username, password, etc.).

**Start Flask App:**
- Open a terminal and run:
```
python Property_Portfolio_Forecaster_app.py
```
- Ensure the server is active. You should see a confirmation message in the terminal.

### Running the Client Program
- Open Property_Portfolio_Forecaster_main.py in VSCode.
- Run the script to access the interactive interface.
- Follow the prompts to input property details, add renovation features, and view forecasts.

## User Journey & Results

### Forecasting a Property

- Choose to forecast a new or existing property.
- Input property details (e.g., postcode, purchase amount, bedrooms).
- Add renovation features and their associated costs.
- View property valuation and ROI statistics, including:
  - Added value due to inflation.
  - Added value from renovations.
  - Net added value accounting for renovation costs.
- Optionally save the details in the database.

### Amending Renovation Costs

- Select a property and renovation record to amend.
- Input the updated cost.
- View updated ROI statistics and a refreshed list of renovation records.
- Continue amending other properties or records as needed.

## Output Examples

- Forecast Results: Displays property valuation and ROI statistics.
- Amend Results: Shows updated renovation costs and recalculated ROI.

## Testing

Two test scripts are included in the Testing Folder.
Screenshots of successful test runs are available in the Testing Snippet folder.

## Future Enhancements

- **Advanced Inflation Impact:** Currently the code assumes a flat inflation percentage from the first year onwards. To enhance this, a more comprehensive calculation can be coded into SQL, possibly utilising real figures scraped from the web.
- **Web Interface:** Build a user-friendly web application for broader accessibility.
- **Advanced ROI Calculations:** Incorporate more complex algorithms for ROI forecasting.
- **Data Visualization:** Add graphical representations of ROI statistics and property trends.
- **Enhanced Error Handling:** Improve error messages and handling for edge cases.

## License

This project is open-source and available under the MIT License.

## Contact

For questions, feedback, or collaboration opportunities, please contact:

GitHub: CodeHerUniverse
