
# Flask User Management Application (educational practical task)

This is a simple Flask-based web application for managing users. The application allows you to create, edit, view, and delete users. It also demonstrates the use of cookies to temporarily store user data during a session.

## Features

- **User Management**: Create, view, edit, and delete users.
- **Persistent Storage**: User data is stored in a JSON file.
- **Cookie-based Temporary Storage**: Users are temporarily stored in cookies during a session.
- **Responsive Design**: The UI is styled with a modern, pastel-themed design.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/flask-user-management.git
   cd flask-user-management
   ```

2. **Install dependencies**:
   Make sure you have Python 3.7+ installed. Then, run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python example.py
   ```

4. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- **Home Page**: A simple welcome page with links to user management features.
- **User List**: View the list of all users, search users by nickname or email, and access options to edit or delete a user.
- **Create User**: Add a new user to the list.
- **Edit User**: Update the details of an existing user.
- **Delete User**: Remove a user from the list.

## How It Works

### Persistent Storage

User data is stored in a JSON file located in the `data` directory. This ensures that user data persists even after the server is restarted.

### Cookie-based Temporary Storage

During a session, user data is temporarily stored in cookies. This is primarily for demonstration purposes and shows how to work with cookies in Flask. Cookies are cleared when the session ends.

## Directory Structure

```
/flask-user-management
├── templates
│   ├── users
│   │   ├── layout.html
│   │   ├── users.html
│   │   ├── new.html
│   │   ├── edit.html
│   │   ├── show.html
│   │   ├── 404.html
├── css
│   ├── styles.css
├── data
│   ├── users.json
├── example.py
├── user_repository.py
├── cookie_user_repository.py
├── validate.py
├── utils.py
├── requirements.txt
└── README.md
```

## Future Improvements

- **Session Management**: Implement session-based storage for better management of user data during a session.
- **Authentication**: Add user authentication and authorization features.
- **Database Integration**: Move from JSON file storage to a database like SQLite or PostgreSQL.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
