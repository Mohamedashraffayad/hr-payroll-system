#!/usr/bin/env python3
"""
HR & Payroll System - Backend API Server
Complete REST API with SQLite database
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import hashlib
import secrets
import urllib.parse
from datetime import datetime, timedelta
import os

# Database setup
DB_PATH = '/home/claude/hr_payroll.db'

def init_database():
    """Initialize the SQLite database with all tables"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Companies
    c.execute('''CREATE TABLE IF NOT EXISTS companies (
        company_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name_en TEXT NOT NULL,
        company_name_ar TEXT NOT NULL,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Departments
    c.execute('''CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name_en TEXT NOT NULL,
        department_name_ar TEXT NOT NULL,
        company_id INTEGER,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    )''')
    
    # Locations
    c.execute('''CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_name_en TEXT NOT NULL,
        location_name_ar TEXT NOT NULL,
        company_id INTEGER,
        is_active INTEGER DEFAULT 1,
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    )''')
    
    # Job Titles
    c.execute('''CREATE TABLE IF NOT EXISTS job_titles (
        job_title_id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title_en TEXT NOT NULL,
        job_title_ar TEXT NOT NULL,
        job_code TEXT,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Job Grades
    c.execute('''CREATE TABLE IF NOT EXISTS job_grades (
        job_grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
        grade_code TEXT NOT NULL,
        grade_name TEXT,
        min_salary REAL,
        max_salary REAL,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Employees
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_code TEXT UNIQUE NOT NULL,
        name_en TEXT,
        name_ar TEXT NOT NULL,
        national_id TEXT UNIQUE,
        hire_date TEXT NOT NULL,
        termination_date TEXT,
        employment_status TEXT DEFAULT 'active',
        company_id INTEGER,
        department_id INTEGER,
        location_id INTEGER,
        job_title_id INTEGER,
        job_grade_id INTEGER,
        phone TEXT,
        email TEXT,
        bank_name TEXT,
        bank_account TEXT,
        social_insurance_number TEXT,
        social_insurance_salary REAL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (company_id) REFERENCES companies(company_id),
        FOREIGN KEY (department_id) REFERENCES departments(department_id),
        FOREIGN KEY (location_id) REFERENCES locations(location_id),
        FOREIGN KEY (job_title_id) REFERENCES job_titles(job_title_id),
        FOREIGN KEY (job_grade_id) REFERENCES job_grades(job_grade_id)
    )''')
    
    # Employee Salary Components
    c.execute('''CREATE TABLE IF NOT EXISTS employee_salary_components (
        component_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        basic_salary REAL NOT NULL,
        other_allowance REAL DEFAULT 0,
        location_allowance REAL DEFAULT 0,
        transport_housing_food_allowance REAL DEFAULT 0,
        gross_salary REAL NOT NULL,
        effective_from TEXT NOT NULL,
        effective_to TEXT,
        is_current INTEGER DEFAULT 1,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )''')
    
    # Payroll Runs
    c.execute('''CREATE TABLE IF NOT EXISTS payroll_runs (
        payroll_run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_name TEXT NOT NULL,
        company_id INTEGER,
        period_month INTEGER NOT NULL,
        period_year INTEGER NOT NULL,
        period_start_date TEXT NOT NULL,
        period_end_date TEXT NOT NULL,
        working_days INTEGER NOT NULL,
        status TEXT DEFAULT 'draft',
        total_gross REAL,
        total_deductions REAL,
        total_net REAL,
        total_employees INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        approved_at TEXT,
        paid_at TEXT,
        FOREIGN KEY (company_id) REFERENCES companies(company_id)
    )''')
    
    # Payroll Items
    c.execute('''CREATE TABLE IF NOT EXISTS payroll_items (
        payroll_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        payroll_run_id INTEGER,
        employee_id INTEGER,
        basic_salary REAL,
        other_allowance REAL DEFAULT 0,
        location_allowance REAL DEFAULT 0,
        transport_allowance REAL DEFAULT 0,
        gross_salary REAL,
        incentive_amount REAL DEFAULT 0,
        overtime_amount REAL DEFAULT 0,
        total_income REAL,
        social_insurance_employee REAL,
        tax REAL DEFAULT 0,
        absence_deduction REAL DEFAULT 0,
        loans REAL DEFAULT 0,
        medical_insurance_employee REAL DEFAULT 0,
        penalties REAL DEFAULT 0,
        total_deductions REAL,
        net_salary REAL,
        social_insurance_employer REAL,
        working_days INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (payroll_run_id) REFERENCES payroll_runs(payroll_run_id),
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )''')
    
    # Leave Types
    c.execute('''CREATE TABLE IF NOT EXISTS leave_types (
        leave_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
        leave_name_en TEXT NOT NULL,
        leave_name_ar TEXT NOT NULL,
        default_days_per_year INTEGER,
        is_paid INTEGER DEFAULT 1,
        requires_approval INTEGER DEFAULT 1,
        is_active INTEGER DEFAULT 1
    )''')
    
    # Leave Balances
    c.execute('''CREATE TABLE IF NOT EXISTS leave_balances (
        balance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        leave_type_id INTEGER,
        year INTEGER NOT NULL,
        total_days REAL NOT NULL,
        used_days REAL DEFAULT 0,
        remaining_days REAL NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
        FOREIGN KEY (leave_type_id) REFERENCES leave_types(leave_type_id),
        UNIQUE(employee_id, leave_type_id, year)
    )''')
    
    # Leave Requests
    c.execute('''CREATE TABLE IF NOT EXISTS leave_requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        leave_type_id INTEGER,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        days_requested REAL NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        requested_at TEXT DEFAULT CURRENT_TIMESTAMP,
        approved_by INTEGER,
        approved_at TEXT,
        rejection_reason TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
        FOREIGN KEY (leave_type_id) REFERENCES leave_types(leave_type_id)
    )''')
    
    # Attendance
    c.execute('''CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        attendance_date TEXT NOT NULL,
        clock_in TEXT,
        clock_out TEXT,
        total_hours REAL,
        status TEXT,
        late_minutes INTEGER DEFAULT 0,
        early_leave_minutes INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
        UNIQUE(employee_id, attendance_date)
    )''')
    
    # Users
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'employee',
        is_active INTEGER DEFAULT 1,
        last_login TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
    )''')
    
    # Sessions
    c.execute('''CREATE TABLE IF NOT EXISTS sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        token TEXT UNIQUE NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        expires_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def seed_data():
    """Seed initial data from the Excel structure"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if already seeded
    c.execute("SELECT COUNT(*) FROM companies")
    if c.fetchone()[0] > 0:
        print("✅ Database already seeded")
        conn.close()
        return
    
    print("🌱 Seeding database with initial data...")
    
    # Companies
    companies = [
        ('Tiba Landscape for General Contracting', 'طيبة لاند سكيب للمقاولات العامة'),
        ('Al-Saman for Modern Agriculture', 'السمان للزراعة الحديثة'),
        ('Al-Saman for General Contracting', 'السمان للمقاولات العامة'),
        ('Al-Saman for Development', 'السمان للتنمية'),
        ('Al-Saman for Import and Export', 'السمان للاستيراد والتصدير')
    ]
    c.executemany("INSERT INTO companies (company_name_en, company_name_ar) VALUES (?, ?)", companies)
    
    # Departments
    departments = [
        ('Internal Audit', 'المراجعة الداخلية', 1),
        ('Agriculture', 'المحاصيل', 2),
        ('Projects', 'المشروعات', 1),
        ('Administration', 'الإدارة', 1),
        ('Maintenance', 'الصيانة', 1),
        ('Contracting', 'المقاولات', 3),
        ('Development', 'التنمية', 4),
        ('Import/Export', 'الاستيراد والتصدير', 5)
    ]
    c.executemany("INSERT INTO departments (department_name_en, department_name_ar, company_id) VALUES (?, ?, ?)", departments)
    
    # Locations
    locations = [
        ('Head Office', 'المركز الرئيسى', 1),
        ('Airport Farm', 'مزرعة المطار', 2),
        ('Delta Farm', 'مزرعة الدلتا', 2),
        ('Project Site A', 'موقع مشروع أ', 1),
        ('Project Site B', 'موقع مشروع ب', 3),
        ('Project Site C', 'موقع مشروع ج', 1)
    ]
    c.executemany("INSERT INTO locations (location_name_en, location_name_ar, company_id) VALUES (?, ?, ?)", locations)
    
    # Job Grades
    grades = [
        ('D1', 'Director Level 1', 5000, 8000),
        ('D2', 'Director Level 2', 8000, 12000),
        ('D3', 'Director Level 3', 12000, 20000),
        ('M1', 'Manager Level 1', 4000, 7000),
        ('M2', 'Manager Level 2', 7000, 10000),
        ('M3', 'Manager Level 3', 10000, 15000)
    ]
    c.executemany("INSERT INTO job_grades (grade_code, grade_name, min_salary, max_salary) VALUES (?, ?, ?, ?)", grades)
    
    # Job Titles
    titles = [
        ('Internal Auditor', 'مراجع داخلي', 'J1'),
        ('Agricultural Engineer', 'مهندس زراعي', 'J2'),
        ('Project Manager', 'مدير مشروع', 'J3'),
        ('Administrator', 'إداري', 'J4'),
        ('Maintenance Technician', 'فني صيانة', 'J5'),
        ('Contract Manager', 'مدير عقود', 'J6'),
        ('Development Specialist', 'أخصائي تنمية', 'J7'),
        ('Import/Export Coordinator', 'منسق استيراد وتصدير', 'J8')
    ]
    c.executemany("INSERT INTO job_titles (job_title_en, job_title_ar, job_code) VALUES (?, ?, ?)", titles)
    
    # Sample Employees (10 employees based on your Excel)
    employees_data = [
        ('11', 'Ahmed Hassan Ibrahim', 'أحمد حسن إبراهيم', '25302220100074', '2015-11-15', 1, 1, 1, 1, 3, '01012345678', 'ahmed@example.com', 'CIB', '100025470607', '74952464', 8334),
        ('12', 'Taher Mahmoud Ismail', 'طاهر محمود إسماعيل', '28402041805991', '2016-01-01', 2, 2, 2, 2, 1, '01023456789', 'taher@example.com', 'CIB', '100065016448', '74952464', 6500),
        ('13', 'Mohamed Ali Hassan', 'محمد علي حسن', '29012345678901', '2017-03-15', 1, 3, 4, 3, 2, '01034567890', 'mohamed@example.com', 'NBE', '100045678901', '85012345', 7200),
        ('14', 'Sara Ahmed Mohamed', 'سارة أحمد محمد', '29512345678902', '2018-06-01', 5, 8, 1, 8, 1, '01045678901', 'sara@example.com', 'NBE', '100056789012', '86123456', 5500),
        ('15', 'Khaled Ibrahim Saleh', 'خالد إبراهيم صالح', '28712345678903', '2016-09-20', 1, 5, 2, 5, 3, '01056789012', 'khaled@example.com', 'CIB', '100067890123', '87234567', 9100),
        ('16', 'Fatima Nour El-Din', 'فاطمة نور الدين', '29612345678904', '2019-01-10', 2, 2, 3, 2, 2, '01067890123', 'fatima@example.com', 'NBE', '100078901234', '88345678', 6000),
        ('17', 'Omar Hassan Badawi', 'عمر حسن بدوي', '28312345678905', '2017-11-05', 3, 6, 5, 6, 1, '01078901234', 'omar@example.com', 'CIB', '100089012345', '89456789', 7800),
        ('18', 'Nadia Rashad Farouk', 'نادية رشاد فاروق', '29012345678906', '2018-04-12', 4, 7, 1, 7, 3, '01089012345', 'nadia@example.com', 'NBE', '100090123456', '90567890', 11000),
        ('19', 'Youssef Mostafa Kamal', 'يوسف مصطفى كمال', '28812345678907', '2017-07-22', 1, 3, 6, 3, 2, '01090123456', 'youssef@example.com', 'CIB', '100001234567', '91678901', 8600),
        ('20', 'Dina Sherif Abdallah', 'دينا شريف عبدالله', '29412345678908', '2019-02-14', 1, 4, 1, 4, 1, '01001234567', 'dina@example.com', 'NBE', '100012345678', '92789012', 6200)
    ]
    
    for emp in employees_data:
        c.execute("""INSERT INTO employees 
            (employee_code, name_en, name_ar, national_id, hire_date, company_id, department_id, 
             location_id, job_title_id, job_grade_id, phone, email, bank_name, bank_account, 
             social_insurance_number, social_insurance_salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", emp)
        
        emp_id = c.lastrowid
        salary = emp[15]
        
        # Insert salary components
        c.execute("""INSERT INTO employee_salary_components
            (employee_id, basic_salary, other_allowance, location_allowance, 
             transport_housing_food_allowance, gross_salary, effective_from)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (emp_id, salary, 0, 0, 0, salary, '2026-01-01'))
    
    # Leave Types
    leave_types = [
        ('Annual Leave', 'إجازة سنوية', 21, 1, 1),
        ('Sick Leave', 'إجازة مرضية', 15, 1, 1),
        ('Emergency Leave', 'إجازة طارئة', 7, 0, 1),
        ('Maternity Leave', 'إجازة وضع', 90, 1, 1)
    ]
    c.executemany("INSERT INTO leave_types (leave_name_en, leave_name_ar, default_days_per_year, is_paid, requires_approval) VALUES (?, ?, ?, ?, ?)", leave_types)
    
    # Create leave balances for all employees for 2026
    for emp_id in range(1, 11):
        for leave_type_id in range(1, 5):
            c.execute("SELECT default_days_per_year FROM leave_types WHERE leave_type_id = ?", (leave_type_id,))
            total_days = c.fetchone()[0]
            used = 0
            if leave_type_id == 1:  # Annual leave - some used
                used = emp_id % 5 + 3  # Varies between 3-7 days
            elif leave_type_id == 2:  # Sick leave - minimal usage
                used = emp_id % 3  # 0-2 days
            
            c.execute("""INSERT INTO leave_balances 
                (employee_id, leave_type_id, year, total_days, used_days, remaining_days)
                VALUES (?, ?, 2026, ?, ?, ?)""",
                (emp_id, leave_type_id, total_days, used, total_days - used))
    
    # Create some sample leave requests
    leave_requests = [
        (1, 1, '2026-01-20', '2026-01-25', 5, 'Annual vacation', 'pending'),
        (2, 2, '2026-01-22', '2026-01-23', 2, 'Sick', 'approved'),
        (3, 3, '2026-01-21', '2026-01-21', 1, 'Emergency', 'pending'),
        (4, 1, '2026-02-01', '2026-02-05', 5, 'Personal trip', 'pending'),
        (5, 2, '2026-01-19', '2026-01-19', 1, 'Medical checkup', 'approved'),
        (6, 1, '2026-01-28', '2026-02-01', 4, 'Family visit', 'rejected')
    ]
    c.executemany("""INSERT INTO leave_requests 
        (employee_id, leave_type_id, start_date, end_date, days_requested, reason, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", leave_requests)
    
    # Create admin user (password: admin123)
    password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
    c.execute("""INSERT INTO users (employee_id, username, email, password_hash, role)
        VALUES (1, 'admin', 'admin@alsaman.com', ?, 'admin')""", (password_hash,))
    
    conn.commit()
    conn.close()
    print("✅ Database seeded successfully!")
    print("👤 Admin user created - username: admin, password: admin123")

class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def _json_response(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data).encode())
    
    def _error_response(self, message, status=400):
        self._json_response({'error': message}, status)
    
    def do_OPTIONS(self):
        self._set_headers(204)
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        
        try:
            # GET /api/employees - List all employees
            if path == '/api/employees':
                c.execute("""
                    SELECT e.*, c.company_name_en, d.department_name_en, 
                           l.location_name_en, jg.grade_code, s.basic_salary
                    FROM employees e
                    LEFT JOIN companies c ON e.company_id = c.company_id
                    LEFT JOIN departments d ON e.department_id = d.department_id
                    LEFT JOIN locations l ON e.location_id = l.location_id
                    LEFT JOIN job_grades jg ON e.job_grade_id = jg.job_grade_id
                    LEFT JOIN employee_salary_components s ON e.employee_id = s.employee_id AND s.is_current = 1
                    WHERE e.employment_status = 'active'
                    ORDER BY e.employee_code
                """)
                employees = [dict(row) for row in c.fetchall()]
                self._json_response({'employees': employees, 'count': len(employees)})
            
            # GET /api/employees/:id - Get single employee
            elif path.startswith('/api/employees/') and len(path.split('/')) == 4:
                emp_id = path.split('/')[-1]
                c.execute("""
                    SELECT e.*, c.company_name_en, d.department_name_en, 
                           l.location_name_en, jg.grade_code, jt.job_title_en,
                           s.basic_salary, s.other_allowance, s.location_allowance,
                           s.transport_housing_food_allowance, s.gross_salary
                    FROM employees e
                    LEFT JOIN companies c ON e.company_id = c.company_id
                    LEFT JOIN departments d ON e.department_id = d.department_id
                    LEFT JOIN locations l ON e.location_id = l.location_id
                    LEFT JOIN job_grades jg ON e.job_grade_id = jg.job_grade_id
                    LEFT JOIN job_titles jt ON e.job_title_id = jt.job_title_id
                    LEFT JOIN employee_salary_components s ON e.employee_id = s.employee_id AND s.is_current = 1
                    WHERE e.employee_id = ?
                """, (emp_id,))
                employee = c.fetchone()
                if employee:
                    self._json_response({'employee': dict(employee)})
                else:
                    self._error_response('Employee not found', 404)
            
            # GET /api/companies - List all companies
            elif path == '/api/companies':
                c.execute("SELECT * FROM companies WHERE is_active = 1")
                companies = [dict(row) for row in c.fetchall()]
                self._json_response({'companies': companies})
            
            # GET /api/departments - List all departments
            elif path == '/api/departments':
                c.execute("""
                    SELECT d.*, c.company_name_en 
                    FROM departments d
                    LEFT JOIN companies c ON d.company_id = c.company_id
                    WHERE d.is_active = 1
                """)
                departments = [dict(row) for row in c.fetchall()]
                self._json_response({'departments': departments})
            
            # GET /api/payroll/runs - List payroll runs
            elif path == '/api/payroll/runs':
                c.execute("""
                    SELECT pr.*, c.company_name_en
                    FROM payroll_runs pr
                    LEFT JOIN companies c ON pr.company_id = c.company_id
                    ORDER BY pr.period_year DESC, pr.period_month DESC
                """)
                runs = [dict(row) for row in c.fetchall()]
                self._json_response({'payroll_runs': runs})
            
            # GET /api/payroll/:run_id - Get payroll details
            elif path.startswith('/api/payroll/') and len(path.split('/')) == 4:
                run_id = path.split('/')[-1]
                c.execute("SELECT * FROM payroll_runs WHERE payroll_run_id = ?", (run_id,))
                run = c.fetchone()
                if run:
                    c.execute("""
                        SELECT pi.*, e.name_en, e.employee_code, c.company_name_en
                        FROM payroll_items pi
                        JOIN employees e ON pi.employee_id = e.employee_id
                        LEFT JOIN companies c ON e.company_id = c.company_id
                        WHERE pi.payroll_run_id = ?
                    """, (run_id,))
                    items = [dict(row) for row in c.fetchall()]
                    self._json_response({'payroll_run': dict(run), 'items': items})
                else:
                    self._error_response('Payroll run not found', 404)
            
            # GET /api/leave/requests - List leave requests
            elif path == '/api/leave/requests':
                c.execute("""
                    SELECT lr.*, e.name_en, e.employee_code, lt.leave_name_en
                    FROM leave_requests lr
                    JOIN employees e ON lr.employee_id = e.employee_id
                    JOIN leave_types lt ON lr.leave_type_id = lt.leave_type_id
                    ORDER BY lr.requested_at DESC
                """)
                requests = [dict(row) for row in c.fetchall()]
                self._json_response({'leave_requests': requests})
            
            # GET /api/leave/balances/:employee_id - Get employee leave balances
            elif path.startswith('/api/leave/balances/'):
                emp_id = path.split('/')[-1]
                c.execute("""
                    SELECT lb.*, lt.leave_name_en, lt.leave_name_ar
                    FROM leave_balances lb
                    JOIN leave_types lt ON lb.leave_type_id = lt.leave_type_id
                    WHERE lb.employee_id = ? AND lb.year = 2026
                """, (emp_id,))
                balances = [dict(row) for row in c.fetchall()]
                self._json_response({'balances': balances})
            
            # GET /api/stats/dashboard - Dashboard statistics
            elif path == '/api/stats/dashboard':
                # Total active employees
                c.execute("SELECT COUNT(*) as count FROM employees WHERE employment_status = 'active'")
                total_employees = c.fetchone()['count']
                
                # Monthly payroll
                c.execute("""
                    SELECT SUM(pi.net_salary) as total
                    FROM payroll_items pi
                    JOIN payroll_runs pr ON pi.payroll_run_id = pr.payroll_run_id
                    WHERE pr.period_year = 2026 AND pr.period_month = 1
                """)
                monthly_payroll = c.fetchone()['total'] or 0
                
                # On leave today
                today = datetime.now().strftime('%Y-%m-%d')
                c.execute("""
                    SELECT COUNT(*) as count FROM leave_requests
                    WHERE status = 'approved' AND ? BETWEEN start_date AND end_date
                """, (today,))
                on_leave = c.fetchone()['count']
                
                # Pending approvals
                c.execute("SELECT COUNT(*) as count FROM leave_requests WHERE status = 'pending'")
                pending = c.fetchone()['count']
                
                # Company breakdown
                c.execute("""
                    SELECT c.company_name_en, COUNT(e.employee_id) as count
                    FROM companies c
                    LEFT JOIN employees e ON c.company_id = e.company_id AND e.employment_status = 'active'
                    GROUP BY c.company_id
                """)
                company_breakdown = [dict(row) for row in c.fetchall()]
                
                self._json_response({
                    'total_employees': total_employees,
                    'monthly_payroll': round(monthly_payroll, 2),
                    'on_leave_today': on_leave,
                    'pending_approvals': pending,
                    'company_breakdown': company_breakdown
                })
            
            else:
                self._error_response('Endpoint not found', 404)
        
        except Exception as e:
            self._error_response(str(e), 500)
        
        finally:
            conn.close()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        try:
            # POST /api/employees - Create employee
            if self.path == '/api/employees':
                c.execute("""INSERT INTO employees 
                    (employee_code, name_en, name_ar, national_id, hire_date, 
                     company_id, department_id, location_id, job_title_id, job_grade_id,
                     phone, email, bank_name, bank_account)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (data.get('employee_code'), data.get('name_en'), data.get('name_ar'),
                     data.get('national_id'), data.get('hire_date'), data.get('company_id'),
                     data.get('department_id'), data.get('location_id'), data.get('job_title_id'),
                     data.get('job_grade_id'), data.get('phone'), data.get('email'),
                     data.get('bank_name'), data.get('bank_account')))
                
                emp_id = c.lastrowid
                
                # Insert salary components
                c.execute("""INSERT INTO employee_salary_components
                    (employee_id, basic_salary, other_allowance, location_allowance,
                     transport_housing_food_allowance, gross_salary, effective_from)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (emp_id, data.get('basic_salary'), data.get('other_allowance', 0),
                     data.get('location_allowance', 0), data.get('transport_allowance', 0),
                     data.get('basic_salary'), datetime.now().strftime('%Y-%m-%d')))
                
                conn.commit()
                self._json_response({'message': 'Employee created', 'employee_id': emp_id}, 201)
            
            # POST /api/payroll/run - Create payroll run
            elif self.path == '/api/payroll/run':
                # Create payroll run
                c.execute("""INSERT INTO payroll_runs
                    (run_name, company_id, period_month, period_year, period_start_date,
                     period_end_date, working_days, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, 'draft')""",
                    (data.get('run_name'), data.get('company_id'), data.get('period_month'),
                     data.get('period_year'), data.get('period_start_date'),
                     data.get('period_end_date'), data.get('working_days')))
                
                run_id = c.lastrowid
                
                # Calculate payroll for all active employees
                c.execute("""
                    SELECT e.employee_id, s.basic_salary, s.other_allowance, 
                           s.location_allowance, s.transport_housing_food_allowance, s.gross_salary
                    FROM employees e
                    JOIN employee_salary_components s ON e.employee_id = s.employee_id AND s.is_current = 1
                    WHERE e.employment_status = 'active'
                """)
                
                total_gross = 0
                total_net = 0
                total_deductions = 0
                emp_count = 0
                
                for emp in c.fetchall():
                    emp_id, basic, other_allow, loc_allow, trans_allow, gross = emp
                    
                    # Calculate deductions
                    si_employee = round(gross * 0.11, 2)  # 11% employee SI
                    si_employer = round(gross * 0.1875, 2)  # 18.75% employer SI
                    tax = 0  # Simplified - would need full tax calculation
                    
                    total_deductions_emp = si_employee + tax
                    net = gross - total_deductions_emp
                    
                    # Insert payroll item
                    c.execute("""INSERT INTO payroll_items
                        (payroll_run_id, employee_id, basic_salary, other_allowance,
                         location_allowance, transport_allowance, gross_salary,
                         total_income, social_insurance_employee, tax, total_deductions,
                         net_salary, social_insurance_employer, working_days)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (run_id, emp_id, basic, other_allow, loc_allow, trans_allow, gross,
                         gross, si_employee, tax, total_deductions_emp, net, si_employer,
                         data.get('working_days')))
                    
                    total_gross += gross
                    total_net += net
                    total_deductions += total_deductions_emp
                    emp_count += 1
                
                # Update payroll run totals
                c.execute("""UPDATE payroll_runs SET 
                    total_gross = ?, total_deductions = ?, total_net = ?, total_employees = ?
                    WHERE payroll_run_id = ?""",
                    (total_gross, total_deductions, total_net, emp_count, run_id))
                
                conn.commit()
                self._json_response({
                    'message': 'Payroll run created',
                    'payroll_run_id': run_id,
                    'employees_processed': emp_count
                }, 201)
            
            # POST /api/leave/request - Create leave request
            elif self.path == '/api/leave/request':
                c.execute("""INSERT INTO leave_requests
                    (employee_id, leave_type_id, start_date, end_date, days_requested, reason)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (data.get('employee_id'), data.get('leave_type_id'), data.get('start_date'),
                     data.get('end_date'), data.get('days_requested'), data.get('reason')))
                
                conn.commit()
                self._json_response({'message': 'Leave request submitted', 'request_id': c.lastrowid}, 201)
            
            else:
                self._error_response('Endpoint not found', 404)
        
        except Exception as e:
            conn.rollback()
            self._error_response(str(e), 500)
        
        finally:
            conn.close()
    
    def do_PUT(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body) if body else {}
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        try:
            # PUT /api/leave/requests/:id/approve - Approve leave
            if '/approve' in self.path:
                request_id = self.path.split('/')[-2]
                c.execute("""UPDATE leave_requests SET status = 'approved', approved_at = ?
                    WHERE request_id = ?""",
                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request_id))
                conn.commit()
                self._json_response({'message': 'Leave request approved'})
            
            # PUT /api/leave/requests/:id/reject - Reject leave
            elif '/reject' in self.path:
                request_id = self.path.split('/')[-2]
                c.execute("""UPDATE leave_requests SET status = 'rejected', 
                    rejection_reason = ? WHERE request_id = ?""",
                    (data.get('reason', 'Rejected'), request_id))
                conn.commit()
                self._json_response({'message': 'Leave request rejected'})
            
            # PUT /api/payroll/:id/approve - Approve payroll
            elif self.path.endswith('/approve'):
                run_id = self.path.split('/')[-2]
                c.execute("""UPDATE payroll_runs SET status = 'approved', approved_at = ?
                    WHERE payroll_run_id = ?""",
                    (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), run_id))
                conn.commit()
                self._json_response({'message': 'Payroll approved'})
            
            else:
                self._error_response('Endpoint not found', 404)
        
        except Exception as e:
            conn.rollback()
            self._error_response(str(e), 500)
        
        finally:
            conn.close()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def run_server(port=8000):
    """Start the API server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, APIHandler)
    print(f"""
