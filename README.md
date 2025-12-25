# 🚗 CarMind - Vehicle Management System

CarMind is a comprehensive vehicle management and maintenance tracking system built with Python and Tkinter. It provides role-based access for administrators, technicians, and vehicle owners to manage vehicles, track maintenance records, monitor faults, and generate insightful reports.

## ✨ Features

### 👤 User Roles

- **Admin Panel**: Complete system management and user oversight
- **Technician Panel**: Maintenance tracking and fault diagnosis
- **User Panel**: Personal vehicle management and service history

### 🔑 Core Functionalities

- **User Authentication**: Secure login and registration system
- **Vehicle Management**: Add, view, and manage vehicle information
- **Maintenance Tracking**: Record and monitor service history
- **Fault Diagnosis**: Track fault codes and vehicle issues
- **Report Generation**: Comprehensive analytics and insights
  - Most frequent fault codes
  - Vehicles requiring oil changes
  - Maintenance statistics
  - Service history analysis

## 🛠️ Technology Stack

- **Language**: Python 3.x
- **GUI Framework**: Tkinter
- **Database**: MySQL
- **Database Connector**: mysql-connector-python

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- MySQL Server
- pip (Python package manager)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ozgunsaz/CarMind.git
   cd CarMind
   ```

2. **Install required packages**
   ```bash
   pip install mysql-connector-python
   ```

3. **Set up the database**
   - Create a MySQL database named `carmind_db`
   - Import the database schema from `carmind.sql` (if available)
   - Update database credentials in `db_connection.py`:
     ```python
     host="localhost"
     user="your_username"
     password="your_password"
     database="carmind_db"
     ```

4. **Test database connection**
   ```bash
   python test_connection.py
   ```

## 🎯 Usage

1. **Run the application**
   ```bash
   python login.py
   ```

2. **Login or Register**
   - Use existing credentials or create a new account
   - Default roles: user, technician, admin

3. **Navigate the interface**
   - Each role has specific functionalities tailored to their needs
   - Follow the intuitive GUI to manage vehicles and maintenance

## 📁 Project Structure

```
CarMind/
├── login.py                 # Main entry point with authentication
├── admin_panel.py          # Administrator interface
├── technician_panel.py     # Technician interface
├── user_panel.py           # User interface
├── report_panel.py         # Reports and analytics
├── db_connection.py        # Database connection handler
├── test_connection.py      # Database connection tester
├── carmind.sql            # Database schema
└── README.md              # Project documentation
```

## 🎨 Interface

The application features a modern, user-friendly interface with:
- Custom color scheme (Orange theme)
- Responsive design
- Scrollable content areas
- Interactive tables and forms
- Styled buttons and entry fields

## 🔒 Security Notes

⚠️ **Important**: Before deploying to production:
- Remove hardcoded database credentials from `db_connection.py`
- Use environment variables for sensitive information
- Implement password hashing (currently using plain text)
- Add input validation and SQL injection prevention
- Use parameterized queries (already implemented)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

**Özgün Saz**
- GitHub: [@ozgunsaz](https://github.com/ozgunsaz)

## 📞 Support

For support, please open an issue in the GitHub repository.

## 🗺️ Future Enhancements

- [ ] Password encryption
- [ ] Email notifications for maintenance reminders
- [ ] Export reports to PDF/Excel
- [ ] Multi-language support
- [ ] Mobile responsive web version
- [ ] Advanced analytics and dashboards
- [ ] Integration with vehicle diagnostic APIs

---

**Status**: Demo version completed, ready for updates and improvements.

*Last updated: December 25, 2025*
