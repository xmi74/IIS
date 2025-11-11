# Animal Shelter Information System

This is a simple information system for managing abandoned animals in a shelter, with features for volunteers to borrow them for walks.

This project was created as part of the Information Systems (IIS) course at the Brno University of Technology.

## Features

The system supports several user roles with different permissions:

#### Administrator
*   Manages all users in the system.
*   Creates accounts for caretakers and veterinarians.

#### Caretaker
*   Manages animals and their records (history, health status).
*   Creates schedules for walks.
*   Verifies volunteers.
*   Approves animal walk reservations, and logs check-outs and check-ins.
*   Creates requests for the veterinarian.

#### Veterinarian 
*   Handles requests from caretakers (schedules examinations).
*   Maintains and updates the animals' health records.

#### Volunteer 
*   Reserves animals for walks according to the schedule.
*   Can see their history of walks.

#### Unregistered User 
*   Browses information about the shelter and the animals available for adoption or walks.

## Application Showcase

https://github.com/user-attachments/assets/681d6669-1b12-4413-9067-c0214b96a1c2


## Tech Stack
*   **Back End:** Flask (Python)
*   **Front End:** HTML, Bootstrap
*   **Database:** MySQL

## File Structure & Authors

```
.
├── api/                  # API endpoints
├── doc_data/             # Data for documentation
├── forms/                # Forms
├── img/                  # Images for README and documentation
├── models/               # Database models
├── static/               # Static files
│   └── img/
├── templates/            # HTML templates
├── utils/                # Utility functions
├── __init__.py           # Package initialization
├── .gcloudignore         # Configuration for Google Cloud
├── .gitignore            # Configuration for Git
├── app.py                # Main Flask application file
├── app.yaml              # Configuration for App Engine
├── create_db.py          # Script to create the database
├── doc.html              # Documentation
├── README.md             # This file
├── requirements.txt      # List of Python dependencies
├── routes.py             # Application route definitions
└── seed.py               # Script to seed the database with initial data
```

### Authors
*   Igor Mikula
*   Aurel Strigáč
*   Daniel Putis

## Getting Started

#### Step 1: Clone the repository
```bash
git clone https://github.com/xmi74/IIS.git
cd IIS
```

#### Step 2: Create a virtual environment
```bash
python3 -m venv venv
```

#### Step 3: Activate the virtual environment (Linux/macOS)
```bash
source venv/bin/activate
```

#### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Create the database instance
Run the script and enter your MySQL credentials.
```bash
python3 create_db.py
Enter your MySQL username: <your_username>
Enter your MySQL password: <your_password>
```

#### Step 6: Run the project
Start the application and re-enter your MySQL credentials.
```bash
python3 app.py
Enter your MySQL username: <your_username>
Enter your MySQL password: <your_password>
```

## License
MIT License

