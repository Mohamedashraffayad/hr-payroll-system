# HR & Payroll System - Software Architecture

## 1. System Overview

**Type:** Web-based Application (Progressive Web App)  
**Users:** 500 employees  
**Deployment:** Cloud-hosted (AWS/Azure/GCP)

---

## 2. Architecture Style

**Three-Tier Architecture** with microservices approach for scalability:

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  (React/Vue.js Frontend - Responsive Web App)               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│         (API Gateway + Backend Services)                     │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐      │
│  │   Employee   │  │   Payroll    │  │   Leave &   │      │
│  │  Management  │  │  Processing  │  │ Attendance  │      │
│  └──────────────┘  └──────────────┘  └─────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐      │
│  │  Reporting   │  │ Notification │  │     Auth    │      │
│  │   Service    │  │   Service    │  │   Service   │      │
│  └──────────────┘  └──────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐      │
│  │  PostgreSQL  │  │  File Store  │  │    Redis    │      │
│  │   Database   │  │   (S3/Blob)  │  │   (Cache)   │      │
│  └──────────────┘  └──────────────┘  └─────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack Recommendation

### Frontend
- **Framework:** React.js with TypeScript
- **UI Library:** Material-UI or Ant Design
- **State Management:** Redux Toolkit or Zustand
- **API Communication:** Axios
- **Charts/Reports:** Chart.js or Recharts

### Backend
- **Framework:** Node.js with Express OR Python with FastAPI
- **API Style:** RESTful API
- **Authentication:** JWT tokens + OAuth 2.0
- **Validation:** Joi or Zod

### Database
- **Primary DB:** PostgreSQL (relational data)
- **Cache:** Redis (session management, performance)
- **File Storage:** AWS S3 / Azure Blob (documents, payslips)

### Infrastructure
- **Hosting:** AWS (EC2/ECS) or Azure App Service
- **CDN:** CloudFlare
- **Monitoring:** DataDog or New Relic
- **CI/CD:** GitHub Actions or GitLab CI

---

## 4. Core Modules & Database Schema

### 4.1 Employee Management Module

**Features:**
- Employee profile management
- Department/role assignment
- Document storage (ID, contracts, certificates)
- Employment history tracking

**Database Tables:**
```
employees
├── employee_id (PK)
├── first_name
├── last_name
├── email
├── phone
├── date_of_birth
├── hire_date
├── department_id (FK)
├── position_id (FK)
├── salary
├── employment_status (active/inactive)
├── bank_account_info
└── created_at, updated_at

departments
├── department_id (PK)
├── department_name
└── manager_id (FK)

positions
├── position_id (PK)
├── position_title
└── department_id (FK)

employee_documents
├── document_id (PK)
├── employee_id (FK)
├── document_type
├── file_url
└── uploaded_at
```

---

### 4.2 Payroll Processing Module

**Features:**
- Salary calculation (basic + allowances - deductions)
- Tax calculation
- Payroll run management
- Payment history
- Bulk payroll processing

**Database Tables:**
```
payroll_runs
├── payroll_run_id (PK)
├── run_date
├── period_start
├── period_end
├── status (draft/processed/approved/paid)
└── created_by (FK)

payroll_items
├── payroll_item_id (PK)
├── payroll_run_id (FK)
├── employee_id (FK)
├── basic_salary
├── allowances (JSON or separate table)
├── deductions (JSON or separate table)
├── tax_amount
├── net_salary
└── payment_date

salary_components
├── component_id (PK)
├── employee_id (FK)
├── component_type (allowance/deduction)
├── component_name
├── amount
├── is_recurring
└── effective_from
```

---

### 4.3 Leave & Attendance Module

**Features:**
- Leave request & approval workflow
- Leave balance tracking
- Attendance logging (clock in/out)
- Absence management
- Holiday calendar

**Database Tables:**
```
leave_types
├── leave_type_id (PK)
├── leave_name (Annual, Sick, etc.)
├── default_days
└── requires_approval

leave_balances
├── balance_id (PK)
├── employee_id (FK)
├── leave_type_id (FK)
├── year
├── total_days
├── used_days
└── remaining_days

leave_requests
├── request_id (PK)
├── employee_id (FK)
├── leave_type_id (FK)
├── start_date
├── end_date
├── days_requested
├── reason
├── status (pending/approved/rejected)
├── approved_by (FK)
└── created_at

attendance
├── attendance_id (PK)
├── employee_id (FK)
├── date
├── clock_in
├── clock_out
├── total_hours
└── status (present/absent/half-day)
```

