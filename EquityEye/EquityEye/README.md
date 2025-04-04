
# Equity Eye
Note: This version does not contain large files with stock price data due to moodle's file size submission limit.

Equity Eye is a web-based investment simulation platform designed to help users—especially beginners—learn about stock trading in a risk-free environment. The project consists of a Vue.js frontend and a Django backend, connected to a MySQL database.

## ⚙️ Prerequisites

Before running the project, make sure the following are installed on your computer:

- Node.js and npm
- Vue.js CLI
- Python 3.x
- Django
- MySQL

## 🚀 Getting Started

### 1. Frontend Setup

1. Open the project folder `EquityEye-Frontend` in your preferred IDE.
2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run serve
   ```

   The frontend will run on `http://localhost:8080` by default.

### 2. Backend Setup

1. Navigate to your Django project folder in the terminal.
2. Run the development server:

   ```bash
   python manage.py runserver
   ```

   The backend will run on `http://127.0.0.1:8000`.

## 🗄️ Database

Make sure your MySQL server is running and that the database is properly configured in your Django settings (`settings.py`). You may need to:

- Create a database (e.g., `equity_eye`)
- Apply migrations:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

## ✅ You're ready!

Visit `http://localhost:8080` to access Equity Eye in your browser. You can now explore features like:

- Simulated stock buying/selling
- Personalized AI recommendations
- Real-time data visualization

Enjoy learning and investing without the risk!
