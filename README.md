# 🔍 NCTracker - Quality NCR Management System

**A modern web-based solution for Non-Conformance Report management, replacing GitLab markdown workflows with a powerful, user-friendly application.**

## 🎯 Overview

NCTracker transforms your quality management process by replacing manual GitLab markdown NCR creation with a streamlined, database-driven system. Built with Streamlit and SQLite, it provides:

- **📋 Complete 5-Section NCR Forms** - Mirrors your existing GitLab template exactly
- **📊 Real-time Dashboard** - Beautiful analytics and KPI tracking
- **🔍 Advanced Search & Filtering** - Find any NCR instantly
- **👥 Multi-User Collaboration** - Comments, mentions, file attachments
- **📈 Analytics & Reporting** - Export to Excel, generate trend reports
- **🌐 Local Network Deployment** - Run on your company network

## ✨ Key Features

### 🔄 Complete Workflow
- **Section 1**: NCR Details (Basic Information, Problem Statement, Containment)
- **Section 2**: NC Level & CAPA (Risk Assessment, Assignment)
- **Section 3**: Investigation & Disposition (Root Cause, Disposition)
- **Section 4**: Correction Actions (Preventive Measures)
- **Section 5**: Closure & QA Audit (Final Review)

### 📊 Analytics & Insights
- **Real-time Dashboard** with key metrics
- **Trend Analysis** - Monthly NCR volumes, resolution times
- **Category Analysis** - Problem types, disposition patterns
- **Performance Metrics** - Average resolution times, department efficiency
- **Export Capabilities** - Excel reports, text summaries

### 🔍 Powerful Search
- **Multi-criteria Search** - Status, NC level, date ranges
- **Text Search** - Search across titles, descriptions, part numbers
- **Advanced Filters** - Combine multiple criteria
- **Quick Access** - Recent NCRs, favorites

### 👥 Collaboration Features
- **User Management** - Role-based access (NCR Owner, QE, MRB Team, Admin)
- **Comments System** - Discussion threads on each NCR
- **@Mentions** - Notify specific users
- **File Attachments** - Support for document uploads
- **Status Tracking** - Complete audit trail

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Local network access
- 2GB+ RAM recommended

### Installation (2 minutes)
```bash
# 1. Navigate to project directory
cd QualityNCR-Tracker

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
streamlit run app.py

# 4. Open browser to http://localhost:8501
```

### First Login
- **Username**: `admin`
- **Password**: `admin123`
- **⚠️ Important**: Change password after first login!

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User PCs      │    │  NCTracker App   │    │   SQLite DB     │
│                 │    │                  │    │                 │
│ - Web Browser   │◄──►│ - Streamlit      │◄──►│ - NCR Records   │
│ - Local Network │    │ - User Management│    │ - User Data     │
│                 │    │ - Analytics      │    │ - Comments      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Database**: SQLite (Single file, no server required)
- **Visualizations**: Plotly (Interactive charts)
- **Data Processing**: Pandas (Data analysis)
- **Authentication**: Session-based with password hashing

## 📖 User Guide

### Getting Started
1. **Login** with your credentials
2. **Dashboard** - View system overview and key metrics
3. **New NCR** - Create a new nonconformance report
4. **Search** - Find existing NCRs
5. **Analytics** - Review trends and performance

### Creating an NCR
1. **Navigate to "➕ New NCR"**
2. **Complete Section 1** - Basic details and problem statement
3. **Complete Section 2** - NC level and CAPA assessment
4. **Complete Section 3** - Investigation and disposition
5. **Complete Section 4** - Correction actions
6. **Complete Section 5** - Final QA audit
7. **Submit** - NCR is created and tracked

### Managing Users
1. **Go to "👥 Users"**
2. **Add New Users** - Specify role and department
3. **User Roles**:
   - **NCR Owner**: Create and manage NCRs
   - **QE (Quality Engineer)**: Advanced permissions
   - **MRB Team**: Investigation and disposition
   - **Admin**: Full system access

