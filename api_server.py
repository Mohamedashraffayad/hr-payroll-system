#!/usr/bin/env python3
"""Complete HR System API with all features"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, sqlite3, hashlib, secrets, urllib.parse, os, base64
from datetime import datetime, timedelta

DB = 'hr_database.db'

class API(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        self.end_headers()
    
    def _json(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data).encode())
    
    def _error(self, msg, status=400):
        self._json({'error': msg}, status)
    
    def do_OPTIONS(self):
        self._set_headers(204)
    
    def do_GET(self):
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        path = urllib.parse.urlparse(self.path).path
        
        try:
            # Auth endpoints
            if path == '/api/employees':
                c.execute('''SELECT e.*, d.department_name, p.position_name 
                    FROM employees e 
                    LEFT JOIN departments d ON e.department_id=d.department_id
                    LEFT JOIN job_positions p ON e.position_id=p.position_id''')
                self._json({'employees': [dict(r) for r in c.fetchall()]})
            
            elif path.startswith('/api/employee/'):
                emp_id = path.split('/')[-1]
                c.execute('''SELECT e.*, d.department_name, p.position_name 
                    FROM employees e 
                    LEFT JOIN departments d ON e.department_id=d.department_id
                    LEFT JOIN job_positions p ON e.position_id=p.position_id
                    WHERE e.employee_id=?''', (emp_id,))
                r = c.fetchone()
                self._json({'employee': dict(r) if r else None})
            
            elif path == '/api/leave/requests':
                c.execute('''SELECT lr.*, e.employee_alias, e.employee_code, lt.leave_name
                    FROM leave_requests lr
                    JOIN employees e ON lr.employee_id=e.employee_id
                    JOIN leave_types lt ON lr.leave_type_id=lt.leave_type_id
                    ORDER BY lr.requested_at DESC''')
                self._json({'requests': [dict(r) for r in c.fetchall()]})
            
            elif path.startswith('/api/leave/employee/'):
                emp_id = path.split('/')[-1]
                c.execute('''SELECT lr.*, lt.leave_name FROM leave_requests lr
                    JOIN leave_types lt ON lr.leave_type_id=lt.leave_type_id
                    WHERE lr.employee_id=? ORDER BY lr.requested_at DESC''', (emp_id,))
                self._json({'requests': [dict(r) for r in c.fetchall()]})
            
            elif path.startswith('/api/leave/balances/'):
                emp_id = path.split('/')[-1]
                c.execute('''SELECT lb.*, lt.leave_name FROM leave_balances lb
                    JOIN leave_types lt ON lb.leave_type_id=lt.leave_type_id
                    WHERE lb.employee_id=? AND lb.year=2026''', (emp_id,))
                self._json({'balances': [dict(r) for r in c.fetchall()]})
            
            elif path.startswith('/api/attendance/employee/'):
                emp_id = path.split('/')[-1]
                c.execute('''SELECT * FROM attendance WHERE employee_id=? ORDER BY date DESC LIMIT 30''', (emp_id,))
                self._json({'attendance': [dict(r) for r in c.fetchall()]})
            
            elif path.startswith('/api/payroll/employee/'):
                emp_id = path.split('/')[-1]
                c.execute('SELECT * FROM payroll WHERE employee_id=? ORDER BY year DESC, month DESC', (emp_id,))
                self._json({'payroll': [dict(r) for r in c.fetchall()]})
            
            elif path == '/api/leave/types':
                c.execute('SELECT * FROM leave_types')
                self._json({'types': [dict(r) for r in c.fetchall()]})
            
            elif path == '/api/dashboard/stats':
                c.execute('SELECT COUNT(*) as total FROM employees WHERE status="active"')
                total_emp = c.fetchone()[0]
                c.execute('SELECT COUNT(*) as pending FROM leave_requests WHERE status="pending"')
                pending = c.fetchone()[0]
                c.execute('SELECT SUM(net_salary) as payroll FROM payroll WHERE year=2024 AND month=12')
                payroll = c.fetchone()[0] or 0
                self._json({'total_employees': total_emp, 'pending_leaves': pending, 'monthly_payroll': round(payroll,2)})
            
            else:
                self._error('Not found', 404)
        except Exception as e:
            self._error(str(e), 500)
        finally:
            conn.close()
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length).decode()) if length else {}
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        try:
            if self.path == '/api/auth/login':
                user = data.get('username')
                pwd = hashlib.sha256(data.get('password','').encode()).hexdigest()
                c.execute('''SELECT u.*, e.employee_alias, e.employee_code FROM users u
                    LEFT JOIN employees e ON u.employee_id=e.employee_id
                    WHERE u.username=? AND u.password_hash=? AND u.is_active=1''', (user, pwd))
                row = c.fetchone()
                if row:
                    self._json({'success': True, 'user': {
                        'user_id': row[0], 'username': row[1], 'role': row[3],
                        'employee_id': row[4], 'employee_alias': row[7], 'employee_code': row[8]
                    }})
                else:
                    self._error('Invalid credentials', 401)
            
            elif self.path == '/api/employee/add':
                c.execute('''INSERT INTO employees (employee_code, employee_alias, department_id, position_id, hire_date, basic_salary, allowances, status, bank_code)
                    VALUES (?,?,?,?,?,?,?,?,?)''', 
                    (data['code'], data['alias'], data['dept'], data['pos'], data['hire'], data['salary'], data.get('allow',0), 'active', data.get('bank','')))
                conn.commit()
                self._json({'success': True, 'employee_id': c.lastrowid}, 201)
            
            elif self.path == '/api/leave/request':
                emp_id = data['employee_id']
                leave_type = data['leave_type_id']
                start = data['start_date']
                end = data['end_date']
                days = data['days_count']
                reason = data.get('reason','')
                medical = data.get('medical_document','')
                
                c.execute('''INSERT INTO leave_requests (employee_id, leave_type_id, start_date, end_date, days_count, reason, medical_document)
                    VALUES (?,?,?,?,?,?,?)''', (emp_id, leave_type, start, end, days, reason, medical))
                conn.commit()
                self._json({'success': True, 'request_id': c.lastrowid}, 201)
            
            elif self.path == '/api/attendance/clock':
                c.execute('''INSERT INTO attendance (employee_id, date, clock_in, status)
                    VALUES (?,?,?,?)''', (data['employee_id'], datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M'), 'present'))
                conn.commit()
                self._json({'success': True})
            
            else:
                self._error('Not found', 404)
        except Exception as e:
            conn.rollback()
            self._error(str(e), 500)
        finally:
            conn.close()
    
    def do_PUT(self):
        length = int(self.headers.get('Content-Length', 0))
        data = json.loads(self.rfile.read(length).decode()) if length else {}
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        try:
            if '/approve' in self.path:
                req_id = self.path.split('/')[-2]
                c.execute('UPDATE leave_requests SET status="approved", reviewed_at=? WHERE request_id=?',
                         (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), req_id))
                conn.commit()
                self._json({'success': True})
            
            elif '/reject' in self.path:
                req_id = self.path.split('/')[-2]
                c.execute('UPDATE leave_requests SET status="rejected", reviewed_at=? WHERE request_id=?',
                         (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), req_id))
                conn.commit()
                self._json({'success': True})
            
            elif self.path.startswith('/api/employee/update/'):
                emp_id = self.path.split('/')[-1]
                c.execute('''UPDATE employees SET employee_alias=?, department_id=?, position_id=?, basic_salary=?, allowances=?
                    WHERE employee_id=?''', (data['alias'], data['dept'], data['pos'], data['salary'], data.get('allow',0), emp_id))
                conn.commit()
                self._json({'success': True})
            
            else:
                self._error('Not found', 404)
        except Exception as e:
            conn.rollback()
            self._error(str(e), 500)
        finally:
            conn.close()
    
    def log_message(self, format, *args):
        pass

def run(port=8000):
    server = HTTPServer(('', port), API)
    print(f'''
╔══════════════════════════════════════════════════════╗
║       HR SYSTEM API SERVER - RUNNING                 ║
╚══════════════════════════════════════════════════════╝
🌐 API: http://localhost:{port}
📊 Database: {DB}
✅ All endpoints ready
Press Ctrl+C to stop
    ''')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n🛑 Server stopped')

if __name__ == '__main__':
    run()
