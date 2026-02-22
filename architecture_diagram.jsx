import React, { useState } from 'react';
import { Database, Server, Globe, Users, FileText, Calendar, DollarSign, Settings, Lock, BarChart3 } from 'lucide-react';

export default function HRPayrollArchitecture() {
  const [selectedLayer, setSelectedLayer] = useState(null);

  const layers = {
    presentation: {
      title: "Presentation Layer",
      color: "bg-blue-500",
      icon: Globe,
      items: [
        "React.js Frontend (Web App)",
        "Responsive Design (Mobile/Tablet/Desktop)",
        "Material-UI Components",
        "Real-time Updates",
        "Multi-language Support (EN/AR)"
      ]
    },
    application: {
      title: "Application Layer",
      color: "bg-green-500",
      icon: Server,
      items: [
        "RESTful API Gateway",
        "Node.js/Express Backend",
        "JWT Authentication",
        "Role-Based Access Control (RBAC)",
        "Business Logic Services"
      ]
    },
    services: {
      title: "Microservices",
      color: "bg-purple-500",
      icon: Settings,
      modules: [
        { name: "Employee Management", icon: Users, features: ["Profile Management", "Document Storage", "Org Structure"] },
        { name: "Payroll Processing", icon: DollarSign, features: ["Salary Calculation", "Tax Computation", "Bulk Processing"] },
        { name: "Leave & Attendance", icon: Calendar, features: ["Leave Requests", "Attendance Tracking", "Approval Workflow"] },
        { name: "Reporting", icon: BarChart3, features: ["Financial Reports", "Analytics", "Excel Export"] },
        { name: "Authentication", icon: Lock, features: ["User Login", "MFA", "Session Management"] }
      ]
    },
    data: {
      title: "Data Layer",
      color: "bg-orange-500",
      icon: Database,
      items: [
        "PostgreSQL (Primary Database)",
        "Redis (Cache & Sessions)",
        "AWS S3 (Document Storage)",
        "Backup & Recovery System"
      ]
    }
  };

  const features = [
    { name: "Employee Management", desc: "700+ employees across 5 companies", icon: Users },
    { name: "Payroll Processing", desc: "Automated salary calculation with 127 components", icon: DollarSign },
    { name: "Leave & Attendance", desc: "Leave requests, approvals, attendance tracking", icon: Calendar },
    { name: "Payslips", desc: "PDF generation & automated email delivery", icon: FileText },
    { name: "Reports", desc: "Real-time dashboards & Excel exports", icon: BarChart3 },
    { name: "Self-Service", desc: "Employee portal for payslips & requests", icon: Users }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-slate-800 mb-4">
            HR & Payroll System Architecture
          </h1>
          <p className="text-lg text-slate-600">
            Web-based solution for 500+ employees across multiple companies
          </p>
        </div>

        {/* Architecture Layers */}
        <div className="space-y-6 mb-12">
          {/* Presentation Layer */}
          <div 
            className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-blue-500 cursor-pointer hover:shadow-xl transition-shadow"
            onClick={() => setSelectedLayer(selectedLayer === 'presentation' ? null : 'presentation')}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Globe className="w-8 h-8 text-blue-500" />
                <h2 className="text-2xl font-bold text-slate-800">Presentation Layer</h2>
              </div>
              <span className="text-sm text-slate-500">Click to expand</span>
            </div>
            {selectedLayer === 'presentation' && (
              <div className="mt-4 grid grid-cols-2 gap-4">
                {layers.presentation.items.map((item, idx) => (
                  <div key={idx} className="bg-blue-50 p-3 rounded-lg">
                    <p className="text-slate-700">{item}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Application Layer */}
          <div 
            className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-green-500 cursor-pointer hover:shadow-xl transition-shadow"
            onClick={() => setSelectedLayer(selectedLayer === 'application' ? null : 'application')}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Server className="w-8 h-8 text-green-500" />
                <h2 className="text-2xl font-bold text-slate-800">Application Layer</h2>
              </div>
              <span className="text-sm text-slate-500">Click to expand</span>
            </div>
            {selectedLayer === 'application' && (
              <div className="mt-4 grid grid-cols-2 gap-4">
                {layers.application.items.map((item, idx) => (
                  <div key={idx} className="bg-green-50 p-3 rounded-lg">
                    <p className="text-slate-700">{item}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Services Layer */}
          <div className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-purple-500">
            <div className="flex items-center space-x-4 mb-6">
              <Settings className="w-8 h-8 text-purple-500" />
              <h2 className="text-2xl font-bold text-slate-800">Microservices</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {layers.services.modules.map((module, idx) => {
                const Icon = module.icon;
                return (
                  <div key={idx} className="bg-purple-50 p-4 rounded-lg">
                    <div className="flex items-center space-x-2 mb-3">
                      <Icon className="w-5 h-5 text-purple-600" />
                      <h3 className="font-semibold text-slate-800">{module.name}</h3>
                    </div>
                    <ul className="space-y-1">
                      {module.features.map((feature, fidx) => (
                        <li key={fidx} className="text-sm text-slate-600">• {feature}</li>
                      ))}
                    </ul>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Data Layer */}
          <div 
            className="bg-white rounded-lg shadow-lg p-6 border-l-4 border-orange-500 cursor-pointer hover:shadow-xl transition-shadow"
            onClick={() => setSelectedLayer(selectedLayer === 'data' ? null : 'data')}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Database className="w-8 h-8 text-orange-500" />
                <h2 className="text-2xl font-bold text-slate-800">Data Layer</h2>
              </div>
              <span className="text-sm text-slate-500">Click to expand</span>
            </div>
            {selectedLayer === 'data' && (
              <div className="mt-4 grid grid-cols-2 gap-4">
                {layers.data.items.map((item, idx) => (
                  <div key={idx} className="bg-orange-50 p-3 rounded-lg">
                    <p className="text-slate-700">{item}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Key Features */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-2xl font-bold text-slate-800 mb-6 text-center">Core Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, idx) => {
              const Icon = feature.icon;
              return (
                <div key={idx} className="border border-slate-200 rounded-lg p-5 hover:shadow-md transition-shadow">
                  <div className="flex items-start space-x-3">
                    <Icon className="w-6 h-6 text-indigo-600 flex-shrink-0 mt-1" />
                    <div>
                      <h3 className="font-semibold text-slate-800 mb-1">{feature.name}</h3>
                      <p className="text-sm text-slate-600">{feature.desc}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Excel Migration Info */}
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">From Excel to Modern System</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h3 className="font-semibold mb-2">Current State</h3>
              <ul className="space-y-1 text-sm">
                <li>• 127 columns of formulas</li>
                <li>• Manual calculations</li>
                <li>• 16 interconnected sheets</li>
                <li>• Risk of errors</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Migration Process</h3>
              <ul className="space-y-1 text-sm">
                <li>• Extract & clean data</li>
                <li>• Map to database tables</li>
                <li>• Automated scripts</li>
                <li>• Parallel running (1-2 months)</li>
              </ul>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Future State</h3>
              <ul className="space-y-1 text-sm">
                <li>• Automated calculations</li>
                <li>• Real-time reports</li>
                <li>• Mobile access</li>
                <li>• Audit trails</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Tech Stack Summary */}
        <div className="mt-12 bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-slate-800 mb-6 text-center">Recommended Tech Stack</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                <Globe className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="font-semibold text-slate-800 mb-2">Frontend</h3>
              <p className="text-sm text-slate-600">React.js + TypeScript</p>
              <p className="text-sm text-slate-600">Material-UI</p>
            </div>
            <div className="text-center">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                <Server className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="font-semibold text-slate-800 mb-2">Backend</h3>
              <p className="text-sm text-slate-600">Node.js + Express</p>
              <p className="text-sm text-slate-600">JWT Auth</p>
            </div>
            <div className="text-center">
              <div className="bg-orange-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                <Database className="w-8 h-8 text-orange-600" />
              </div>
              <h3 className="font-semibold text-slate-800 mb-2">Database</h3>
              <p className="text-sm text-slate-600">PostgreSQL</p>
              <p className="text-sm text-slate-600">Redis Cache</p>
            </div>
            <div className="text-center">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-3">
                <Settings className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="font-semibold text-slate-800 mb-2">Infrastructure</h3>
              <p className="text-sm text-slate-600">AWS / Azure</p>
              <p className="text-sm text-slate-600">Docker</p>
            </div>
          </div>
        </div>

        {/* Next Steps */}
        <div className="mt-12 bg-slate-800 rounded-lg shadow-lg p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">Next Steps</h2>
          <ol className="space-y-3">
            <li className="flex items-start">
              <span className="bg-indigo-500 rounded-full w-8 h-8 flex items-center justify-center mr-3 flex-shrink-0">1</span>
              <span>Review the architecture and database schema documents</span>
            </li>
            <li className="flex items-start">
              <span className="bg-indigo-500 rounded-full w-8 h-8 flex items-center justify-center mr-3 flex-shrink-0">2</span>
              <span>Decide on technology stack based on your team's expertise</span>
            </li>
            <li className="flex items-start">
              <span className="bg-indigo-500 rounded-full w-8 h-8 flex items-center justify-center mr-3 flex-shrink-0">3</span>
              <span>Set up development environment and database</span>
            </li>
            <li className="flex items-start">
              <span className="bg-indigo-500 rounded-full w-8 h-8 flex items-center justify-center mr-3 flex-shrink-0">4</span>
              <span>Create data migration scripts from Excel</span>
            </li>
            <li className="flex items-start">
              <span className="bg-indigo-500 rounded-full w-8 h-8 flex items-center justify-center mr-3 flex-shrink-0">5</span>
              <span>Build MVP (Employee Management + Basic Payroll)</span>
            </li>
          </ol>
        </div>
      </div>
    </div>
  );
}