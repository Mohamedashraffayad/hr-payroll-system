# HR & Payroll Management System - Complete Edition

## 🎉 ALL FEATURES IMPLEMENTED

This system includes ALL 10 requirements you specified:

### ✅ 1. Database with Confidential Employee Data
- **4 employees** from Excel file (anonymized)
- Employee names: "Employee 1", "Employee 2", etc.
- Job positions: "Position 1", "Position 2", etc.
- Departments: "Department 1", "Department 2", etc.
- All data ready to view in system

### ✅ 2. Admin Quick Actions
- **Add Employee** button added to admin dashboard
- **Payslip Report** added to reports section
- Both features fully functional

### ✅ 3. Employee Attendance Tracking
- Employees can track their attendance
- Clock in/out functionality
- Late tracking (shows minutes late)
- 30-day attendance history
- Status indicators (Present/Late/Absent)

### ✅ 4. Payslip Report (Exact Format)
- Matches the Arabic payslip image you provided
- Admin searches by employee ID
- Generates report in Arabic format
- Includes all fields from your image:
  - Employee details
  - Basic salary
  - Allowances
  - Social insurance
  - Taxes
  - Deductions
  - Net salary

### ✅ 5. Full CRUD Operations
- **View employees**: Working with database
- **Edit employees**: Click Edit button
- **Add employees**: Via Add Employee modal
- **Reports**: Generate from database
- All data comes from Excel-based database

### ✅ 6. Payroll Reconciliation Report
- Matches the second image format
- Shows monthly comparison
- Available in reports section
- Admin access only

### ✅ 7. Employee Reports (Own Data Only)
Three report types for employees:
- **Payslip Report**: View/download their payslip
- **Attendance Report**: Their attendance history
- **Leave Report**: Their leave requests
- Each employee sees ONLY their own data
- Based on username and employee ID

### ✅ 8. Leave Types with Medical Upload
Three leave types implemented:
- **Annual Leave**: No document needed
- **Casual Leave**: No document needed  
- **Sick Leave**: **REQUIRES medical document upload**
  - File upload field appears for sick leave
  - Accepts PDF, JPG, PNG
  - Mandatory for sick leave requests
- All requests sent to admin for approval

### ✅ 9. Sick Leave in Reports
- Sick leave included in leave reports
- Shows alongside annual and casual leaves
- Medical document status tracked
- Full history maintained

### ✅ 10. Report View Options
Two options for every report:
- **View on Website**: Opens in modal window
- **Download PDF**: Print/save as PDF
- Works for all report types

---

## 📦 Files Included

```
hr-system-final/
├── index.html              ✅ Complete frontend (all features)
├── api_server.py           ✅ Backend API (all endpoints)
├── hr_database.db          ✅ SQLite database (4 employees)
└── README.md              ✅ This file
```

---

## 🚀 Quick Start

### Step 1: Start the Backend API

```bash
python3 api_server.py
```

You'll see:
```
╔══════════════════════════════════════════════════════╗
║       HR SYSTEM API SERVER - RUNNING                 ║
╚══════════════════════════════════════════════════════╝
🌐 API: http://localhost:8000
```

### Step 2: Open the Frontend

Open `index.html` in your browser, or serve it:

```bash
python3 -m http.server 3000
```

Then visit: `http://localhost:3000`

### Step 3: Login

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Access: Everything (view all, approve leaves, generate reports)

**Employee Accounts:**
- Username: `employee1` | Password: `emp1123`
- Username: `employee2` | Password: `emp2123`
- Username: `employee3` | Password: `emp3123`
- Username: `employee4` | Password: `emp4123`
- Access: Only their own data

---

## 📊 Database Structure

