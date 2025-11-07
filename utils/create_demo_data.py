"""
NCTracker Demo Data Creator
Creates a few sample NCRs to demonstrate app functionality
"""

import random
from datetime import datetime, timedelta
import hashlib
import sqlite3
from database import db

def create_demo_users():
    """Create demo users"""
    demo_users = [
        ('john.doe', 'john.doe@company.com', 'John Doe', 'ncr_owner', 'Manufacturing'),
        ('jane.smith', 'jane.smith@company.com', 'Jane Smith', 'qe', 'Quality'),
        ('mike.johnson', 'mike.johnson@company.com', 'Mike Johnson', 'mrb_team', 'Engineering'),
        ('sarah.wilson', 'sarah.wilson@company.com', 'Sarah Wilson', 'admin', 'Management'),
    ]
    
    password_hash = hashlib.sha256('password123'.encode()).hexdigest()
    
    for username, email, full_name, role, department in demo_users:
        try:
            db.execute_update('''
                INSERT OR IGNORE INTO users (username, email, full_name, role, department, password_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, full_name, role, department, password_hash))
        except Exception as e:
            print(f"Note: User {username} may already exist")

def create_demo_ncrs():
    """Create a few demo NCRs using direct database access"""
    
    # Demo NCR data - simplified
    demo_data = [
        {
            'ncr_number': 'NCR-0001',
            'title': 'PCB-2024-001, Temperature sensor out of range',
            'status': 'CLOSED',
            'priority': 3,
            'site': 'Site A',
            'part_number': 'PCB-2024-001',
            'part_number_rev': 'B2',
            'quantity_affected': 5,
            'units_affected': 'pieces',
            'project_affected': 'Project Alpha',
            'serial_number': 'SN123456',
            'other_id': 'ID1001',
            'po_number': 'PO12345',
            'supplier': 'ABC Components',
            'build_group_operation': 'Build-A-5',
            'problem_is': 'Temperature sensor readings show 25°C instead of target 20°C range',
            'problem_should_be': 'Temperature sensors should maintain readings within 20±2°C specification',
            'is_contained': True,
            'how_contained': 'Affected units segregated and tagged',
            'containment_justification': '',
            'nc_level': 3,
            'capa_required': False,
            'capa_number': '',
            'qe_assigned': True,
            'nc_owner_assigned': True,
            'external_notification_required': False,
            'external_notification_method': '',
            'problem_category': 'Manufacturing',
            'disposition_action': 'Rework',
            'disposition_instructions': 'Recalibrate sensors per procedure PR-001',
            'disposition_justification': 'Rework feasible with acceptable cost and timeline',
            'required_approvals': '["Quality Manager", "Process Engineer"]',
            'correction_actions': '["Process/Procedural Update", "Training"]',
            'evidence_of_completion': 'All sensors recalibrated and verified per specification',
            'closure_date': '2024-11-01',
            'qe_audit_complete': True,
            'created_by': 1,  # Will be updated after users are created
            'assigned_to': None,
            'created_at': '2024-10-15T10:30:00',
            'updated_at': '2024-11-01T14:45:00',
            'closed_at': '2024-11-01T14:45:00'
        },
        {
            'ncr_number': 'NCR-0002', 
            'title': 'IC-555-REV-B, Solder joint quality issue',
            'status': 'IN_PROGRESS',
            'priority': 2,
            'site': 'Site B',
            'part_number': 'IC-555-REV-B',
            'part_number_rev': 'A1',
            'quantity_affected': 25,
            'units_affected': 'pieces',
            'project_affected': 'Project Beta',
            'serial_number': 'SN234567',
            'other_id': 'ID1002',
            'po_number': 'PO23456',
            'supplier': 'TechSupply Inc',
            'build_group_operation': 'Build-B-3',
            'problem_is': 'Multiple solder joints show cold joints and poor wetting on pin connections',
            'problem_should_be': 'All solder joints should meet IPC-A-610 Class 2 standards with proper wetting',
            'is_contained': True,
            'how_contained': 'Production line stopped, affected units quarantined',
            'containment_justification': '',
            'nc_level': 2,
            'capa_required': True,
            'capa_number': 'CAPA-2024-012',
            'qe_assigned': True,
            'nc_owner_assigned': True,
            'external_notification_required': False,
            'external_notification_method': '',
            'problem_category': 'Manufacturing',
            'disposition_action': 'Repair',
            'disposition_instructions': 'Rework solder joints using controlled temperature profile',
            'disposition_justification': 'Repair possible with proper rework procedures',
            'required_approvals': '["Quality Manager", "Process Engineer", "SME"]',
            'correction_actions': '["RCCA/CAPA", "Process/Procedural Update", "Training"]',
            'evidence_of_completion': '',
            'closure_date': None,
            'qe_audit_complete': False,
            'created_by': 2,
            'assigned_to': None,
            'created_at': '2024-11-05T09:15:00',
            'updated_at': '2024-11-06T11:20:00',
            'closed_at': None
        },
        {
            'ncr_number': 'NCR-0003',
            'title': 'ASSY-123-A, Dimension measurement error', 
            'status': 'NEW',
            'priority': 1,
            'site': 'Site A',
            'part_number': 'ASSY-123-A',
            'part_number_rev': 'C3',
            'quantity_affected': 1,
            'units_affected': 'piece',
            'project_affected': 'Project Gamma',
            'serial_number': 'SN345678',
            'other_id': 'ID1003',
            'po_number': 'PO34567',
            'supplier': 'Precision Parts Co',
            'build_group_operation': 'Build-A-1',
            'problem_is': 'Critical mounting hole dimension measured at 12.8mm vs 12.5mm specification',
            'problem_should_be': 'Mounting hole should be 12.5±0.1mm per drawing specification',
            'is_contained': True,
            'how_contained': 'Part isolated, no further processing allowed',
            'containment_justification': '',
            'nc_level': 1,
            'capa_required': True,
            'capa_number': '',
            'qe_assigned': True,
            'nc_owner_assigned': False,
            'external_notification_required': True,
            'external_notification_method': 'Customer notification required per contract',
            'problem_category': 'Supplier',
            'disposition_action': 'Reject - Return to Supplier',
            'disposition_instructions': 'Return to supplier for replacement',
            'disposition_justification': 'Cannot be reworked to meet critical specification',
            'required_approvals': '["Quality Manager", "SME Manager", "Customer Service"]',
            'correction_actions': '["SCAR or Supplier Support", "Process/Procedural Update"]',
            'evidence_of_completion': '',
            'closure_date': None,
            'qe_audit_complete': False,
            'created_by': 3,
            'assigned_to': None,
            'created_at': '2024-11-06T14:30:00',
            'updated_at': '2024-11-06T14:30:00',
            'closed_at': None
        }
    ]
    
    # Get users to assign correctly
    users = db.get_all_users()
    user_map = {user['username']: user['id'] for user in users}
    
    # Update created_by based on username
    username_to_id = {
        'john.doe': 2,  # Will be updated after creation
        'jane.smith': 3,
        'mike.johnson': 4,
        'sarah.wilson': 5
    }
    
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        
        for ncr_data in demo_data:
            try:
                # Insert the NCR
                cursor.execute('''
                    INSERT INTO ncrs (
                        ncr_number, title, status, priority, site, part_number, part_number_rev,
                        quantity_affected, units_affected, project_affected, serial_number, other_id,
                        po_number, supplier, build_group_operation, problem_is, problem_should_be,
                        is_contained, how_contained, containment_justification, nc_level, capa_required,
                        capa_number, qe_assigned, nc_owner_assigned, external_notification_required,
                        external_notification_method, problem_category, disposition_action,
                        disposition_instructions, disposition_justification, required_approvals,
                        correction_actions, evidence_of_completion, closure_date, qe_audit_complete,
                        created_by, assigned_to, created_at, updated_at, closed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    ncr_data['ncr_number'], ncr_data['title'], ncr_data['status'], ncr_data['priority'],
                    ncr_data['site'], ncr_data['part_number'], ncr_data['part_number_rev'],
                    ncr_data['quantity_affected'], ncr_data['units_affected'], ncr_data['project_affected'],
                    ncr_data['serial_number'], ncr_data['other_id'], ncr_data['po_number'], ncr_data['supplier'],
                    ncr_data['build_group_operation'], ncr_data['problem_is'], ncr_data['problem_should_be'],
                    ncr_data['is_contained'], ncr_data['how_contained'], ncr_data['containment_justification'],
                    ncr_data['nc_level'], ncr_data['capa_required'], ncr_data['capa_number'],
                    ncr_data['qe_assigned'], ncr_data['nc_owner_assigned'], ncr_data['external_notification_required'],
                    ncr_data['external_notification_method'], ncr_data['problem_category'], ncr_data['disposition_action'],
                    ncr_data['disposition_instructions'], ncr_data['disposition_justification'],
                    ncr_data['required_approvals'], ncr_data['correction_actions'], ncr_data['evidence_of_completion'],
                    ncr_data['closure_date'], ncr_data['qe_audit_complete'], ncr_data['created_by'],
                    ncr_data['assigned_to'], ncr_data['created_at'], ncr_data['updated_at'], ncr_data['closed_at']
                ))
                print(f"✅ Created {ncr_data['ncr_number']}: {ncr_data['title']}")
                
            except Exception as e:
                print(f"❌ Error creating {ncr_data['ncr_number']}: {e}")
        
        conn.commit()

def main():
    """Create demo data for the application"""
    print("🎯 Creating NCTracker Demo Data...")
    print("=" * 50)
    
    # Create demo users
    print("1. Creating demo users...")
    create_demo_users()
    print("✅ Users created")
    
    # Create demo NCRs
    print("2. Creating demo NCRs...")
    create_demo_ncrs()
    
    # Show final stats
    stats = db.get_dashboard_stats()
    print(f"\n📊 Database Statistics:")
    print(f"   Total NCRs: {stats['total_ncrs']}")
    print(f"   Status breakdown: {stats['status_counts']}")
    print(f"   NC Level breakdown: {stats['nc_level_counts']}")
    
    print(f"\n🎉 Demo data creation completed!")
    print(f"📋 You now have {stats['total_ncrs']} sample NCRs to explore")
    print(f"\n🔐 Login credentials:")
    print(f"   Admin: admin / admin123")
    print(f"   User: john.doe / password123")
    print(f"   User: jane.smith / password123")
    print(f"   User: mike.johnson / password123")
    print(f"   User: sarah.wilson / password123")

if __name__ == "__main__":
    main()