### Using Analytics
1. **Dashboard** - Real-time overview
2. **Analytics Page** - Detailed analysis
3. **Export Data** - Download Excel reports
4. **Generate Reports** - Summary documents

## 🔧 Configuration

### Network Deployment
For local network access, run with network configuration:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### Custom Settings
Edit `app.py` to customize:
- Page title and icons
- Color scheme
- Default values
- Feature toggles

## 📊 Database Schema

### Core Tables
- **users** - User accounts and roles
- **ncrs** - Main NCR records
- **comments** - Collaboration discussions
- **attachments** - File uploads
- **status_history** - Change tracking
- **mentions** - User notifications

### Data Relationships
- NCRs have multiple comments and attachments
- Users can be assigned to multiple NCRs
- Status changes are tracked with timestamps
- File uploads are linked to specific NCRs

## 🔒 Security Features

- **Password Hashing** - SHA-256 encryption
- **Session Management** - Secure user sessions
- **Role-based Access** - Permission control
- **Audit Trail** - Complete change history
- **Data Validation** - Input sanitization

## 📈 Performance

### Expected Performance
- **Concurrent Users**: 10-20 users
- **Database Size**: Up to 100MB comfortably
- **Response Time**: < 2 seconds for most operations
- **Uptime**: 99%+ with proper maintenance

### Optimization Tips
- Regular database backups
- Archive old NCRs yearly
- Monitor disk space
- Update dependencies regularly

## 🛠️ Maintenance

### Regular Tasks
- **Daily**: Check system is running
- **Weekly**: Review backup procedures
- **Monthly**: Update user access reviews
- **Quarterly**: Archive old data

### Backup Procedure
```bash
# Backup database
cp nctracker.db nctracker_backup_$(date +%Y%m%d).db

# Backup uploads
cp -r uploads uploads_backup_$(date +%Y%m%d)
```

## 🆘 Troubleshooting

### Common Issues
| Problem | Solution |
|---------|----------|
| Cannot access application | Check server is running, verify IP/port |
| Database errors | Check file permissions, disk space |
| Slow performance | Monitor server resources, optimize queries |
| Login issues | Verify username/password, check database |

### Log Files
- **Console Output**: Real-time application logs
- **Browser Console**: JavaScript errors
- **Streamlit Logs**: Connection attempts and errors

## 📋 Comparison: GitLab vs NCTracker

| Feature | GitLab (Current) | NCTracker (New) |
|---------|------------------|-----------------|
| **Form Creation** | Manual markdown editing | Guided form interface |
| **Data Analysis** | Parsing nightmare | Real-time analytics |
| **Search** | GitLab search | Advanced filtering |
| **Collaboration** | Comments system | Rich collaboration features |
| **Reporting** | Manual export | One-click reports |
| **Accessibility** | GitLab access required | Standalone web app |
| **Data Insights** | Not available | Dashboard & trends |

## 🎉 Benefits

### For Users
- **Easier to Use** - No more markdown editing
- **Faster Creation** - Guided form workflow
- **Better Search** - Find any NCR instantly
- **Real-time Insights** - See trends and patterns

### for Management
- **Better Data** - Structured, analyzable data
- **Reporting** - Easy export and analysis
- **Visibility** - Real-time dashboard
- **Compliance** - Complete audit trail

### For IT
- **Simple Deployment** - No complex setup
- **Easy Maintenance** - Single file database
- **Network Ready** - Multi-user from day one
- **Backup Simple** - Copy database file

## 🚀 Next Steps

1. **Deploy Locally** - Follow deployment guide
2. **Create Test Users** - Set up your team
3. **Migrate Data** - Import existing NCRs (optional)
4. **Train Users** - Brief team on new system
5. **Monitor Performance** - Track adoption and usage

## 📞 Support

- **Documentation**: Check `DEPLOYMENT_GUIDE.md`
- **Testing**: Run `python test_app.py`
- **Logs**: Check console output
- **Issues**: Review troubleshooting section

---

**🎯 Ready to modernize your quality management? Start with NCTracker today!**