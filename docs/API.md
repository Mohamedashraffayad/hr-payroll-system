# API Documentation

Complete REST API reference for the HR & Payroll Management System.

## Base URL

```
http://localhost:8000/api
```

## Response Format

All responses are in JSON format:

```json
{
  "data": { ... },
  "count": 10
}
```

Error responses:
```json
{
  "error": "Error message here"
}
```

---

## Authentication

Currently, the API is open for development. For production, implement JWT authentication:

```bash
# Login (planned)
POST /api/auth/login
{
  "username": "admin",
  "password": "password"
}

# Response
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": { ... }
}
```

---

## Employees

### List All Employees

```bash
GET /api/employees
```

**Response:**
```json
{
  "employees": [
    {
      "employee_id": 1,
      "employee_code": "11",
      "name_en": "Ahmed Hassan Ibrahim",
      "name_ar": "أحمد حسن إبراهيم",
      "national_id": "25302220100074",
      "hire_date": "2015-11-15",
      "company_name_en": "Tiba Landscape for General Contracting",
      "department_name_en": "Internal Audit",
      "location_name_en": "Head Office",
      "grade_code": "D3",
      "basic_salary": 8334,
      "employment_status": "active"
    }
  ],
  "count": 10
}
```

### Get Single Employee

```bash
GET /api/employees/:id
```

**Response:**
```json
{
  "employee": {
    "employee_id": 1,
    "employee_code": "11",
    "name_en": "Ahmed Hassan Ibrahim",
    "name_ar": "أحمد حسن إبراهيم",
    "basic_salary": 8334,
    "other_allowance": 0,
    "gross_salary": 8334,
    "bank_name": "CIB",
    "bank_account": "100025470607",
    "social_insurance_number": "74952464"
  }
}
```

### Create Employee

```bash
POST /api/employees
Content-Type: application/json

{
  "employee_code": "350",
  "name_en": "John Doe",
  "name_ar": "جون دو",
  "national_id": "12345678901234",
  "hire_date": "2026-01-01",
  "company_id": 1,
  "department_id": 1,
  "location_id": 1,
  "job_title_id": 1,
  "job_grade_id": 1,
  "phone": "01012345678",
  "email": "john@example.com",
  "basic_salary": 10000,
  "other_allowance": 500,
  "bank_name": "CIB",
  "bank_account": "100012345678"
}
```

**Response:**
```json
{
  "message": "Employee created",
  "employee_id": 11
}
```

---

## Payroll

### List Payroll Runs

```bash
GET /api/payroll/runs
```

**Response:**
```json
{
  "payroll_runs": [
    {
      "payroll_run_id": 1,
      "run_name": "January 2026 Payroll",
      "period_month": 1,
      "period_year": 2026,
      "working_days": 31,
      "status": "draft",
      "total_gross": 58342.00,
      "total_deductions": 6417.62,
      "total_net": 51924.38,
      "total_employees": 10
    }
  ]
}
```

### Get Payroll Details

```bash
GET /api/payroll/:run_id
```

**Response:**
```json
{
  "payroll_run": {
    "payroll_run_id": 1,
    "run_name": "January 2026 Payroll",
    "period_month": 1,
    "period_year": 2026,
    "total_net": 51924.38
  },
  "items": [
    {
      "payroll_item_id": 1,
      "employee_id": 1,
      "name_en": "Ahmed Hassan Ibrahim",
      "employee_code": "11",
      "basic_salary": 8334,
      "gross_salary": 8334,
      "social_insurance_employee": 916.74,
      "tax": 0,
      "total_deductions": 916.74,
      "net_salary": 7417.26
    }
  ]
}
```

### Create Payroll Run

```bash
POST /api/payroll/run
Content-Type: application/json

{
  "run_name": "February 2026 Payroll",
  "company_id": null,
  "period_month": 2,
  "period_year": 2026,
  "period_start_date": "2026-02-01",
  "period_end_date": "2026-02-28",
  "working_days": 28
}
```

**Response:**
```json
{
  "message": "Payroll run created",
  "payroll_run_id": 2,
  "employees_processed": 10
}
```

**What happens automatically:**
1. System retrieves all active employees
2. Gets their current salary components
3. Calculates social insurance (11% employee + 18.75% employer)
4. Calculates taxes based on Egyptian tax brackets
5. Computes net salary
6. Creates payroll items for each employee
7. Calculates totals

### Approve Payroll Run

```bash
PUT /api/payroll/:run_id/approve
```

**Response:**
```json
{
  "message": "Payroll approved"
}
```

---

## Leave Management

### List Leave Requests

```bash
GET /api/leave/requests
```

