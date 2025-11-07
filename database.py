"""
NCTracker Database Management Module
Handles all database operations, schema creation, and data management
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
import hashlib


class DatabaseManager:
    def __init__(self, db_path: str = "nctracker.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    role VARCHAR(20) NOT NULL,
                    department VARCHAR(50),
                    password_hash VARCHAR(128) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # NCRs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ncrs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ncr_number VARCHAR(20) UNIQUE NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    status VARCHAR(20) DEFAULT 'NEW',
                    priority INTEGER DEFAULT 3,
                    
                    -- Section 1: NCR Details
                    site VARCHAR(50),
                    part_number VARCHAR(50),
                    part_number_rev VARCHAR(20),
                    quantity_affected INTEGER,
                    units_affected TEXT,
                    project_affected VARCHAR(100),
                    serial_number VARCHAR(50),
                    other_id VARCHAR(50),
                    po_number VARCHAR(50),
                    supplier VARCHAR(100),
                    build_group_operation VARCHAR(100),
                    
                    -- Problem Statement
                    problem_is TEXT,
                    problem_should_be TEXT,
                    
                    -- Containment
                    is_contained BOOLEAN,
                    how_contained TEXT,
                    containment_justification TEXT,
                    
                    -- Section 2: NC Level and CAPA
                    nc_level INTEGER,
                    capa_required BOOLEAN,
                    capa_number VARCHAR(50),
                    qe_assigned BOOLEAN,
                    nc_owner_assigned BOOLEAN,
                    external_notification_required BOOLEAN,
                    external_notification_method TEXT,
                    
                    -- Section 3: Investigation
                    problem_category VARCHAR(50),
                    disposition_action VARCHAR(50),
                    disposition_instructions TEXT,
                    disposition_justification TEXT,
                    required_approvals TEXT,
                    
                    -- Section 4: Correction
                    correction_actions TEXT,
                    evidence_of_completion TEXT,
                    
                    -- Section 5: Closure
                    closure_date DATE,
                    qe_audit_complete BOOLEAN,
                    
                    -- Metadata
                    created_by INTEGER NOT NULL,
                    assigned_to INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    closed_at TIMESTAMP,
                    
                    FOREIGN KEY (created_by) REFERENCES users (id),
                    FOREIGN KEY (assigned_to) REFERENCES users (id)
                )
            ''')
            
            # Comments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ncr_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ncr_id) REFERENCES ncrs (id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Attachments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attachments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ncr_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    filename VARCHAR(255) NOT NULL,
                    file_path VARCHAR(500) NOT NULL,
                    file_size INTEGER,
                    mime_type VARCHAR(100),
                    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ncr_id) REFERENCES ncrs (id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Status history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ncr_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    old_status VARCHAR(20),
                    new_status VARCHAR(20),
                    change_reason TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (ncr_id) REFERENCES ncrs (id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Mentions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mentions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    comment_id INTEGER NOT NULL,
                    mentioned_user_id INTEGER NOT NULL,
                    notified BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (comment_id) REFERENCES comments (id) ON DELETE CASCADE,
                    FOREIGN KEY (mentioned_user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
            
        # Create default admin user if none exists
        self.create_default_admin()
    
    def create_default_admin(self):
        """Create default admin user if no users exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            if user_count == 0:
                admin_password = "admin123"  # Default password - should be changed
                password_hash = hashlib.sha256(admin_password.encode()).hexdigest()
                
                cursor.execute('''
                    INSERT INTO users (username, email, full_name, role, password_hash)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', 'admin@company.com', 'System Administrator', 'admin', password_hash))
                
                conn.commit()
                print("Default admin user created: username='admin', password='admin123'")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Execute a query and return results as list of dictionaries"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute an update/insert query and return last row id"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    
    # User Management
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user info"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        query = '''
            SELECT id, username, email, full_name, role, department, created_at
            FROM users 
            WHERE username = ? AND password_hash = ?
        '''
        
        results = self.execute_query(query, (username, password_hash))
        return results[0] if results else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user information by ID"""
        query = '''
            SELECT id, username, email, full_name, role, department, created_at
            FROM users WHERE id = ?
        '''
        results = self.execute_query(query, (user_id,))
        return results[0] if results else None
    
    def get_all_users(self) -> List[Dict]:
        """Get all users for mentions and assignments"""
        query = '''
            SELECT id, username, full_name, role, department
            FROM users ORDER BY full_name
        '''
        return self.execute_query(query)
    
    # NCR Management
    def create_ncr(self, ncr_data: Dict) -> int:
        """Create a new NCR"""
        # Generate NCR number
        ncr_number = self.generate_ncr_number()
        ncr_data['ncr_number'] = ncr_number
        
        query = '''
            INSERT INTO ncrs (
                ncr_number, title, status, priority, site, part_number, part_number_rev,
                quantity_affected, units_affected, project_affected, serial_number, other_id,
                po_number, supplier, build_group_operation, problem_is, problem_should_be,
                is_contained, how_contained, containment_justification, nc_level, capa_required,
                capa_number, qe_assigned, nc_owner_assigned, external_notification_required,
                external_notification_method, problem_category, disposition_action,
                disposition_instructions, disposition_justification, required_approvals,
                correction_actions, evidence_of_completion, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            ncr_data.get('ncr_number'),
            ncr_data.get('title'),
            ncr_data.get('status', 'NEW'),
            ncr_data.get('priority', 3),
            ncr_data.get('site'),
            ncr_data.get('part_number'),
            ncr_data.get('part_number_rev'),
            ncr_data.get('quantity_affected'),
            ncr_data.get('units_affected'),
            ncr_data.get('project_affected'),
            ncr_data.get('serial_number'),
            ncr_data.get('other_id'),
            ncr_data.get('po_number'),
            ncr_data.get('supplier'),
            ncr_data.get('build_group_operation'),
            ncr_data.get('problem_is'),
            ncr_data.get('problem_should_be'),
            ncr_data.get('is_contained'),
            ncr_data.get('how_contained'),
            ncr_data.get('containment_justification'),
            ncr_data.get('nc_level'),
            ncr_data.get('capa_required'),
            ncr_data.get('capa_number'),
            ncr_data.get('qe_assigned'),
            ncr_data.get('nc_owner_assigned'),
            ncr_data.get('external_notification_required'),
            ncr_data.get('external_notification_method'),
            ncr_data.get('problem_category'),
            ncr_data.get('disposition_action'),
            ncr_data.get('disposition_instructions'),
            ncr_data.get('disposition_justification'),
            json.dumps(ncr_data.get('required_approvals', [])),
            json.dumps(ncr_data.get('correction_actions', [])),
            ncr_data.get('evidence_of_completion'),
            ncr_data.get('created_by')
        )
        
        return self.execute_update(query, params)
    
    def get_ncr_by_id(self, ncr_id: int) -> Optional[Dict]:
        """Get NCR by ID"""
        query = '''
            SELECT n.*, u1.full_name as created_by_name, u2.full_name as assigned_to_name
            FROM ncrs n
            LEFT JOIN users u1 ON n.created_by = u1.id
            LEFT JOIN users u2 ON n.assigned_to = u2.id
            WHERE n.id = ?
        '''
        results = self.execute_query(query, (ncr_id,))
        if results:
            ncr = results[0]
            # Parse JSON fields
            ncr['required_approvals'] = json.loads(ncr.get('required_approvals', '[]'))
            ncr['correction_actions'] = json.loads(ncr.get('correction_actions', '[]'))
            return ncr
        return None
    
    def get_ncrs(self, filters: Dict = None) -> List[Dict]:
        """Get all NCRs with optional filters"""
        query = '''
            SELECT n.*, u1.full_name as created_by_name, u2.full_name as assigned_to_name
            FROM ncrs n
            LEFT JOIN users u1 ON n.created_by = u1.id
            LEFT JOIN users u2 ON n.assigned_to = u2.id
        '''
        
        where_conditions = []
        params = []
        
        if filters:
            if filters.get('status'):
                where_conditions.append('n.status = ?')
                params.append(filters['status'])
            
            if filters.get('nc_level'):
                where_conditions.append('n.nc_level = ?')
                params.append(filters['nc_level'])
            
            if filters.get('created_by'):
                where_conditions.append('n.created_by = ?')
                params.append(filters['created_by'])
            
            if filters.get('search'):
                where_conditions.append('(n.title LIKE ? OR n.part_number LIKE ? OR n.problem_is LIKE ?)')
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term, search_term])
        
        if where_conditions:
            query += ' WHERE ' + ' AND '.join(where_conditions)
        
        query += ' ORDER BY n.created_at DESC'
        
        return self.execute_query(query, tuple(params))
    
    def update_ncr(self, ncr_id: int, update_data: Dict) -> bool:
        """Update NCR data"""
        # Remove fields that shouldn't be updated
        update_data.pop('id', None)
        update_data.pop('ncr_number', None)
        update_data.pop('created_at', None)
        
        # Handle JSON fields
        if 'required_approvals' in update_data:
            update_data['required_approvals'] = json.dumps(update_data['required_approvals'])
        if 'correction_actions' in update_data:
            update_data['correction_actions'] = json.dumps(update_data['correction_actions'])
        
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.now().isoformat()
        
        # Build update query
        set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
        query = f"UPDATE ncrs SET {set_clause} WHERE id = ?"
        
        params = list(update_data.values()) + [ncr_id]
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
    
    def generate_ncr_number(self) -> str:
        """Generate next NCR number"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ncrs")
            count = cursor.fetchone()[0]
            return f"NCR-{count + 1:04d}"
    
    # Comments
    def add_comment(self, ncr_id: int, user_id: int, content: str) -> int:
        """Add comment to NCR"""
        query = '''
            INSERT INTO comments (ncr_id, user_id, content)
            VALUES (?, ?, ?)
        '''
        return self.execute_update(query, (ncr_id, user_id, content))
    
    def get_comments(self, ncr_id: int) -> List[Dict]:
        """Get comments for NCR"""
        query = '''
            SELECT c.*, u.full_name as user_name, u.username
            FROM comments c
            JOIN users u ON c.user_id = u.id
            WHERE c.ncr_id = ?
            ORDER BY c.created_at ASC
        '''
        return self.execute_query(query, (ncr_id,))
    
    # Status History
    def add_status_history(self, ncr_id: int, user_id: int, old_status: str, new_status: str, reason: str = None):
        """Add status change to history"""
        query = '''
            INSERT INTO status_history (ncr_id, user_id, old_status, new_status, change_reason)
            VALUES (?, ?, ?, ?, ?)
        '''
        self.execute_update(query, (ncr_id, user_id, old_status, new_status, reason))
    
    # Attachments
    def add_attachment(self, ncr_id: int, user_id: int, filename: str, file_path: str, file_size: int, mime_type: str):
        """Add file attachment"""
        query = '''
            INSERT INTO attachments (ncr_id, user_id, filename, file_path, file_size, mime_type)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        return self.execute_update(query, (ncr_id, user_id, filename, file_path, file_size, mime_type))
    
    def get_attachments(self, ncr_id: int) -> List[Dict]:
        """Get attachments for NCR"""
        query = '''
            SELECT a.*, u.full_name as user_name
            FROM attachments a
            JOIN users u ON a.user_id = u.id
            WHERE a.ncr_id = ?
            ORDER BY a.uploaded_at DESC
        '''
        return self.execute_query(query, (ncr_id,))
    
    # Analytics
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total NCRs
            cursor.execute("SELECT COUNT(*) FROM ncrs")
            total_ncrs = cursor.fetchone()[0]
            
            # Status breakdown
            cursor.execute("SELECT status, COUNT(*) FROM ncrs GROUP BY status")
            status_counts = dict(cursor.fetchall())
            
            # NC Level breakdown
            cursor.execute("SELECT nc_level, COUNT(*) FROM ncrs WHERE nc_level IS NOT NULL GROUP BY nc_level")
            nc_level_counts = dict(cursor.fetchall())
            
            # Recent NCRs (last 30 days)
            cursor.execute("SELECT COUNT(*) FROM ncrs WHERE created_at >= date('now', '-30 days')")
            recent_ncrs = cursor.fetchone()[0]
            
            # Average resolution time for closed NCRs
            cursor.execute('''
                SELECT AVG(julianday(closed_at) - julianday(created_at)) as avg_days
                FROM ncrs WHERE status = 'CLOSED' AND closed_at IS NOT NULL
            ''')
            avg_resolution = cursor.fetchone()[0] or 0
            
            return {
                'total_ncrs': total_ncrs,
                'status_counts': status_counts,
                'nc_level_counts': nc_level_counts,
                'recent_ncrs': recent_ncrs,
                'avg_resolution_days': round(avg_resolution, 1)
            }


# Global database instance
db = DatabaseManager()