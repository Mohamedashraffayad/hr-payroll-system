# HR & Payroll Management System 🏢

A complete, bilingual (English/Arabic) HR and Payroll management system designed for multi-company organizations. Built specifically for Al-Saman Group with support for 5+ companies and 500+ employees.

![Demo](https://img.shields.io/badge/Status-Production%20Ready-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Language](https://img.shields.io/badge/Languages-EN%20%7C%20AR-orange)

## 🌐 Live Demo

**[View Live Demo](https://YOUR-USERNAME.github.io/hr-payroll-system/)**

## ✨ Features

### 📊 Dashboard
- Real-time statistics and KPIs
- Company breakdown visualization
- Payroll trend charts
- Quick action buttons

### 👥 Employee Management
- Complete employee database
- Multi-company support (5 companies)
- Department and location tracking
- Job grades and titles
- Bank account details
- Social insurance information

### 💰 Payroll Processing
- Automated salary calculations
- Egyptian social insurance (11% employee + 18.75% employer)
- Tax computation
- Allowances and deductions
- Monthly payroll runs
- Approval workflow

### 📅 Leave & Attendance
- Leave request submission
- Approval/rejection workflow
- Leave balance tracking
- Multiple leave types (Annual, Sick, Emergency, Maternity)
- Attendance records

### 📄 Payslips
- Detailed salary breakdown
- Earnings vs deductions
- Net salary calculation
- PDF generation ready
- Email delivery interface

### 📈 Reports & Analytics
- Dashboard statistics
- Company-wise breakdown
- Payroll cost analysis
- Key HR metrics
- Excel export ready

### 🙋 Employee Self-Service Portal
- Personal dashboard
- Leave balance view
- Payslip access
- Leave request submission

## 🚀 Quick Start

### Option 1: GitHub Pages (Frontend Only - Demo)
Just visit the live demo link above! The frontend will load with sample data.

### Option 2: Full System (Frontend + Backend)

#### Prerequisites
- Python 3.7 or higher
- Modern web browser

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/hr-payroll-system.git
cd hr-payroll-system
```

2. **Start the backend server**
```bash
python3 api/server.py
```

The server will:
- Create the SQLite database automatically
- Seed with sample data
- Start on `http://localhost:8000`

3. **Open the frontend**
- Double-click `index.html`, or
- Use a local server:
```bash
python3 -m http.server 3000
```
Then visit: `http://localhost:3000`

## 📁 Project Structure

```
hr-payroll-system/
├── index.html              # Main frontend application
├── api/
│   ├── server.py          # Backend REST API server
│   └── database.py        # Database models and setup
├── docs/
│   ├── DEPLOYMENT.md      # Deployment guide
│   ├── API.md             # API documentation
│   └── DATABASE.md        # Database schema
├── assets/
│   └── screenshots/       # Application screenshots
├── README.md              # This file
└── LICENSE                # MIT License
```

## 🔌 API Endpoints

### Employees
- `GET /api/employees` - List all employees
- `GET /api/employees/:id` - Get single employee
- `POST /api/employees` - Create employee

### Payroll
- `GET /api/payroll/runs` - List payroll runs
- `POST /api/payroll/run` - Create payroll run
- `PUT /api/payroll/:id/approve` - Approve payroll

### Leave Management
- `GET /api/leave/requests` - List leave requests
- `POST /api/leave/request` - Submit leave request
- `PUT /api/leave/:id/approve` - Approve leave
- `PUT /api/leave/:id/reject` - Reject leave

### Statistics
- `GET /api/stats/dashboard` - Dashboard statistics

[View Full API Documentation](docs/API.md)

## 🗄️ Database Schema

Built with SQLite for simplicity and portability. Includes:
- 20+ normalized tables
- Employee master data
- Salary components
- Payroll runs and items
- Leave types and balances
- Attendance records
- User authentication

[View Full Database Schema](docs/DATABASE.md)

## 🌍 Bilingual Support

Switch seamlessly between:
- 🇬🇧 **English** - Full interface translation
- 🇸🇦 **Arabic** - RTL layout with Arabic text

Click the 🌐 button in the header to toggle languages.

## 🎨 Technology Stack

### Frontend
- Pure HTML5/CSS3/JavaScript (no frameworks!)
- Responsive design (mobile, tablet, desktop)
- Modern ES6+ JavaScript
- No build process required

### Backend
- Python 3 (standard library only)
- SQLite database
- RESTful API design
- Zero external dependencies for core functionality

## 📊 Sample Data

The system comes pre-loaded with:
- ✅ 10 sample employees
- ✅ 5 companies (Al-Saman Group entities)
- ✅ 8 departments
- ✅ 6 locations
- ✅ Multiple job grades and titles
- ✅ Leave balances for 2026
- ✅ Sample leave requests

## 🔐 Security Features

- Password hashing (SHA-256)
- Session management
- SQL injection prevention (parameterized queries)
- CORS configuration
- Input validation

**Note:** For production deployment, implement:
- JWT authentication
- HTTPS/SSL
- Rate limiting
- Enhanced password hashing (bcrypt)
- Audit logging

## 📱 Browser Support

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## 🚢 Deployment Options

### 1. GitHub Pages (Frontend Only)
Perfect for demos and prototypes. See [Deployment Guide](docs/DEPLOYMENT.md).

### 2. Shared Hosting
Upload both frontend and backend to any PHP/Python hosting.

### 3. Cloud Platforms
- **Heroku** - Easy deployment, free tier available
- **AWS EC2** - Scalable, professional
- **DigitalOcean** - Simple VPS, $5/month
- **Azure App Service** - Enterprise-grade

### 4. Docker Container
```bash
docker build -t hr-payroll-system .
docker run -p 8000:8000 hr-payroll-system
```

## 📚 Documentation

- [Deployment Guide](docs/DEPLOYMENT.md) - Complete deployment instructions
- [API Documentation](docs/API.md) - All API endpoints explained
- [Database Schema](docs/DATABASE.md) - Full database structure
- [User Guide](docs/USER_GUIDE.md) - How to use the system

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created for **Al-Saman Group** companies:
- Tiba Landscape for General Contracting
- Al-Saman for Modern Agriculture
- Al-Saman for General Contracting
- Al-Saman for Development
- Al-Saman for Import and Export

## 🙏 Acknowledgments

- Built with ❤️ for modern HR management
- Designed for Egyptian payroll regulations
- Inspired by real-world HR challenges

## 📧 Support

For questions or support, please:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the [FAQ](docs/FAQ.md)

## 🗺️ Roadmap

### Phase 1 (Current) ✅
- [x] Core HR management
- [x] Payroll processing
- [x] Leave management
- [x] Bilingual interface

### Phase 2 (Planned)
- [ ] Document management
- [ ] Email notifications
- [ ] Advanced reporting
- [ ] Mobile app

### Phase 3 (Future)
- [ ] Performance reviews
- [ ] Recruitment module
- [ ] Training management
- [ ] Asset tracking

---

⭐ **Star this repo if you find it useful!**

📢 **Share with your HR team!**

🚀 **Deploy and simplify your HR operations today!**
