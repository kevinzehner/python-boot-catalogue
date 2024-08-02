CV Boots Catalogue Application


Overview
This project is a CV Boots Catalogue Application developed using Python and PyQt5. The application is designed to aid a company during an exhibition in Germany. It allows staff to confirm the availability of parts based on specific vehicle data provided by customers. The application uses a series of dropdowns to filter available parts and displays relevant information in an organized manner.

Features
Dropdown Menus: Users can select vehicle manufacturer, model, engine size, mark series, drive type, position, and transmission to filter available parts.
Search Functionality: Based on the selected criteria, the application searches the database for available parts and displays them.
Image Display: Each part is accompanied by an image for easy identification.
Results Layout: Results are displayed in a grid layout, with each part's size and number presented.


Installation
Prerequisites
Python 3.12
PyQt5
SQLite3
Setting Up the Environment
Clone the Repository:

sh
Copy code
git clone https://github.com/kevinzehner/python-boot-catalogue.git
cd python-boot-catalogue
Create a Virtual Environment:

sh
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install Dependencies:

sh
Copy code
pip install -r requirements.txt
Set Up the Database:
Ensure that the boots.db database file is in the root directory of the project.

Create Indexes for Faster Search:

python
Copy code
python -c "from create_indexes import create_indexes; create_indexes('boots.db')"
Running the Application
Run the Application:

sh
Copy code
python main.py
The application window will open, displaying the dropdown menus for selecting the vehicle data.

Usage

Select Vehicle Data: Use the dropdown menus to select the vehicle manufacturer, model, engine size, mark series, drive type, position, and transmission.
Search for Parts: Click the "Search" button to find available parts based on the selected criteria.
View Results: The results will be displayed in a grid layout, showing part numbers, sizes, and images.


Known Issues

Ensure the database file boots.db is present in the root directory of the application.
If the application is slow, verify that the indexes have been created on the database.
We attempted to package the application using PyInstaller but were unable to open the packaged application. This issue is still unresolved.


Contributing

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

If you have any questions or need further assistance, please contact Kevin Zehner.