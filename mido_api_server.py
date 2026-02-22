#!/usr/bin/env python3
"""
Mido System API Server
Backend for ECGS HR & Payroll System
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import hashlib
import urllib.parse

DB_PATH = 'mido_hr_database.db'

class MidoAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type='application/json'):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
    
    def do_GET(self):
        try:
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            query = urllib.parse.parse_qs(parsed_path.query)
            
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Login
            if path == '/api/login':
                username = query.get('username', [''])[0]
                password = query.get('password', [''])[0]
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                
                cursor.execute('''
                    SELECT u.id, u.username, u.role, u.employee_id, e.name, e.employee_code
                    FROM users u
                    LEFT JOIN employees e ON u.employee_id = e.id
                    WHERE u.username = ? AND u.password_hash = ?
                ''', (username, password_hash))
                
                user = cursor.fetchone()
                if user:
                    self._set_headers()
                    self.wfile.write(json.dumps(dict(user)).encode())
                else:
                    self._set_headers(401)
                    self.wfile.write(json.dumps({'error': 'Invalid credentials'}).encode())
            
            # Get employees
            elif path == '/api/employees':
                cursor.execute('''
                    SELECT e.*, c.name as company_name, d.name as department_name, p.name as position_name
                    FROM employees e
                    LEFT JOIN companies c ON e.company_id = c.id
                    LEFT JOIN departments d ON e.department_id = d.id
                    LEFT JOIN positions p ON e.position_id = p.id
                    WHERE e.status = 'active'
                    ORDER BY e.id
                ''')
                employees = [dict(row) for row in cursor.fetchall()]
                self._set_headers()
                self.wfile.write(json.dumps(employees).encode())
            
            # Get payroll
            elif path == '/api/payroll':
                emp_id = query.get('employee_id', [None])[0]
                if emp_id:
                    cursor.execute('''
                        SELECT p.*, e.name as employee_name, e.employee_code
                        FROM payroll p
                        JOIN employees e ON p.employee_id = e.id
                        WHERE p.employee_id = ?
                        ORDER BY p.year DESC, p.month DESC
                    ''', (emp_id,))
                else:
                    cursor.execute('''
                        SELECT p.*, e.name as employee_name, e.employee_code
                        FROM payroll p
                        JOIN employees e ON p.employee_id = e.id
                        ORDER BY p.year DESC, p.month DESC
                    ''')
                records = [dict(row) for row in cursor.fetchall()]
                self._set_headers()
                self.wfile.write(json.dumps(records).encode())
            
            # Get stats
            elif path == '/api/stats':
                stats = {}
                cursor.execute('SELECT COUNT(*) as count FROM employees WHERE status = "active"')
                stats['total_employees'] = cursor.fetchone()['count']
                
                cursor.execute('''
                    SELECT SUM(net_salary) as total 
                    FROM payroll 
                    WHERE month = "December" AND year = 2024
                ''')
                result = cursor.fetchone()
                stats['monthly_payroll'] = float(result['total']) if result['total'] else 0
                
                cursor.execute('SELECT COUNT(*) as count FROM leave_requests WHERE status = "pending"')
                stats['pending_leaves'] = cursor.fetchone()['count']
                
                from datetime import datetime
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('SELECT COUNT(*) as count FROM attendance WHERE date = ?', (today,))
                stats['present_today'] = cursor.fetchone()['count']
                
                self._set_headers()
                self.wfile.write(json.dumps(stats).encode())
            
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode())
            
            conn.close()
            
        except Exception as e:
            print(f"Error: {str(e)}")
            self._set_headers(500)
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, MidoAPIHandler)
    print(f'🚀 Mido System API Server')
    print(f'   URL: http://localhost:{port}')
    print(f'   Database: {DB_PATH}')
    print(f'   Press Ctrl+C to stop\n')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
