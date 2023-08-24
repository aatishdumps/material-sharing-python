# Educational Material Management System

Welcome to the Educational Material Management System! This application helps educational institutions manage and share learning materials among students and faculty members.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Introduction

The Educational Material Management System is a web application designed to facilitate the organization and distribution of educational resources within a college or university setting. It allows users to upload, access, and search for various learning materials, including documents, presentations, and videos.

## Features

- User registration and authentication.
- Role-based access control (Admin, Faculty, Student).
- Uploading and sharing of materials (PDFs, documents, videos, etc.).
- Material categorization and tagging.
- Messaging system for communication between users.
- Admin panel for managing users, categories, and courses.
- Material search functionality.
- User profile management and password change.

## Technologies Used

- Frontend: HTML, Bootstrap, jQuery
- Backend: Flask (Python)
- Database: MySQL

## Installation

1. Clone the repository: `git clone https://github.com/aatishdumps/material-sharing-python.git`
2. Navigate to the project directory: `cd educational-material-management`
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database by importing the provided SQL dump.
5. Configure database connection in `app.py`.
6. Run the application: `python app.py`
7. Access the application in your web browser: `http://localhost:5000`

## Usage

- Register as a new user or log in with existing credentials.
- Explore the dashboard, browse materials by category and course.
- Upload new learning materials.
- Send and receive messages with other users.
- Admin users can manage users, categories, and courses from the admin panel.

## Contributing

Contributions are welcome! To contribute to this project:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m "Add your message"`
4. Push to your branch: `git push origin feature-name`
5. Create a pull request detailing your changes.