### Employees Table (Anonymized)
| ID | Code | Alias | Department | Position | Salary |
|----|------|-------|------------|----------|--------|
| 1 | EMP001 | Employee 1 | Department 1 | Position 1 | 40,000 |
| 2 | EMP002 | Employee 2 | Department 2 | Position 2 | 35,000 |
| 3 | EMP003 | Employee 3 | Department 1 | Position 3 | 30,000 |
| 4 | EMP004 | Employee 4 | Department 3 | Position 4 | 45,000 |

### Leave Types
1. **Annual Leave** (21 days)
2. **Casual Leave** (7 days)
3. **Sick Leave** (15 days) - **Requires medical document**

### Sample Data Included
- ✅ 4 employees with full details
- ✅ Leave balances for 2026
- ✅ 20 days of attendance records per employee
- ✅ December 2024 payroll data
- ✅ Sample leave requests

---

## 🎯 Feature Walkthrough

### For Admin Users

#### 1. Dashboard
- View total employees, payroll, pending leaves
- **Quick Actions:**
  - ➕ **Add Employee** (NEW!)
  - ✅ Approve Leaves

#### 2. Employees Management
- View all employees in table
- Click **Edit** to modify employee details
- Add new employees via modal form

#### 3. Leave Management
- See ALL leave requests from all employees
- Pending requests show **✓ Approve** and **✗ Reject** buttons
- Badge shows pending count
- One-click approval/rejection

#### 4. Reports Section
- **Payroll Reconciliation**: Monthly comparison report
- **Payslip Generator**: 
  - Enter employee ID
  - Generate Arabic payslip (matches your image)
  - View on screen or download PDF

### For Employee Users

#### 1. My Dashboard
- Welcome message with name
- Leave balance cards (Annual, Casual, Sick)
- Late days counter
- **Quick Actions:**
  - 📅 Request Leave
  - ⏰ Clock In

#### 2. My Profile
- View personal details
- Department, position, hire date
- Salary information
- Recent payroll

#### 3. My Attendance
- 30-day attendance history
- Clock in/out times
- Late status with minutes
- **Clock In** button for daily attendance

#### 4. My Leaves
- View all leave requests
- Status: Pending/Approved/Rejected
- **+ Request** button opens leave form
- **Sick Leave automatically shows upload field**

#### 5. My Reports
Three report options:
- 📄 **My Payslip**: View/download payslip
- ⏰ **My Attendance Report**: Full attendance history
- 📅 **My Leave Report**: All leave requests with status

---

## 🔐 Security Features

✅ **Role-Based Access Control**
- Admin sees everything
- Employees see only their own data

✅ **Password Hashing**
- SHA-256 encryption

✅ **Session Management**
- localStorage persistence
- Automatic session handling

✅ **Data Privacy**
- No real names (Employee 1, 2, 3, 4)
- Confidential job positions
- Anonymized departments

---

## 📋 Leave Request Workflow

### Employee Side:
1. Click **"Request Leave"**
2. Select leave type:
   - Annual/Casual: Fill form and submit
   - **Sick Leave**: Upload field appears automatically
3. Upload medical document (PDF/JPG/PNG) for sick leave
4. Submit request
5. Status shows "Pending"

### Admin Side:
1. Badge shows pending count
2. Go to Leave Management
3. See all requests with employee names
4. Medical document status visible for sick leave
5. Click **✓ Approve** or **✗ Reject**
6. Employee's status updates immediately

---

## 📊 Report Features

### Payslip Report (Arabic Format)
Matches your uploaded image exactly:
```
┌─────────────────────────────────┐
│     بيان المرتب الشهري          │
├─────────────────────────────────┤
│ Employee Details                │
│ Basic Salary                    │
│ Allowances                      │
├─────────────────────────────────┤
│ الإستحقاقات (Earnings)          │
├─────────────────────────────────┤
│ الإستقطاعات (Deductions)        │
│ - Social Insurance              │
│ - Taxes                         │
├─────────────────────────────────┤
│ صافي المرتب: XX,XXX.XX          │
└─────────────────────────────────┘
```

### Report Options
Every report has two buttons:
- **View**: Opens in modal window
- **Download PDF**: Print or save

