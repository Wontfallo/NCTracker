"""
NCTracker Sample Data Generator - Simplified Version
Creates 100 realistic NCRs for testing and demonstration using direct SQL
"""

import random
import sqlite3
import hashlib
from datetime import datetime, timedelta
from database import db
import utils

def create_sample_users():
    """Create additional sample users for realistic testing"""
    sample_users = [
        ('john.doe', 'john.doe@company.com', 'John Doe', 'ncr_owner', 'Manufacturing'),
        ('jane.smith', 'jane.smith@company.com', 'Jane Smith', 'qe', 'Quality'),
        ('mike.johnson', 'mike.johnson@company.com', 'Mike Johnson', 'mrb_team', 'Engineering'),
        ('sarah.wilson', 'sarah.wilson@company.com', 'Sarah Wilson', 'admin', 'Management'),
        ('david.brown', 'david.brown@company.com', 'David Brown', 'ncr_owner', 'Assembly'),
        ('lisa.davis', 'lisa.davis@company.com', 'Lisa Davis', 'qe', 'Quality'),
        ('robert.garcia', 'robert.garcia@company.com', 'Robert Garcia', 'mrb_team', 'Process'),
        ('amanda.miller', 'amanda.miller@company.com', 'Amanda Miller', 'ncr_owner', 'Testing'),
        ('james.taylor', 'james.taylor@company.com', 'James Taylor', 'qe', 'Quality'),
        ('emily.anderson', 'emily.anderson@company.com', 'Emily Anderson', 'mrb_team', 'Design')
    ]
    
    password_hash = hashlib.sha256('password123'.encode()).hexdigest()
    
    for username, email, full_name, role, department in sample_users:
        try:
            db.execute_update('''
                INSERT OR IGNORE INTO users (username, email, full_name, role, department, password_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, full_name, role, department, password_hash))
        except:
            pass

def generate_sample_ncrs(count=100):
    """Generate realistic sample NCRs using direct SQL"""
    
    # Sample data pools for realistic variation
    sites = ['Site A', 'Site B', 'Site C', 'Site D']
    part_prefixes = ['PCB', 'IC', 'ASSY', 'BRD', 'CMP', 'WLD', 'PNL']
    part_numbers = [
        f'{random.choice(part_prefixes)}-{random.randint(1000, 9999)}-{random.choice(["A", "B", "C", "D"])}{random.randint(10, 99)}'
        for _ in range(50)
    ]
    
    projects = [
        'Project Alpha', 'Project Beta', 'Project Gamma', 'Project Delta',
        'Aerospace Platform', 'Medical Device', 'Automotive System', 'Industrial Control',
        'Consumer Electronics', 'Telecommunications', 'Defense System', 'Energy Management'
    ]
    
    suppliers = [
        'ABC Components Ltd', 'TechSupply Inc', 'Precision Parts Co', 'Global Manufacturing',
        'Electronics Corp', 'Allied Industries', 'Vertex Solutions', 'Quantum Electronics',
        'Metro Systems', 'Prime Components', 'Advanced Materials', 'Integrated Circuits Inc'
    ]
    
    problem_categories = [
        'Document', 'Design', 'Manufacturing', 'Supplier', 'Equipment',
        'Customer', 'Process', 'Improvement', 'Software', 'Service', 'Other'
    ]
    
    disposition_actions = [
        'Rework', 'Repair', 'Reject - Return to Supplier', 'Reject - Scrap', 'Use-As-Is'
    ]
    
    titles = [
        'Temperature sensor calibration out of range',
        'Solder joint quality - cold joints detected',
        'PCB trace width non-conformance',
        'Dimension measurement outside tolerance',
        'Surface finish roughness excessive',
        'Missing component on assembly',
        'Wrong material used in fabrication',
        'Test procedure not followed',
        'Label printing misalignment',
        'Packaging damage during transport',
        'Inspection criteria not met',
        'Software configuration error',
        'Firmware version mismatch',
        'Quality documentation incomplete',
        'Supplier quality audit findings',
        'Process parameter drift',
        'Tooling wear beyond limits',
        'Calibration due date missed',
        'Training record missing',
        'Change control not followed'
    ]
    
    users = db.get_all_users()
    if not users:
        create_sample_users()
        users = db.get_all_users()
    
    created_ncrs = []
    
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        
        for i in range(count):
            try:
                # Generate NCR number
                cursor.execute("SELECT COUNT(*) FROM ncrs")
                count_existing = cursor.fetchone()[0]
                ncr_number = f"NCR-{count_existing + 1:04d}"
                
                # Random creation date (last 365 days)
                days_ago = random.randint(0, 365)
                created_date = datetime.now() - timedelta(days=days_ago)
                
                # Random user for created_by
                creator = random.choice(users)
                
                # Random status with realistic distribution
                status_options = ['NEW', 'IN_PROGRESS', 'PENDING_APPROVAL', 'CLOSED']
                status_weights = [10, 25, 15, 50]
                status = random.choices(status_options, weights=status_weights)[0]
                
                # NC Level with realistic distribution
                nc_level = random.choices([1, 2, 3, 4], weights=[5, 15, 50, 30])[0]
                
                # Generate realistic problem description
                title = random.choice(titles)
                part_number = random.choice(part_numbers)
                is_statement = f"The {part_number} component shows {title.lower()}, with measurements indicating {random.randint(10, 50)}% deviation from specification."
                should_be = f"The {part_number} should meet all {random.choice(['electrical', 'mechanical', 'thermal', 'dimensional'])} specifications within tolerance limits."
                
                # Prepare the data
                ncr_data = (
                    ncr_number,  # ncr_number
                    f'{part_number}, {title}',  # title
                    status,  # status
                    nc_level,  # priority
                    random.choice(sites),  # site
                    part_number,  # part_number
                    random.choice(['A', 'B', 'C', 'D']) + str(random.randint(1, 5)),  # part_number_rev
                    random.randint(1, 1000),  # quantity_affected
                    'pieces',  # units_affected
                    random.choice(projects),  # project_affected
                    f'SN{random.randint(100000, 999999)}',  # serial_number
                    f'ID{random.randint(1000, 9999)}',  # other_id
                    f'PO{random.randint(10000, 99999)}',  # po_number
                    random.choice(suppliers),  # supplier
                    f'Build {random.choice(["A", "B", "C"])}-{random.randint(1, 20)}',  # build_group_operation
                    is_statement,  # problem_is
                    should_be,  # problem_should_be
                    random.choice([True, False]),  # is_contained
                    'Parts segregated and tagged' if random.choice([True, False]) else '',  # how_contained
                    'Immediate containment not required - low risk level' if random.choice([True, False]) else '',  # containment_justification
                    nc_level,  # nc_level
                    nc_level in [1, 2],  # capa_required
                    f'CAPA-{random.randint(1000, 9999)}' if nc_level in [1, 2] and random.choice([True, False]) else '',  # capa_number
                    random.choice([True, False]),  # qe_assigned
                    random.choice([True, False]),  # nc_owner_assigned
                    nc_level == 1 and random.choice([True, False]),  # external_notification_required
                    'Customer notification via email' if nc_level == 1 and random.choice([True, False]) else '',  # external_notification_method
                    random.choice(problem_categories),  # problem_category
                    random.choice(disposition_actions),  # disposition_action
                    'Follow rework procedure WR-001' if random.choice([True, False]) else '',  # disposition_instructions
                    'Rework feasible with acceptable risk level' if random.choice([True, False]) else '',  # disposition_justification
                    '["Approver 1", "Approver 2"]',  # required_approvals (JSON)
                    '["RCCA/CAPA", "Process/Procedural Update"]' if random.choice([True, False]) else '["Disposition Work Only"]',  # correction_actions (JSON)
                    'Corrective actions implemented and verified' if status == 'CLOSED' else '',  # evidence_of_completion
                    None,  # closure_date
                    status == 'CLOSED',  # qe_audit_complete
                    creator['id'],  # created_by
                    None,  # assigned_to
                    created_date.isoformat(),  # created_at
                    created_date.isoformat(),  # updated_at
                    None  # closed_at
                )
                
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
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', ncr_data)
                
                created_ncrs.append(cursor.lastrowid)
                
                # Add some random comments
                if random.choice([True, False]):
                    add_sample_comments(cursor.lastrowid, users, cursor)
                
            except Exception as e:
                print(f"Error creating NCR {i+1}: {e}")
                continue
        
        conn.commit()
    
    return created_ncrs

def add_sample_comments(ncr_id, users, cursor):
    """Add realistic sample comments to an NCR"""
    comment_templates = [
        "Investigation underway. Root cause analysis in progress.",
        "Containment actions implemented. Parts segregated.",
        "CAPA initiated for prevention of recurrence.",
        "Supplier has been notified and corrective action requested.",
        "Rework instructions have been issued to production.",
        "Additional testing required before disposition approval.",
        "Quality Manager approval obtained for use-as-is disposition.",
        "Customer has been notified per escalation procedure.",
        "Process change implemented to prevent recurrence.",
        "Training scheduled for affected personnel.",
        "Supplier audit scheduled to verify corrective actions.",
        "Documentation updated to reflect process changes.",
        "Follow-up inspection scheduled for next week.",
        "Preventive maintenance completed on affected equipment.",
        "Material traceability verified - no impact to other lots.",
        "Design review scheduled to address the issue.",
        "Procurement investigating alternative suppliers.",
        "Calibration verified - equipment not at fault.",
        "Customer impact assessment completed.",
        "Lessons learned documented for future reference."
    ]
    
    num_comments = random.randint(0, 5)
    for _ in range(num_comments):
        comment = random.choice(comment_templates)
        user = random.choice(users)
        try:
            cursor.execute('''
                INSERT INTO comments (ncr_id, user_id, content, created_at)
                VALUES (?, ?, ?, ?)
            ''', (ncr_id, user['id'], comment, datetime.now().isoformat()))
        except:
            pass

def main():
    """Main function to create sample database"""
    print("🔄 Creating NCTracker Sample Database...")
    print("=" * 50)
    
    # Create sample users
    print("1. Creating sample users...")
    create_sample_users()
    print("✅ Users created")
    
    # Generate sample NCRs
    print("2. Generating 100 sample NCRs...")
    ncrs = generate_sample_ncrs(100)
    print(f"✅ Created {len(ncrs)} NCRs")
    
    # Get final statistics
    stats = db.get_dashboard_stats()
    print("\n📊 Final Database Statistics:")
    print(f"   Total NCRs: {stats['total_ncrs']}")
    print(f"   Status breakdown: {stats['status_counts']}")
    print(f"   NC Level breakdown: {stats['nc_level_counts']}")
    print(f"   Recent NCRs (30 days): {stats['recent_ncrs']}")
    
    print("\n🎉 Sample database creation completed!")
    print("You can now start the application and explore with realistic data.")
    print("\nDefault login: admin / admin123")
    print("Sample users: See user management page")

if __name__ == "__main__":
    main()