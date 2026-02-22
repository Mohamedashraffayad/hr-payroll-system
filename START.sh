#!/bin/bash
echo "╔══════════════════════════════════════════════════════╗"
echo "║       HR SYSTEM - STARTING                           ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "📊 Database: hr_database.db (4 employees loaded)"
echo "🔐 Login Credentials:"
echo "   Admin: admin / admin123"
echo "   Employee: employee1 / emp1123"
echo ""
echo "🚀 Starting backend API server..."
echo ""
python3 api_server.py &
API_PID=$!
echo ""
echo "✅ API Server running (PID: $API_PID)"
echo "🌐 API: http://localhost:8000"
echo ""
echo "📱 Now open index.html in your browser"
echo "   Or run: python3 -m http.server 3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
wait $API_PID