---

### 4.4 Payslip Generation Module

**Features:**
- Automated payslip generation
- PDF generation
- Email delivery
- Payslip history & download

**Database Tables:**
```
payslips
├── payslip_id (PK)
├── employee_id (FK)
├── payroll_run_id (FK)
├── file_url
├── generated_at
└── sent_at
```

---

### 4.5 Reporting Module

**Features:**
- Payroll summary reports
- Headcount reports
- Leave utilization reports
- Cost analysis
- Export to Excel/PDF

**Key Reports:**
- Monthly payroll summary
- Department-wise cost breakdown
- Employee turnover rate
- Leave balance report
- Attendance statistics

---

### 4.6 Employee Self-Service Portal

**Features:**
- View personal information
- Download payslips
- Request leave
- View leave balance
- Update bank details
- Clock in/out (if needed)
- View attendance history

---

## 5. User Roles & Permissions

| Role | Permissions |
|------|------------|
| **Admin** | Full system access, user management, system configuration |
| **HR Manager** | Employee management, payroll processing, reports, approve leaves |
| **Department Manager** | View team data, approve leaves for team members |
| **Employee** | Self-service portal access only |
| **Payroll Specialist** | Payroll processing, payslip generation |

---

## 6. Security Features

- **Authentication:** Multi-factor authentication (MFA)
- **Authorization:** Role-based access control (RBAC)
- **Data Encryption:** 
  - At rest: AES-256
  - In transit: TLS 1.3
- **Audit Logging:** Track all sensitive operations
- **Password Policy:** Strong password requirements
- **Session Management:** Automatic timeout after inactivity
- **Backup:** Daily automated backups with 30-day retention

---

## 7. Integration Points

**Current (Phase 1):**
- Email service (SendGrid/AWS SES) for notifications
- Payment gateway (for future salary disbursement)

**Future (Phase 2):**
- Accounting software integration (QuickBooks, Xero)
- Biometric attendance devices
- Government tax reporting APIs
- Background check services

---

## 8. Development Phases

### Phase 1 (MVP - 3-4 months)
- User authentication & authorization
- Employee management
- Basic payroll processing
- Leave management
- Payslip generation
- Basic reports

### Phase 2 (4-6 months)
- Advanced reporting & analytics
- Attendance tracking with clock in/out
- Performance review module
- Mobile app (optional)
- Document management system

### Phase 3 (6+ months)
- Recruitment module
- Training & development tracking
- Asset management
- Advanced workflow automation
- AI-powered insights

---

## 9. Data Migration Strategy - YOUR EXCEL FILE

### 9.1 Current Excel Structure Analysis

Your Excel file has **16 sheets** with the main payroll calculation in "Dec. .2025 payroll calc." (716 employees):

**Key Sheets:**
1. **Dec. .2025 payroll calc.** - Main payroll data (127 columns!)
2. **مواقع ومزارع** - Locations/Farms summary
3. **Payslip** - Payslip template
4. **Cash & Bank** - Payment details
5. **Leavers** - Terminated employees
6. **payroll reconciliation** - Monthly reconciliation
7. **Approval Payroll sheets** - Approval records
8. **Company-specific sheets** - Per company summaries

### 9.2 Main Payroll Sheet Mapping

