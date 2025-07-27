# Automated Resume-to-Portfolio Converter

## Project Description
This project is an automated tool designed to convert resumes into professional portfolio websites. It leverages AI to enhance the content and presentation, providing users with a seamless way to showcase their skills and experience.

## Features
- **Resume Upload**: Easily upload your resume in various formats.
- **AI Enhancement**: AI-powered suggestions and improvements for your portfolio content.
- **Professional Portfolio Generation**: Automatically generates a clean, modern, and responsive portfolio website.
- **User Authentication**: Secure login and registration system.
- **Dashboard**: Personalized dashboard for managing portfolios.
- **Animated Backgrounds**: Dynamic and interactive background animations using `particles.js`.
- **Scroll Animations**: Smooth scroll animations for an enhanced user experience using AOS (Animate On Scroll).

## Installation
To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Automated-Resume-to-Portfolio-Converter.git
   cd Automated-Resume-to-Portfolio-Converter
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize the database**:
   ```bash
   python migrate_db.py
   ```
   or if you need to migrate portfolio data:
   ```bash
   python migrate_portfolio.py
   ```

6. **Run the application**:
   ```bash
   set FLASK_APP=app.py
   flask run
   ```
   Alternatively, you can run:
   ```bash
   python app.py
   ```

   The application should now be running on `http://127.0.0.1:5000/`.

## Usage
1. **Register/Login**: Create an account or log in to access the dashboard.
2. **Upload Resume**: Navigate to the upload section to submit your resume.
3. **Generate Portfolio**: The system will process your resume and generate a portfolio.
4. **Customize (Future Feature)**: Edit and customize your portfolio from the dashboard.
5. **Share**: Share your professional portfolio with potential employers.

## Project Structure
```
Automated Resume-to-Portfolio Converter/
├── .vercel/                 # Vercel deployment configuration
├── __pycache__/             # Python cache files
├── ai_service.py            # AI-related services
├── app.py                   # Main Flask application file
├── instance/                # Instance folder for database and other instance-specific files
├── migrate_db.py            # Database migration script
├── migrate_portfolio.py     # Portfolio data migration script
├── requirements.txt         # Python dependencies
├── schema.sql               # Database schema definition
├── static/                  # Static assets (CSS, JS, Images)
│   ├── css/                 # CSS stylesheets
│   ├── images/              # Image assets
│   └── js/                  # JavaScript files
├── templates/               # HTML templates
│   ├── 404.html             # Custom 404 error page
│   ├── 500.html             # Custom 500 error page
│   ├── about.html           # About page
│   ├── base.html            # Base template for common elements
│   ├── dashboard.html       # User dashboard
│   ├── faq.html             # FAQ page
│   ├── index.html           # Home page
│   ├── login.html           # Login page
│   ├── portfolio.html       # Portfolio display page
│   ├── register.html        # Registration page
│   └── uploads.html         # Upload page
├── test_flask.py            # Flask unit tests
├── test_imports.py          # Import tests
└── uploads/                 # Directory for uploaded files
```

## License
This project is licensed under the MIT License - see the <mcfile name="LICENSE" path="f:\Automated Resume-to-Portfolio Converter\LICENSE"></mcfile> file for details.