# 📖 Study Tracker with GUI (WIP)

## 📝 Description
Study Tracker is an application designed to help you monitor the time spent on different subjects or projects, with features to enhance productivity and organization.

## 🔑 Key Features

### ⏳ Study Timer (Pomodoro)
- ▶️ Start, ⏸️ pause, and 🔄 reset study sessions.
- ⏱️ Customize session duration (e.g., 25-minute focus, 5-minute break).
- 🔔 Receive notifications at the end of each session.

### 📊 Session Logging
- 🗂️ Automatically save time spent on each subject or project.
- 📅 View a detailed history with date, duration, and category.

### 📈 Progress Charts
- 📊 Display weekly/monthly charts showing time dedicated to each subject.
- 🛠️ Use libraries like Matplotlib or Plotly for visualizations.

### 📚 Subject/Project Management
- ➕ Add, ✏️ edit, and ❌ delete subjects or categories.
- 🔗 Associate study sessions with specific subjects.

### 📝 Quick Notes
- 🗒️ Add notes related to study sessions directly in the app.

### ⚙️ Customizable Settings
- 🎨 Choose themes (🌞 light/🌙 dark mode).
- ⏲️ Enable reminders for regular breaks (e.g., 👀 20/20/20 eye rest technique).

## 🛠️ Technologies

- **🖥️ GUI**: Tkinter (simple and built-in Python).
- **🗄️ Database**: PocketBase for storing sessions, subjects, and notes.
- **📊 Charts**: Matplotlib or Plotly for data visualization.
- **🔔 Notifications**: Plyer library for system alerts.

## 📁 Project Structure
The project follows a modular structure to ensure best practices:

```
📂 study-tracker
│── 🏁 main.py        # Initializes the application
│── ⏳ timer.py       # Manages the Pomodoro timer
│── 🗄️ database.py    # Handles SQLite database operations
│── 🎨 gui.py         # Sets up the graphical user interface
│── 📊 charts.py      # Generates charts with Matplotlib or Plotly
```


## 🤝 Contributing
Contributions are welcome! Feel free to submit issues and pull requests.

## 📜 License
This project is licensed under the MIT License.
