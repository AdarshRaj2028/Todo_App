# 📝 Todo App - Multi-Interface Task Manager

A comprehensive todo application built in Python featuring three different user interfaces that share synchronized data in real-time. This is my first Python project after learning the fundamentals, showcasing clean code architecture and cross-platform compatibility.

## 🏗️ Project Structure

Todo_App/
├── cli.py # Command line interface
├── gui.py # Desktop GUI application
├── app_web.py # Web interface
├── functions.py # Shared core functions
├── requirements.txt # Project dependencies
└── README.md # Project documentation

## 🌟 Features

### Core Functionality
- ✅ **Add Tasks** – Create new todo items with automatic date tracking  
- ✏️ **Edit Tasks** – Modify existing todos with validation  
- 🗑️ **Remove Tasks** – Delete unwanted items  
- ✔️ **Complete Tasks** – Mark tasks as done and move to completed list  
- 🧹 **Clear Completed** – Remove all completed tasks  
- 📊 **View Tasks** – Display active and completed todos  

### Advanced Features
- 🔄 **Real-time Sync** – All three interfaces share the same data instantly  
- 💾 **Persistent Storage** – Data saved in user's home directory (`~/.todo_app`)  
- 📅 **Date Tracking** – Automatic timestamp when tasks are created  
- 🎨 **Theme Support** – Dark/Light themes in GUI version  
- ⚡ **Input Validation** – Comprehensive error handling and user feedback  
- 🖥️ **Cross-platform** – Works on Windows, macOS, and Linux  

### Data Storage
- **Location:** `~/.todo_app/` (hidden folder in user's home directory)  
- **Files:**  
  - `todo_list.txt` – Active todos  
  - `completed_todo_list.txt` – Completed tasks  
- **Format:** UTF-8 encoded text files  
- **Sync:** Real-time synchronization across all interfaces  

### Core Functions
- `load_todos()` – Load tasks from file  
- `save_todos()` – Save tasks to file  
- `add()` – Add new todo with validation  
- `remove()` – Remove todo by index  
- `edit()` – Edit existing todo  
- `complete()` – Mark todo as completed  
- `show()` – Display todos and completed tasks 

## 🚀 Three Ways to Use

### 1. 💻 Command Line Interface (CLI)

- Interactive terminal-based interface  
- Keyboard shortcuts and quick commands  
- Perfect for developers and power users  

### 2. 🖼️ Desktop GUI Application

- Modern graphical interface using FreeSimpleGUI  
- Theme switching (Dark/Light mode)  
- Mouse-friendly with intuitive buttons  

### 3. 🌐 Web Application

- Browser-based interface using Streamlit  
- Responsive design  
- Accessible from any device with a web browser  

## 🧠 Skills Demonstrated

### Technical Skills Acquired
- **Python Fundamentals**: Variables, functions, loops, file I/O
- **GUI Development**: Desktop applications with FreeSimpleGUI
- **Web Development**: Browser apps using Streamlit
- **Data Synchronization**: Real-time data sharing across interfaces
- **Error Handling**: Comprehensive exception management
- **Cross-Platform Development**: Windows, macOS, Linux compatibility

### Industry-Relevant Practices
- **Modular Architecture**: Reusable functions and clean code structure
- **User Experience Design**: Multiple interfaces for different user types
- **Data Persistence**: Reliable file-based storage system
- **Input Validation**: Comprehensive error checking
- **Documentation**: Professional README and inline comments

## 📋 Installation

### Prerequisites
- Python 3.7 or higher  
- pip (Python package installer)  

### Dependencies


### Quick Start

1. **Clone the repository** 

-> git clone https://github.com/AdarshRaj2028/Todo_App.git
-> cd Todo_App

2. **Install dependencies** 

-> pip install -r requirements.txt

3. **Choose your preferred interface**  

--> CLI Version

-> python cli.py

--> GUI Version

-> python gui.py

--> Web Version

-> streamlit run app_web.py

## 🤝 Contributing

This is my first Python project, and I'm open to suggestions and improvements!

### Areas for Enhancement
- Database integration (SQLite/PostgreSQL)  
- Task categories and tags  
- Due dates and reminders  
- Export/import functionality  
- Task priority levels  
- Search and filter capabilities  

### How to Contribute
1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)  
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)  
4. Push to the branch (`git push origin feature/AmazingFeature`)  
5. Open a Pull Request  

## 📝 Development Notes

### AI Assistance
- **Approximately 25% AI assistance** used for code optimization and bug fixes  
- **75% original implementation** demonstrating genuine understanding of Python concepts  
- AI primarily helped with error handling improvements and code structure optimization  

### Learning Approach
- **Hands-on Practice:** Built from scratch to understand core concepts  
- **Iterative Development:** Started with CLI, then added GUI and Web interfaces  
- **Problem-Solving:** Tackled real-world challenges like data synchronization  
- **Best Practices:** Focused on clean, maintainable, and well-documented code

## 👨‍💻 Author

**Adarsh Raj**  
- GitHub: [@AdarshRaj2028](https://github.com/AdarshRaj2028)  
- Project: [Todo_App](https://github.com/AdarshRaj2028/Todo_App)  

⭐ **If you found this project helpful, please consider giving it a star!** ⭐