**Response:**
```json
{
  "leave_requests": [
    {
      "request_id": 1,
      "employee_id": 1,
      "name_en": "Ahmed Hassan Ibrahim",
      "employee_code": "11",
      "leave_name_en": "Annual Leave",
      "start_date": "2026-01-20",
      "end_date": "2026-01-25",
      "days_requested": 5,
      "reason": "Annual vacation",
      "status": "pending",
      "requested_at": "2026-01-10 10:30:00"
    }
  ]
}
```

### Get Employee Leave Balances

```bash
GET /api/leave/balances/:employee_id
```

**Response:**
```json
{
  "balances": [
    {
      "balance_id": 1,
      "employee_id": 1,
      "leave_type_id": 1,
      "leave_name_en": "Annual Leave",
      "leave_name_ar": "إجازة سنوية",
      "year": 2026,
      "total_days": 21,
      "used_days": 8,
      "remaining_days": 13
    }
  ]
}
```

### Submit Leave Request

```bash
POST /api/leave/request
Content-Type: application/json

{
  "employee_id": 1,
  "leave_type_id": 1,
  "start_date": "2026-02-10",
  "end_date": "2026-02-15",
  "days_requested": 5,
  "reason": "Family vacation"
}
```

**Response:**
```json
{
  "message": "Leave request submitted",
  "request_id": 7
}
```

### Approve Leave Request

```bash
PUT /api/leave/requests/:request_id/approve
```

**Response:**
```json
{
  "message": "Leave request approved"
}
```

### Reject Leave Request

```bash
PUT /api/leave/requests/:request_id/reject
Content-Type: application/json

{
  "reason": "Insufficient leave balance"
}
```

**Response:**
```json
{
  "message": "Leave request rejected"
}
```

---

## Statistics

### Dashboard Statistics

```bash
GET /api/stats/dashboard
```

**Response:**
```json
{
  "total_employees": 342,
  "monthly_payroll": 4200000.00,
  "on_leave_today": 18,
  "pending_approvals": 5,
  "company_breakdown": [
    {
      "company_name_en": "Tiba Landscape for General Contracting",
      "count": 154
    },
    {
      "company_name_en": "Al-Saman for Modern Agriculture",
      "count": 74
    }
  ]
}
```

---

## Master Data

### List Companies

```bash
GET /api/companies
```

**Response:**
```json
{
  "companies": [
    {
      "company_id": 1,
      "company_name_en": "Tiba Landscape for General Contracting",
      "company_name_ar": "طيبة لاند سكيب للمقاولات العامة",
      "is_active": 1
    }
  ]
}
```

### List Departments

```bash
GET /api/departments
```

**Response:**
```json
{
  "departments": [
    {
      "department_id": 1,
      "department_name_en": "Internal Audit",
      "department_name_ar": "المراجعة الداخلية",
      "company_id": 1,
      "company_name_en": "Tiba Landscape for General Contracting",
      "is_active": 1
    }
  ]
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request |
| 404  | Not Found |
| 500  | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting. For production, implement:
- 100 requests per minute per IP
- 1000 requests per hour per user

---

## CORS

Currently configured to allow all origins (`*`). For production, configure specific origins:

```python
Access-Control-Allow-Origin: https://yourdomain.com
```

---

## Examples

### Complete Payroll Workflow

```bash
# 1. Create payroll run
curl -X POST http://localhost:8000/api/payroll/run \
  -H "Content-Type: application/json" \
  -d '{
    "run_name": "March 2026 Payroll",
    "period_month": 3,
    "period_year": 2026,
    "period_start_date": "2026-03-01",
    "period_end_date": "2026-03-31",
    "working_days": 31
  }'

# 2. Review payroll
curl http://localhost:8000/api/payroll/1

# 3. Approve payroll
curl -X PUT http://localhost:8000/api/payroll/1/approve
```

### Leave Management Workflow

```bash
# 1. Check employee leave balance
curl http://localhost:8000/api/leave/balances/1

# 2. Submit leave request
curl -X POST http://localhost:8000/api/leave/request \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": 1,
    "leave_type_id": 1,
    "start_date": "2026-03-15",
    "end_date": "2026-03-20",
    "days_requested": 5,
    "reason": "Spring vacation"
  }'

# 3. Approve leave (manager)
curl -X PUT http://localhost:8000/api/leave/requests/1/approve
```

---

## Webhooks (Planned)

Future support for webhooks on events:
- Employee created
- Payroll approved
- Leave request submitted
- Leave request approved/rejected

---

## API Versioning

Current version: `v1`

Future versions will be accessible via:
```
/api/v2/employees
```

---

## Support

For API questions:
- Check this documentation
- Review the [README](../README.md)
- Open an issue on GitHub
