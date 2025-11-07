"""
NCTracker Utility Functions
Helper functions for the application
"""

import hashlib
import os
from datetime import datetime, date
from typing import List, Dict, Any
import pandas as pd
import streamlit as st
from pathlib import Path

def hash_password(password: str) -> str:
    """Hash a password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def format_date(date_obj) -> str:
    """Format date for display"""
    if isinstance(date_obj, str):
        try:
            date_obj = pd.to_datetime(date_obj).date()
        except:
            return date_obj
    if isinstance(date_obj, (date, datetime)):
        return date_obj.strftime('%Y-%m-%d %H:%M')
    return str(date_obj)

def get_ncr_status_color(status: str) -> str:
    """Get color for NCR status"""
    colors = {
        'NEW': '#FF6B6B',
        'IN_PROGRESS': '#4ECDC4', 
        'PENDING_APPROVAL': '#45B7D1',
        'CLOSED': '#96CEB4'
    }
    return colors.get(status, '#95A5A6')

def get_nc_level_color(level: int) -> str:
    """Get color for NC level"""
    colors = {
        1: '#FF4757',  # Critical - Red
        2: '#FFA502',  # Adverse - Orange
        3: '#F1C40F',  # Moderate - Yellow
        4: '#2ED573'   # Low - Green
    }
    return colors.get(level, '#95A5A6')

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    
    return filename

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def calculate_resolution_time(created_at, closed_at) -> float:
    """Calculate resolution time in days"""
    try:
        created = pd.to_datetime(created_at)
        closed = pd.to_datetime(closed_at)
        return (closed - created).days
    except:
        return None

def get_user_initials(full_name: str) -> str:
    """Get user initials from full name"""
    if not full_name:
        return "??"
    parts = full_name.split()
    if len(parts) == 1:
        return parts[0][:2].upper()
    return f"{parts[0][0]}{parts[-1][0]}".upper()

def export_to_excel(ncrs: List[Dict]) -> bytes:
    """Export NCR data to Excel format"""
    if not ncrs:
        return b""
    
    # Create DataFrame
    df = pd.DataFrame(ncrs)
    
    # Clean up data for export
    columns_to_export = [
        'ncr_number', 'title', 'status', 'nc_level', 'site', 'part_number',
        'part_number_rev', 'quantity_affected', 'project_affected', 'supplier',
        'problem_category', 'disposition_action', 'created_by_name', 'created_at',
        'updated_at', 'closed_at'
    ]
    
    # Filter available columns
    available_columns = [col for col in columns_to_export if col in df.columns]
    export_df = df[available_columns].copy()
    
    # Format dates
    for col in ['created_at', 'updated_at', 'closed_at']:
        if col in export_df.columns:
            export_df[col] = pd.to_datetime(export_df[col]).dt.strftime('%Y-%m-%d %H:%M')
    
    # Convert to Excel
    import io
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, index=False, sheet_name='NCRs')
    output.seek(0)
    
    return output.getvalue()

def create_sample_data():
    """Create sample data for testing"""
    import random
    from database import db
    
    # Sample users
    sample_users = [
        ('john.doe', 'john.doe@company.com', 'John Doe', 'ncr_owner', 'Manufacturing'),
        ('jane.smith', 'jane.smith@company.com', 'Jane Smith', 'qe', 'Quality'),
        ('mike.johnson', 'mike.johnson@company.com', 'Mike Johnson', 'mrb_team', 'Engineering'),
        ('sarah.wilson', 'sarah.wilson@company.com', 'Sarah Wilson', 'admin', 'Management')
    ]
    
    for username, email, full_name, role, dept in sample_users:
        try:
            db.execute_update('''
                INSERT OR IGNORE INTO users (username, email, full_name, role, department, password_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, full_name, role, dept, hash_password('password123')))
        except:
            pass
    
    # Sample NCRs
    sample_ncrs = [
        {
            'title': '13204643-101, LN2 Stack Out of Tolerance',
            'status': 'NEW',
            'nc_level': 2,
            'site': 'Site A',
            'part_number': '13204643-101',
            'project_affected': 'Project Alpha',
            'problem_is': 'LN2 temperature reading shows 15°C instead of target -196°C',
            'problem_should_be': 'LN2 temperature should be maintained at -196°C',
            'problem_category': 'Manufacturing',
            'disposition_action': 'Rework',
            'created_by': 1,
            'quantity_affected': 1,
            'supplier': 'ABC Cryogenics'
        },
        {
            'title': 'PCB-2024-001, Solder Joint Quality Issue',
            'status': 'IN_PROGRESS',
            'nc_level': 3,
            'site': 'Site B', 
            'part_number': 'PCB-2024-001',
            'project_affected': 'Project Beta',
            'problem_is': 'Multiple solder joints showing poor wetting and cold joints',
            'problem_should_be': 'All solder joints should meet IPC-A-610 Class 2 standards',
            'problem_category': 'Manufacturing',
            'disposition_action': 'Repair',
            'created_by': 2,
            'quantity_affected': 25,
            'supplier': 'ElectronicsCorp'
        }
    ]
    
    for ncr_data in sample_ncrs:
        try:
            db.create_ncr(ncr_data)
        except:
            pass

def ensure_directories():
    """Ensure required directories exist"""
    directories = ['uploads', 'exports', 'temp']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def setup_logging():
    """Setup application logging"""
    import logging
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/nctracker.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('NCTracker')

# Global logger
logger = setup_logging()