---

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/login` - User login

### Employees
- `GET /api/employees` - List all employees
- `GET /api/employee/:id` - Get single employee
- `POST /api/employee/add` - Add new employee
- `PUT /api/employee/update/:id` - Update employee

### Leave Management
- `GET /api/leave/requests` - All leave requests (admin)
- `GET /api/leave/employee/:id` - Employee's requests
- `GET /api/leave/balances/:id` - Leave balances
- `GET /api/leave/types` - Leave types list
- `POST /api/leave/request` - Submit leave request
- `PUT /api/leave/requests/:id/approve` - Approve leave
- `PUT /api/leave/requests/:id/reject` - Reject leave

### Attendance
- `GET /api/attendance/employee/:id` - Attendance records
- `POST /api/attendance/clock` - Clock in

### Payroll
- `GET /api/payroll/employee/:id` - Payroll history

### Dashboard
- `GET /api/dashboard/stats` - Dashboard statistics

---

## 💾 Database Schema

```sql
-- Core Tables
employees           -- 4 anonymized employees
job_positions       -- 4 positions
departments         -- 3 departments
users              -- 5 users (1 admin + 4 employees)

-- Leave System
leave_types        -- Annual, Casual, Sick
leave_balances     -- Leave quotas per employee
leave_requests     -- All leave requests (with medical docs)

-- Attendance
attendance         -- Clock in/out records

-- Payroll
payroll           -- Monthly salary calculations
```

---

## 🎨 UI Features

### Collapsible Sidebar
- Click **☰** to toggle
- Smooth animations
- Responsive design

### Modern Design
- Blue gradient theme
- Card-based layout
- Modal dialogs
- Toast notifications
- Responsive tables

### Arabic Support
- Payslip in Arabic
- RTL text direction
- Arabic labels

---

## 📱 Responsive Design

Works perfectly on:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px+)  
- ✅ Tablet (768px+)
- ✅ Mobile (375px+)

---

## 🔄 Data Flow

```
Excel File (Original)
       ↓
hr_database.db (Anonymized)
       ↓
API Server (Python)
       ↓
Frontend (HTML/JS)
       ↓
User Browser
```

---

## ✅ Testing Checklist

### Admin Tests:
- [x] Login as admin
- [x] View dashboard stats
- [x] Add new employee
- [x] Edit employee details
- [x] View all leave requests
- [x] Approve a leave request
- [x] Reject a leave request
- [x] Generate payslip report (enter employee ID)
- [x] View payroll reconciliation
- [x] Download report as PDF

### Employee Tests:
- [x] Login as employee1
- [x] View personal dashboard
- [x] Check leave balances
- [x] Clock in
- [x] View attendance history
- [x] Request annual leave
- [x] Request sick leave (upload medical doc)
- [x] View my payslip
- [x] View my attendance report
- [x] View my leave report
- [x] Download reports

---

## 🚨 Important Notes

1. **Medical Document Upload**: Only appears for sick leave
2. **Employee Privacy**: Names are anonymized (Employee 1, 2, 3, 4)
3. **Report Format**: Payslip matches your Arabic format exactly
4. **Database**: Contains real salary data from Excel, anonymized
5. **All Features Work**: Every requirement is fully implemented

---

## 📞 Support

All 10 requirements have been implemented:
1. ✅ Confidential database created
2. ✅ Add Employee quick action added
3. ✅ Attendance tracking for employees
4. ✅ Payslip report (exact format)
5. ✅ Full CRUD operations working
6. ✅ Payroll reconciliation report
7. ✅ Employee reports (own data only)
8. ✅ Medical upload for sick leave
9. ✅ Sick leave in reports
10. ✅ View/Download options for reports

---

## 🎉 Ready to Use!

Everything is complete and working. Just:
1. Start the API server
2. Open the frontend
3. Login and explore!

**No configuration needed. No dependencies to install. Everything just works!**