Your main sheet has these key columns (I've identified them):

**Employee Info:**
- Column B: Employee Code (c)
- Column C: Name
- Column D: Hire Date
- Column E: Sector
- Column F: Location
- Column G: Job Title
- Column H: Company
- Column I: Department
- Column J: Job Grade

**Salary Components:**
- Column M: Basic Salary (Actual Gross)
- Column N: Other Allowance
- Column O: Location Allowance
- Column P: Transport/Housing/Food Allowance
- Column Q: Total Gross Salary
- Column U-AC: Incentives, Overtime, Settlement
- Column AE: Minimum Wage Difference

**Deductions:**
- Columns AI-BF: Various deductions (Performance, Absence, Penalties, Loans, etc.)
- Column BS: Social Insurance (Employee Share)
- Column BT: Tax
- Column BU: Total Deductions

**Net Salary:**
- Column BV/BW: Net Salary

**Tax & Insurance:**
- Columns CC-CG: Tax calculations
- Columns CJ-CM: Salary components for insurance
- Column CP-CW: Insurance details

**Bank Details:**
- Column DA: Bank Account
- Column DB: Account Holder Name
- Column DC: National ID
- Column DD: Net Salary (duplicate)

### 9.3 Migration Steps

**Phase 1: Extract Master Data**
```
1. Extract unique values for lookup tables:
   - Companies (Column H)
   - Departments (Column I)
   - Locations (Column F)
   - Job Titles (Column G)
   - Job Grades (Column J)
   - Sectors (Column E)

2. Create employee master records:
   - Employee ID (Column B)
   - Name (Column C)
   - Hire Date (Column D)
   - National ID (Column DC)
   - Bank Account (Column DA)
   - Current position & department
```

**Phase 2: Historical Payroll Data**
```
1. Import payroll runs from "Dec. .2025 payroll calc."
2. Import historical data from "payroll reconciliation" sheet
3. Link to employees via Employee ID (Column B)
```

**Phase 3: Active Employees Setup**
```
For each active employee, create:
- Salary structure (basic + allowances)
- Leave balances (extract from current tracking)
- Bank details
- Insurance details
```

**Phase 4: Clean & Validate**
```
1. Remove duplicate employee records
2. Validate all formulas convert to stored calculations
3. Cross-check totals with Excel
4. Handle Arabic text encoding properly
```

### 9.4 Migration Script Structure

```python
# Pseudo-code for migration
import pandas as pd
import openpyxl

# Load Excel
wb = openpyxl.load_workbook('payroll___HR_System.xlsx')
main_sheet = wb['Dec. .2025 payroll calc.']

# Extract companies
companies = extract_unique(main_sheet, column='H')
# Insert into database: INSERT INTO companies...

# Extract employees
for row in main_sheet.iter_rows(min_row=3):
    employee = {
        'employee_id': row[1].value,  # Column B
        'name': row[2].value,          # Column C
        'hire_date': row[3].value,     # Column D
        'department': row[8].value,    # Column I
        'basic_salary': row[12].value, # Column M
        # ... etc
    }
    # Insert into database: INSERT INTO employees...

# Extract payroll data for Dec 2025
for row in main_sheet.iter_rows(min_row=3):
    payroll = {
        'employee_id': row[1].value,
        'gross_salary': row[16].value,   # Column Q
        'deductions': row[73].value,      # Column BU
        'net_salary': row[74].value,      # Column BV
        # ... etc
    }
    # Insert: INSERT INTO payroll_items...
```

### 9.5 Key Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| **127 columns** - too many! | Group related columns into JSON fields or normalize into separate tables |
| **Arabic text** | Use UTF-8 encoding, test thoroughly |
| **Complex formulas** | Convert to stored procedures/calculations in backend |
| **Multiple companies** | Add company_id to all tables for multi-tenancy |
| **Historical data** | Import last 12 months of payroll runs for reporting |

---

## 10. Estimated Costs (Annual)

| Component | Estimated Cost (USD) |
|-----------|---------------------|
| Cloud Hosting (AWS/Azure) | $3,000 - $6,000 |
| Database | $1,200 - $2,400 |
| File Storage | $600 - $1,200 |
| Email Service | $300 - $600 |
| SSL Certificate | $100 - $300 |
| Monitoring Tools | $600 - $1,200 |
| **Total Infrastructure** | **$5,800 - $11,700** |

**Development Costs:** $30,000 - $80,000 (depending on team/agency)

---

## 11. Next Steps

1. **Unlock Excel file** so I can analyze your current data structure
2. **Finalize technology stack** based on your team's expertise
3. **Create detailed wireframes** for key screens
4. **Set up development environment**
5. **Start with database design** based on your actual data
6. **Build MVP in phases**

---

## Questions to Consider:

1. Do you have an in-house development team or will you outsource?
2. What's your preferred cloud provider (AWS/Azure/GCP)?
3. Any specific compliance requirements (GDPR, local labor laws)?
4. Do you need mobile apps or is responsive web sufficient?
5. What's your timeline and budget?
