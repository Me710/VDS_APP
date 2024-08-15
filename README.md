# VDS_APP

**VDS_APP** is a Flask-based web application developed for the **Vie Des Saints (VDS)** project, which aims to spread Christian Catholic teachings and inspirations through the digital space. The application serves as a comprehensive platform for evangelization, allowing users to engage with spiritual content, participate in events, subscribe to newsletters, and volunteer for various activities. It also includes a back-office interface for administrators to manage content efficiently.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

VDS_APP is the digital face of the Vie Des Saints evangelization group, designed to be a one-stop platform for users to explore a variety of religious content. It provides tools for publishing and managing articles, hosting events, and engaging with the community. The application is built using the Flask framework and follows a modular structure for easy scalability and maintenance.

## Features

- **User Authentication:** Secure login, registration, and password management.
- **Content Management:** Create, edit, and publish articles, newsletters, and other spiritual content.
- **Event Management:** Organize and manage events, allowing users to view and participate.
- **Newsletter Subscription:** Users can subscribe to receive regular updates and spiritual insights.
- **Volunteer Management:** Engage users to participate in volunteer activities and community services.
- **Admin Interface:** A back-office interface for administrators to manage all aspects of the platform.

## Project Structure

The project follows a modular structure to separate different functionalities and maintain clean, manageable code:

```
VDS_APP/
│
├── apps/
│   ├── authentication/      # Handles user authentication and session management
│   ├── events/              # Manages events, including creation and listing
│   ├── home/                # Contains views and logic for the homepage
│   ├── publications/        # Manages articles, newsletters, and other publications
│   ├── services/            # Handles various services offered by VDS
│   ├── static/              # Static files (CSS, JS, images)
│   ├── templates/           # HTML templates for front-end and back-office
│   │   ├── back/            # Back-office interface templates
│   │   └── front/           # User-facing interface templates
│   └── users/               # User profile management
│
├── __init__.py              # Initializes the Flask app
├── config.py                # Configuration settings for the app
├── db.sqlite3               # SQLite database file
├── replicate_utils.py       # Utility functions for data replication
├── env/                     # Environment-specific configurations
├── media/                   # User-uploaded media files
├── migrations/              # Database migration scripts
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── README.md                # Project documentation
└── vercel.json              # Vercel deployment configuration
```

## Setup and Installation

### Prerequisites

- **Python 3.8+**
- **pip** (Python package installer)
- **virtualenv** (Recommended for creating a virtual environment)

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Me710/VDS_APP.git
   cd VDS_APP
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

# (Optional) [START]

5. **Set up environment variables:**
   Create a `.env` file in the root directory and add your environment-specific settings. Example:
   ```plaintext
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key
   DATABASE_URL=sqlite:///db.sqlite3
   ```

6. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## Configuration

All configuration settings are stored in `config.py` and the `.env` file. Modify these files to set up your database connections, secret keys, and other environment-specific settings.

## Database Migrations

To manage database changes, Flask-Migrate is used. To create and apply migrations:

1. **Create a migration:**
   ```bash
   flask db migrate -m "Description of the migration"
   ```

2. **Apply the migration:**
   ```bash
   flask db upgrade
   ```
# (Optional) [END]

## Running the Application

To run the application locally:

1. Ensure your virtual environment is activated.
2. Run the Flask development server:
   ```bash
   flask run
   ```
3. Access the application in your browser at `http://127.0.0.1:5000`.

## Deployment

The application can be deployed using Vercel or any other hosting service. Vercel configuration is handled in `vercel.json`. Make sure to adjust the environment variables and other deployment-specific settings.

## Contributing

We welcome contributions !

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

Please ensure your code follows the project’s coding standards and includes relevant tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---