╔════════════════════════════════════════════════════════════╗
║         HR & PAYROLL SYSTEM - API SERVER READY             ║
╚════════════════════════════════════════════════════════════╝

🌐 API Server running on: http://localhost:{port}
📊 Database: {DB_PATH}

Available Endpoints:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Employees:
   GET  /api/employees              - List all employees
   GET  /api/employees/:id          - Get single employee
   POST /api/employees              - Create new employee

💰 Payroll:
   GET  /api/payroll/runs           - List payroll runs
   GET  /api/payroll/:id            - Get payroll details
   POST /api/payroll/run            - Create payroll run
   PUT  /api/payroll/:id/approve    - Approve payroll

📅 Leave:
   GET  /api/leave/requests         - List leave requests
   GET  /api/leave/balances/:id     - Get employee balances
   POST /api/leave/request          - Submit leave request
   PUT  /api/leave/:id/approve      - Approve leave
   PUT  /api/leave/:id/reject       - Reject leave

📊 Stats:
   GET  /api/stats/dashboard        - Dashboard statistics

🏢 Master Data:
   GET  /api/companies              - List companies
   GET  /api/departments            - List departments

Press Ctrl+C to stop the server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == '__main__':
    # Initialize database
    print("🔧 Initializing database...")
    init_database()
    
    # Seed data
    seed_data()
    
    # Start server
    run_server(8000)
