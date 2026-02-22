# Database Schema - Detailed Design for Your System

## Overview
This schema is designed specifically for your multi-company payroll system with 500+ employees across multiple locations and companies.

---

## 1. MASTER DATA TABLES

### 1.1 Companies
```sql
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    company_name_en VARCHAR(200),
    company_name_ar VARCHAR(200),
    legal_name VARCHAR(200),
    tax_id VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Your companies from Excel:
-- 1. طيبة لاند سكيب للمقاولات العامة
-- 2. السمان للزراعة الحديثة
-- 3. السمان للاستيراد والتصدير
-- 4. السمان للمقاولات العامة
-- 5. السمان للتنمية
```

### 1.2 Departments
```sql
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name_en VARCHAR(200),
    department_name_ar VARCHAR(200),
    company_id INTEGER REFERENCES companies(company_id),
    manager_employee_id INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Examples from your data:
-- - المراجعة الداخلية (Internal Audit)
-- - المحاصيل (Crops)
-- - مكتب ر.مجلس الادارة (Board Chairman Office)
```

### 1.3 Locations
```sql
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    location_name_en VARCHAR(200),
    location_name_ar VARCHAR(200),
    location_type VARCHAR(50), -- 'office', 'farm', 'project_site'
    company_id INTEGER REFERENCES companies(company_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Examples: المركز الرئيسى, مزرعة المطار
```

