# NCTracker Deployment Guide
## Quality NCR Tracking System - Local Network Setup

### Overview
This guide explains how to deploy NCTracker on your local network so multiple users can access the system simultaneously.

### System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: Minimum 2GB, recommended 4GB+
- **Storage**: 500MB for application, additional space for file uploads
- **Network**: Local network with TCP/8501 access

### Quick Start (5 Minutes)
1. **Extract/Folder Setup**
   - Ensure you have the complete NCTracker folder with all files
   - Navigate to the project directory in terminal/command prompt

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   streamlit run app.py
   ```

4. **Access Application**
   - **Server Machine**: Open browser to `http://localhost:8501`
   - **Other Computers**: Open browser to `http://[SERVER_IP]:8501`

### Detailed Installation

#### Step 1: Environment Setup
1. **Install Python** (if not already installed)
   - Download from https://python.org
   - During installation, check "Add Python to PATH"

2. **Verify Installation**
   ```bash
   python --version
   pip --version
   ```

#### Step 2: Application Setup
1. **Download NCTracker Files**
   - Ensure all files are in the project directory:
     ```
     NCTracker/
     ├── app.py              (Main application)
     ├── database.py         (Database management)
     ├── utils.py            (Utility functions)
     ├── requirements.txt    (Dependencies)
     └── docs/              (Documentation)
     ```

2. **Install Dependencies**
   ```bash
   cd /path/to/NCTracker
   pip install -r requirements.txt
   ```

3. **Test Installation**
   ```bash
   python test_app.py
   ```
   Should show "🎉 All tests passed!"

#### Step 3: Network Configuration

**For Server Machine:**
1. **Run on Local Network**
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```
   - `--server.address 0.0.0.0` - Allow connections from any IP
   - `--server.port 8501` - Standard Streamlit port

2. **Note Your IP Address**
   - Windows: Run `ipconfig` in Command Prompt
   - Mac/Linux: Run `ifconfig` in Terminal
   - Look for IPv4 address (e.g., 192.168.1.100)

**For User Machines:**
1. **Find Server IP**
   - Ask the administrator for the server's IP address
   - OR use network scanning tools

2. **Access Application**
   ```
   http://[SERVER_IP]:8501
   ```
   Example: `http://192.168.1.100:8501`

#### Step 4: First Login
1. **Default Admin Account**
   - Username: `admin`
   - Password: `admin123`

2. **Create Additional Users**
   - Log in as admin
   - Go to "👥 Users" section
   - Add new users with appropriate roles

### Network Security Considerations

#### Firewall Configuration
- **Server Machine**: Allow incoming connections on port 8501
- **Router**: Ensure port 8501 is not blocked
- **Corporate Networks**: May require IT approval

#### Access Control
- Change default admin password immediately
- Use strong passwords for all accounts
- Regular backup of database file

### Troubleshooting

#### Common Issues

**"Cannot Access Application"**
- Check server is running
- Verify firewall settings
- Confirm correct IP address and port

**"Database Errors"**
- Ensure `nctracker.db` file has write permissions
- Check disk space availability
- Restart application

**"Slow Performance"**
- Check network bandwidth
- Monitor server resources (CPU/RAM)
- Consider upgrading hardware

#### Log Files
- Check console output for error messages
- Streamlit logs show connection attempts
- Browser console may show additional errors

### Maintenance

#### Regular Backups
```bash
# Backup database (daily recommended)
cp nctracker.db nctracker_backup_YYYYMMDD.db

# Backup uploads folder
cp -r uploads uploads_backup_YYYYMMDD
```

#### Updates
1. **Stop Application**: Press Ctrl+C in terminal
2. **Update Files**: Replace old files with new versions
3. **Test**: Run `python test_app.py`
4. **Restart**: Run `streamlit run app.py`

#### Database Management
- **View Size**: Database file should remain under 100MB for optimal performance
- **Clean Up**: Remove old attachments periodically
- **Archive**: Export old NCR data yearly

### Performance Optimization

#### For Small Teams (1-10 users)
- **Server Requirements**: Standard desktop/laptop
- **Network**: 100Mbps minimum
- **Concurrent Users**: 5-10

#### For Larger Teams (10-50 users)
- **Server Requirements**: Dedicated machine with 4GB+ RAM
- **Network**: 1Gbps recommended
- **Concurrent Users**: 10-20

### Advanced Configuration

#### Custom Port
```bash
streamlit run app.py --server.port 8502
```

#### Custom Host
```bash
streamlit run app.py --server.address 192.168.1.50
```

#### Development Mode (Auto-reload)
```bash
streamlit run app.py --server.runOnSave true
```

### User Training

#### Quick User Guide
1. **Login** with provided credentials
2. **Dashboard** - View summary statistics
3. **New NCR** - Create new nonconformance reports
4. **Search NCRs** - Find existing reports
5. **Analytics** - View trends and metrics

#### Key Features
- **5-Section Form**: Complete GitLab template workflow
- **Real-time Collaboration**: Comments and mentions
- **File Attachments**: Support for document uploads
- **Advanced Search**: Filter by status, level, dates
- **Export Capabilities**: Excel reports and summaries

### Support

#### System Health Check
- **Database Connection**: `python -c "from database import db; print('OK')"`
- **All Dependencies**: `python -c "import streamlit, pandas, plotly; print('OK')"`
- **File Permissions**: Ensure write access to directory

#### Emergency Procedures
1. **Application Not Responding**: Restart server
2. **Database Corruption**: Restore from latest backup
3. **Network Issues**: Check firewall and IP configuration

### Security Best Practices
- Change default passwords immediately
- Regular security updates
- Monitor access logs
- Backup strategy implementation
- User access review quarterly

---

## Success Checklist
- [ ] Python installed and working
- [ ] Dependencies installed successfully
- [ ] Application runs without errors
- [ ] Network access configured
- [ ] Default admin password changed
- [ ] First user created
- [ ] Sample data created (for testing)
- [ ] Backup procedure documented
- [ ] User training completed
- [ ] System monitoring in place

**🎉 Your NCTracker system is now ready for production use!**