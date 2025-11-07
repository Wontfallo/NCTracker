"""
NCTracker Sample Data Generator
Creates 100 realistic NCRs for testing and demonstration
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
    """Generate realistic sample NCRs"""
    
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
    
    for i in range(count):
        # Random creation date (last 365 days)
        days_ago = random.randint(0, 365)
        created_date = datetime.now() - timedelta(days=days_ago)
        
        # Random user for created_by
        creator = random.choice(users)
        
        # Random status with realistic distribution
        status_weights = {'NEW': 10, 'IN_PROGRESS': 25, 'PENDING_APPROVAL': 15, 'CLOSED': 50}
        status = random.choices(
            list(status_weights.keys()),
            weights=list(status_weights.values())
        )[0]
        
        # NC Level with realistic distribution
        nc_level_weights = [1, 2, 3, 4]
        nc_level_weights_values = [5, 15, 50, 30]
        nc_level = random.choices(
            nc_level_weights,
            weights=nc_level_weights_values
        )[0]
        
        # Generate realistic problem description
        title = random.choice(titles)
        part_number = random.choice(part_numbers)
        is_statement = f"The {part_number} component shows {title.lower()}, with measurements indicating {random.randint(10, 50)}% deviation from specification."
        should_be = f"The {part_number} should meet all {random.choice(['electrical', 'mechanical', 'thermal', 'dimensional'])} specifications within tolerance limits."
        
        ncr_data = {
            'title': f'{part_number}, {title}',
            'status': status,
            'priority': int(nc_level),
            'site': random.choice(sites),
            'part_number': part_number,
            'part_number_rev': random.choice(['A', 'B', 'C', 'D']) + str(random.randint(1, 5)),
            'quantity_affected': random.randint(1, 1000),
            'units_affected': 'pieces',
            'project_affected': random.choice(projects),
            'serial_number': f'SN{random.randint(100000, 999999)}',
            'other_id': f'ID{random.randint(1000, 9999)}',
            'po_number': f'PO{random.randint(10000, 99999)}',
            'supplier': random.choice(suppliers),
            'build_group_operation': f'Build {random.choice(["A", "B", "C"])}-{random.randint(1, 20)}',
            'problem_is': is_statement,
            'problem_should_be': should_be,
            'is_contained': random.choice([True, False]),
            'how_contained': 'Parts segregated and tagged' if random.choice([True, False]) else '',
            'containment_justification': 'Immediate containment not required - low risk level' if random.choice([True, False]) else '',
            'nc_level': int(nc_level),
            'capa_required': nc_level in [1, 2],
            'capa_number': f'CAPA-{random.randint(1000, 9999)}' if nc_level in [1, 2] and random.choice([True, False]) else '',
            'qe_assigned': random.choice([True, False]),
            'nc_owner_assigned': random.choice([True, False]),
            'external_notification_required': nc_level == 1 and random.choice([True, False]),
            'external_notification_method': 'Customer notification via email' if nc_level == 1 and random.choice([True, False]) else '',
            'problem_category': random.choice(problem_categories),
            'disposition_action': random.choice(disposition_actions),
            'disposition_instructions': 'Follow rework procedure WR-001' if random.choice([True, False]) else '',
            'disposition_justification': 'Rework feasible with acceptable risk level' if random.choice([True, False]) else '',
            'required_approvals': [f'Approver {random.randint(1, 5)}'],
            'correction_actions': ['RCCA/CAPA', 'Process/Procedural Update'] if random.choice([True, False]) else ['Disposition Work Only'],
            'evidence_of_completion': 'Corrective actions implemented and verified' if status == 'CLOSED' else '',
            'created_by': creator['id']
        }
        
        try:
            ncr_id = db.create_ncr(ncr_data)
            created_ncrs.append(ncr_id)
            
            # Add some random comments
            if random.choice([True, False]):
                add_sample_comments(ncr_id, users)
            
        except Exception as e:
            print(f"Error creating NCR {i+1}: {e}")
            continue
    
    return created_ncrs

def add_sample_comments(ncr_id, users):
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
            db.add_comment(ncr_id, user['id'], comment)
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