### 1.4 Job Titles
```sql
CREATE TABLE job_titles (
    job_title_id SERIAL PRIMARY KEY,
    job_title_en VARCHAR(200),
    job_title_ar VARCHAR(200),
    job_code VARCHAR(20), -- J1, J2, etc.
    department_id INTEGER REFERENCES departments(department_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 1.5 Job Grades
```sql
CREATE TABLE job_grades (
    job_grade_id SERIAL PRIMARY KEY,
    grade_code VARCHAR(20), -- D3, M1, etc.
    grade_name VARCHAR(100),
    min_salary DECIMAL(10,2),
    max_salary DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 1.6 Sectors
```sql
CREATE TABLE sectors (
    sector_id SERIAL PRIMARY KEY,
    sector_name_en VARCHAR(200),
    sector_name_ar VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Examples: مكتب ر.مجلس الادارة, المحاصيل
```

---

## 2. EMPLOYEE MANAGEMENT

### 2.1 Employees (Main Table)
```sql
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    employee_code VARCHAR(20) UNIQUE NOT NULL, -- Your Column B (11, 12, 13...)
    name_en VARCHAR(200),
    name_ar VARCHAR(200) NOT NULL, -- Column C
    national_id VARCHAR(30) UNIQUE, -- Column DC
    
    -- Employment Details
    hire_date DATE NOT NULL, -- Column D
    termination_date DATE,
    employment_status VARCHAR(20) DEFAULT 'active', -- active/terminated/suspended
    
    -- Organization Structure
    company_id INTEGER REFERENCES companies(company_id), -- Column H
    department_id INTEGER REFERENCES departments(department_id), -- Column I
    sector_id INTEGER REFERENCES sectors(sector_id), -- Column E
    location_id INTEGER REFERENCES locations(location_id), -- Column F
    job_title_id INTEGER REFERENCES job_titles(job_title_id), -- Column G
    job_grade_id INTEGER REFERENCES job_grades(job_grade_id), -- Column J
    
    -- Contact Information
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    
    -- Bank Details
    bank_name VARCHAR(100), -- Column DB
    bank_account VARCHAR(50), -- Column DA
    
    -- Insurance Details
    social_insurance_number VARCHAR(50), -- Column CX
    social_insurance_salary DECIMAL(10,2), -- Column CW
    
    -- System Fields
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER,
    updated_by INTEGER
);

CREATE INDEX idx_employee_code ON employees(employee_code);
CREATE INDEX idx_employee_status ON employees(employment_status);
CREATE INDEX idx_employee_company ON employees(company_id);
```

### 2.2 Employee Documents
```sql
CREATE TABLE employee_documents (
    document_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    document_type VARCHAR(50), -- 'national_id', 'contract', 'certificate', etc.
    document_name VARCHAR(200),
    file_url VARCHAR(500),
    uploaded_at TIMESTAMP DEFAULT NOW(),
    uploaded_by INTEGER,
    is_active BOOLEAN DEFAULT TRUE
);
```

---

## 3. SALARY STRUCTURE

### 3.1 Employee Salary Components
```sql
CREATE TABLE employee_salary_components (
    component_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    
    -- Basic Salary (from Column M, CJ)
    basic_salary DECIMAL(10,2) NOT NULL,
    
    -- Fixed Allowances (Columns N, O, P)
    other_allowance DECIMAL(10,2) DEFAULT 0,
    location_allowance DECIMAL(10,2) DEFAULT 0,
    transport_housing_food_allowance DECIMAL(10,2) DEFAULT 0,
    
    -- Gross Salary (Column Q)
    gross_salary DECIMAL(10,2) NOT NULL,
    
    -- Effective Dates
    effective_from DATE NOT NULL,
    effective_to DATE,
    
    is_current BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_salary_employee ON employee_salary_components(employee_id);
CREATE INDEX idx_salary_current ON employee_salary_components(is_current);
```

### 3.2 Salary Component Types (for dynamic components)
```sql
CREATE TABLE salary_component_types (
    component_type_id SERIAL PRIMARY KEY,
    component_code VARCHAR(50),
    component_name_en VARCHAR(100),
    component_name_ar VARCHAR(100),
    component_category VARCHAR(20), -- 'earning', 'deduction'
    calculation_type VARCHAR(20), -- 'fixed', 'percentage', 'formula'
    is_taxable BOOLEAN DEFAULT TRUE,
    is_insurable BOOLEAN DEFAULT TRUE,
    is_active BOOLEAN DEFAULT TRUE
);
```

---

## 4. PAYROLL PROCESSING

### 4.1 Payroll Runs
```sql
CREATE TABLE payroll_runs (
    payroll_run_id SERIAL PRIMARY KEY,
    run_name VARCHAR(100), -- e.g., "December 2025 Payroll"
    company_id INTEGER REFERENCES companies(company_id),
    
    -- Period
    period_month INTEGER NOT NULL, -- 1-12
    period_year INTEGER NOT NULL, -- 2025
    period_start_date DATE NOT NULL,
    period_end_date DATE NOT NULL,
    working_days INTEGER NOT NULL, -- Column K (31 for December)
    
    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft/calculated/approved/paid
    
    -- Totals (for reconciliation)
    total_gross DECIMAL(12,2),
    total_deductions DECIMAL(12,2),
    total_net DECIMAL(12,2),
    total_employees INTEGER,
    
    -- Audit
    created_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER,
    approved_at TIMESTAMP,
    approved_by INTEGER,
    paid_at TIMESTAMP
);

CREATE INDEX idx_payroll_period ON payroll_runs(period_year, period_month);
CREATE INDEX idx_payroll_company ON payroll_runs(company_id);
```

### 4.2 Payroll Items (Individual Employee Payroll)
```sql
CREATE TABLE payroll_items (
    payroll_item_id SERIAL PRIMARY KEY,
    payroll_run_id INTEGER REFERENCES payroll_runs(payroll_run_id),
    employee_id INTEGER REFERENCES employees(employee_id),
    
    -- EARNINGS
    basic_salary DECIMAL(10,2), -- Column M
    other_allowance DECIMAL(10,2), -- Column N
    location_allowance DECIMAL(10,2), -- Column O
    transport_allowance DECIMAL(10,2), -- Column P
    gross_salary DECIMAL(10,2), -- Column Q
    
    -- Incentives & Variable Pay (Columns R-U)
    incentive_amount DECIMAL(10,2) DEFAULT 0, -- Column R
    incentive_percentage DECIMAL(5,2) DEFAULT 0, -- Column S
    incentive_days INTEGER DEFAULT 0, -- Column T
    monthly_incentive DECIMAL(10,2) DEFAULT 0, -- Column U
    
    -- Overtime (Columns V-Y)
    overtime_hours DECIMAL(5,2) DEFAULT 0, -- Column V
    overtime_weekend_hours DECIMAL(5,2) DEFAULT 0, -- Column W
    overtime_weekend_days INTEGER DEFAULT 0, -- Column X
    overtime_amount DECIMAL(10,2) DEFAULT 0, -- Column Y
    
    -- Settlement (Columns Z-AB)
    settlement_days INTEGER DEFAULT 0, -- Column Z
    settlement_amount DECIMAL(10,2) DEFAULT 0, -- Column AA
    settlement_total DECIMAL(10,2) DEFAULT 0, -- Column AB
    
    -- Other Income (Columns AC-AE)
    other_income DECIMAL(10,2) DEFAULT 0, -- Column AC
    variable_income DECIMAL(10,2) DEFAULT 0, -- Column AD
    minimum_wage_difference DECIMAL(10,2) DEFAULT 0, -- Column AE
    
    -- Total Income (Columns AF-AG)
    total_income DECIMAL(10,2), -- Column AF
    grand_total_income DECIMAL(10,2), -- Column AG
    
    -- DEDUCTIONS
    -- Performance & Attendance (Columns AH-BF)
    performance_deduction DECIMAL(10,2) DEFAULT 0, -- Column AI
    not_appearance_days INTEGER DEFAULT 0, -- Column AJ
    not_appearance_amount DECIMAL(10,2) DEFAULT 0, -- Column AK
    penalty_days INTEGER DEFAULT 0, -- Column AL
    penalty_amount DECIMAL(10,2) DEFAULT 0, -- Column AM
    
    sick_leave_days INTEGER DEFAULT 0, -- Column AN
    sick_leave_deduction DECIMAL(10,2) DEFAULT 0, -- Column AO
    
    unpaid_days INTEGER DEFAULT 0, -- Column AP
    unpaid_vacations DECIMAL(10,2) DEFAULT 0, -- Column AQ
    
    absence_days INTEGER DEFAULT 0, -- Column AR
    absence_penalty DECIMAL(10,2) DEFAULT 0, -- Column AT
    absence_total DECIMAL(10,2) DEFAULT 0, -- Column AW
    
    no_fingerprint_times INTEGER DEFAULT 0, -- Column AS
    no_fingerprint_days INTEGER DEFAULT 0, -- Column AU
    no_fingerprint_deduction DECIMAL(10,2) DEFAULT 0, -- Column AV
    
    late_minutes INTEGER DEFAULT 0, -- Column AX
    late_penalty DECIMAL(10,2) DEFAULT 0, -- Column AY
    lateness_total DECIMAL(10,2) DEFAULT 0, -- Column AZ
    
    early_leave_days INTEGER DEFAULT 0, -- Column BA
    early_leave_penalty DECIMAL(10,2) DEFAULT 0, -- Column BB
    early_leave_total DECIMAL(10,2) DEFAULT 0, -- Column BC
    
    performance_ded DECIMAL(10,2) DEFAULT 0, -- Column BD
    previous_deducted_days INTEGER DEFAULT 0, -- Column BE
    previous_deductions DECIMAL(10,2) DEFAULT 0, -- Column BF
    
    subtotal_deductions DECIMAL(10,2), -- Column BG
    
    -- Non-taxable Deductions (Columns BH-BP)
    non_taxable_deductions DECIMAL(10,2) DEFAULT 0, -- Column BH
    loans DECIMAL(10,2) DEFAULT 0, -- Column BI
    medical_insurance_employee DECIMAL(10,2) DEFAULT 0, -- Column BJ
    premium_card_deductions DECIMAL(10,2) DEFAULT 0, -- Column BK
    mobile_deductions_1 DECIMAL(10,2) DEFAULT 0, -- Column BL
    martyrs_contribution DECIMAL(10,2) DEFAULT 0, -- Column BM
    mobile_deductions DECIMAL(10,2) DEFAULT 0, -- Column BN
    medical_insurance_max DECIMAL(10,2) DEFAULT 0, -- Column BO
    medical_insurance_taxes DECIMAL(10,2) DEFAULT 0, -- Column BP
    penalties DECIMAL(10,2) DEFAULT 0, -- Column BQ
    
    -- Social Insurance & Tax (Columns BS-BT)
    total_deducted_days INTEGER, -- Column BR
    social_insurance_employee DECIMAL(10,2), -- Column BS (11% of CW)
    tax DECIMAL(10,2), -- Column BT
    
    -- Total Deductions & Net (Columns BU-BW)
    total_deductions DECIMAL(10,2), -- Column BU
    net_salary DECIMAL(10,2), -- Column BV/BW
    
    -- TAX CALCULATION (Columns CC-CG)
    taxable_salary DECIMAL(10,2), -- Column CC
    yearly_taxable_salary DECIMAL(10,2), -- Column CD
    tax_formula_result DECIMAL(10,2), -- Column CE
    monthly_tax DECIMAL(10,2), -- Column CG
    
    -- EMPLOYER COSTS (Columns CQ-CW)
    social_insurance_employer DECIMAL(10,2), -- Column CQ (18.75% of CW)
    total_social_insurance DECIMAL(10,2), -- Column CR
    medical_insurance_employer DECIMAL(10,2), -- Column CT
    total_medical_insurance DECIMAL(10,2), -- Column CU
    
    -- Working Days (Column K)
    working_days INTEGER, -- Column K
    
    -- Audit
    created_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER
);

CREATE INDEX idx_payroll_items_run ON payroll_items(payroll_run_id);
CREATE INDEX idx_payroll_items_employee ON payroll_items(employee_id);
```

### 4.3 Payroll Reconciliation
```sql
CREATE TABLE payroll_reconciliation (
    reconciliation_id SERIAL PRIMARY KEY,
    payroll_run_id INTEGER REFERENCES payroll_runs(payroll_run_id),
    
    previous_month_date DATE,
    current_month_date DATE,
    
    previous_employee_count INTEGER,
    current_employee_count INTEGER,
    difference INTEGER,
    
    previous_total_gross DECIMAL(12,2),
    current_total_gross DECIMAL(12,2),
    gross_difference DECIMAL(12,2),
    
    notes TEXT,
    reconciled_at TIMESTAMP DEFAULT NOW(),
    reconciled_by INTEGER
);
```

---

## 5. LEAVE MANAGEMENT

### 5.1 Leave Types
```sql
CREATE TABLE leave_types (
    leave_type_id SERIAL PRIMARY KEY,
    leave_name_en VARCHAR(100),
    leave_name_ar VARCHAR(100),
    default_days_per_year INTEGER,
    is_paid BOOLEAN DEFAULT TRUE,
    requires_approval BOOLEAN DEFAULT TRUE,
    max_carry_forward INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert default leave types
INSERT INTO leave_types (leave_name_en, leave_name_ar, default_days_per_year, is_paid) VALUES
('Annual Leave', 'إجازة سنوية', 21, TRUE),
('Sick Leave', 'إجازة مرضية', 15, TRUE),
('Emergency Leave', 'إجازة طارئة', 7, FALSE),
('Maternity Leave', 'إجازة وضع', 90, TRUE);
```

### 5.2 Leave Balances
```sql
CREATE TABLE leave_balances (
    balance_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    leave_type_id INTEGER REFERENCES leave_types(leave_type_id),
    year INTEGER NOT NULL,
    
    total_days DECIMAL(5,2) NOT NULL,
    used_days DECIMAL(5,2) DEFAULT 0,
    remaining_days DECIMAL(5,2) NOT NULL,
    
    carry_forward_days DECIMAL(5,2) DEFAULT 0,
    
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(employee_id, leave_type_id, year)
);
```

### 5.3 Leave Requests
```sql
CREATE TABLE leave_requests (
    request_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    leave_type_id INTEGER REFERENCES leave_types(leave_type_id),
    
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    days_requested DECIMAL(5,2) NOT NULL,
    
    reason TEXT,
    
    status VARCHAR(20) DEFAULT 'pending', -- pending/approved/rejected/cancelled
    
    requested_at TIMESTAMP DEFAULT NOW(),
    approved_by INTEGER REFERENCES employees(employee_id),
    approved_at TIMESTAMP,
    rejection_reason TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_leave_requests_employee ON leave_requests(employee_id);
CREATE INDEX idx_leave_requests_status ON leave_requests(status);
```

---

## 6. ATTENDANCE TRACKING

### 6.1 Attendance Records
```sql
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    attendance_date DATE NOT NULL,
    
    clock_in TIME,
    clock_out TIME,
    total_hours DECIMAL(5,2),
    
    status VARCHAR(20), -- present/absent/half_day/leave/sick/weekend
    
    late_minutes INTEGER DEFAULT 0,
    early_leave_minutes INTEGER DEFAULT 0,
    
    no_fingerprint BOOLEAN DEFAULT FALSE,
    
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(employee_id, attendance_date)
);

CREATE INDEX idx_attendance_employee ON attendance(employee_id);
CREATE INDEX idx_attendance_date ON attendance(attendance_date);
CREATE INDEX idx_attendance_status ON attendance(status);
```

---

## 7. TERMINATED EMPLOYEES (LEAVERS)

### 7.1 Terminations
```sql
CREATE TABLE employee_terminations (
    termination_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    
    termination_date DATE NOT NULL,
    termination_reason VARCHAR(50), -- resignation/termination/retirement/contract_end
    
    notice_period_days INTEGER,
    last_working_date DATE,
    
    eos_payment DECIMAL(10,2), -- End of Service payment
    final_settlement DECIMAL(10,2),
    
    payment_method VARCHAR(20), -- bank/cash
    payment_status VARCHAR(20), -- pending/paid
    
    notes TEXT,
    
    processed_by INTEGER,
    processed_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 8. PAYSLIPS

### 8.1 Payslip Generation
```sql
CREATE TABLE payslips (
    payslip_id SERIAL PRIMARY KEY,
    payroll_item_id INTEGER REFERENCES payroll_items(payroll_item_id),
    employee_id INTEGER REFERENCES employees(employee_id),
    payroll_run_id INTEGER REFERENCES payroll_runs(payroll_run_id),
    
    file_url VARCHAR(500), -- S3/Blob storage URL
    pdf_generated BOOLEAN DEFAULT FALSE,
    
    generated_at TIMESTAMP DEFAULT NOW(),
    sent_at TIMESTAMP,
    viewed_at TIMESTAMP,
    downloaded_at TIMESTAMP
);

CREATE INDEX idx_payslips_employee ON payslips(employee_id);
CREATE INDEX idx_payslips_run ON payslips(payroll_run_id);
```

---

## 9. USER MANAGEMENT & AUTHENTICATION

### 9.1 Users
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 9.2 Roles
```sql
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    role_description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Insert default roles
INSERT INTO roles (role_name, role_description) VALUES
('admin', 'Full system access'),
('hr_manager', 'HR management and payroll processing'),
('department_manager', 'Department-level access'),
('payroll_specialist', 'Payroll processing only'),
('employee', 'Self-service portal access only');
```

### 9.3 User Roles (Many-to-Many)
```sql
CREATE TABLE user_roles (
    user_role_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    role_id INTEGER REFERENCES roles(role_id),
    assigned_at TIMESTAMP DEFAULT NOW(),
    assigned_by INTEGER,
    
    UNIQUE(user_id, role_id)
);
```

---

## 10. AUDIT LOG

```sql
CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    action VARCHAR(50), -- create/update/delete/view
    table_name VARCHAR(100),
    record_id INTEGER,
    old_values JSONB,
    new_values JSONB,
    ip_address VARCHAR(50),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_logs(user_id);
CREATE INDEX idx_audit_table ON audit_logs(table_name);
CREATE INDEX idx_audit_created ON audit_logs(created_at);
```

---

## 11. SYSTEM CONFIGURATION

```sql
CREATE TABLE system_settings (
    setting_id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type VARCHAR(20), -- string/number/boolean/json
    description TEXT,
    updated_at TIMESTAMP DEFAULT NOW(),
    updated_by INTEGER
);

-- Insert default settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
('minimum_wage', '6000', 'number', 'Minimum wage in EGP'),
('social_insurance_employee_rate', '0.11', 'number', 'Employee SI rate (11%)'),
('social_insurance_employer_rate', '0.1875', 'number', 'Employer SI rate (18.75%)'),
('tax_brackets', '[{"min":0,"max":40000,"rate":0},{"min":40000,"max":55000,"rate":0.10}]', 'json', 'Tax brackets'),
('working_days_per_month', '30', 'number', 'Default working days');
```

---

## NOTES

1. **Multi-Company Support**: All tables include `company_id` where relevant
2. **Arabic Language**: All name fields have both English and Arabic versions
3. **Audit Trail**: Created/updated timestamps and user tracking
4. **Soft Deletes**: Use `is_active` flags instead of hard deletes
5. **Indexes**: Created for common query patterns
6. **Constraints**: Foreign keys maintain referential integrity

## NEXT STEPS

1. Review and approve schema
2. Set up development database
3. Create migration scripts from your Excel
4. Test with sample data
5. Build API endpoints
