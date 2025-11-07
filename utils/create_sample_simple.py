"""
NCTracker Simple Sample Data Creator
Creates sample data using the existing create_ncr function
"""

import random
from datetime import datetime, timedelta
import hashlib
from database import db

def create_sample_users():
    """Create sample users for testing"""
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
        except Exception as e:
            print(f"Error creating user {username}: {e}")

def create_simple_ncr():
    """Create a simple NCR with minimal required data"""
    
    # Sample data
    part_numbers = ['PCB-2024-001', 'IC-555-REV-B', 'ASSY-123-A', 'CMP-456-C']
    titles = ['Temperature sensor out of range', 'Solder joint quality issue', 'Dimension measurement error', 'Material non-conformance']
    sites = ['Site A', 'Site B', 'Site C']
    projects = ['Project Alpha', 'Project Beta', 'Project Gamma']
    suppliers = ['ABC Components', 'TechSupply Inc', 'Precision Parts Co']
    categories = ['Manufacturing', 'Design', 'Supplier', 'Process']
    dispositions = ['Rework', 'Repair', 'Use-As-Is', 'Reject - Scrap']
    
    # Get users
    users = db.get_all_users()
    if not users:
        create_sample_users()
        users = db.get_all_users()
    
    # Random data selection
    ncr_data = {
        'title': f'{random.choice(part_numbers)}, {random.choice(titles)}',
        'status': random.choice(['NEW', 'IN_PROGRESS', 'PENDING_APPROVAL', 'CLOSED']),
        'priority': random.choice([1, 2, 3, 4]),
        'site': random.choice(sites),
        'part_number': random.choice(part_numbers),
        'part_number_rev': random.choice(['A', 'B', 'C']) + str(random.randint(1, 3)),
        'quantity_affected': random.randint(1, 100),
        'units_affected': 'pieces',
        'project_affected': random.choice(projects),
        'serial_number': f'SN{random.randint(100000, 999999)}',
        'other_id': f'ID{random.randint(1000, 9999)}',
        'po_number': f'PO{random.randint(10000, 99999)}',
        'supplier': random.choice(suppliers),
        'build_group_operation': f'Build-{random.choice(["A", "B", "C"])}-{random.randint(1, 20)}',
        'problem_is': f'The component shows {random.choice(titles).lower()}, exceeding specified tolerance limits.',
        'problem_should_be': 'All components should meet quality specifications within established tolerances.',
        'is_contained': random.choice([True, False]),
        'how_contained': 'Parts segregated in quarantine area' if random.choice([True, False]) else '',
        'containment_justification': '',
        'nc_level': random.choice([1, 2, 3, 4]),
        'capa_required': random.choice([True, False]),
        'capa_number': f'CAPA-{random.randint(1000, 9999)}' if random.choice([True, False]) else '',
        'qe_assigned': random.choice([True, False]),
        'nc_owner_assigned': random.choice([True, False]),
        'external_notification_required': random.choice([True, False]),
        'external_notification_method': 'Customer notification required' if random.choice([True, False]) else '',
        'problem_category': random.choice(categories),
        'disposition_action': random.choice(dispositions),
        'disposition_instructions': 'Follow standard rework procedure' if random.choice([True, False]) else '',
        'disposition_justification': 'Rework is feasible and cost-effective' if random.choice([True, False]) else '',
        'required_approvals': ['Quality Manager', 'Process Engineer'],
        'correction_actions': ['Process Update', 'Training'],
        'evidence_of_completion': 'All corrective actions verified and documented' if random.choice([True, False]) else '',
        'created_by': random.choice(users)['id']
    }
    
    try:
        ncr_id = db.create_ncr(ncr_data)
        return ncr_id
    except Exception as e:
        print(f"Error creating NCR: {e}")
        return None

def main():
    """Create sample data"""
    print("🔄 Creating NCTracker Sample Data...")
    
    # Create sample users
    print("1. Creating sample users...")
    create_sample_users()
    
    # Create sample NCRs
    print("2. Creating 25 sample NCRs...")
    created_count = 0
    for i in range(25):
        ncr_id = create_simple_ncr()
        if ncr_id:
            created_count += 1
            if created_count % 5 == 0:
                print(f"   Created {created_count} NCRs...")
    
    # Get final statistics
    stats = db.get_dashboard_stats()
    print(f"\n✅ Created {created_count} sample NCRs")
    print(f"📊 Total NCRs in database: {stats['total_ncrs']}")
    print(f"📈 Status breakdown: {stats['status_counts']}")
    print(f"🎯 NC Level breakdown: {stats['nc_level_counts']}")
    
    print("\n🎉 Sample data creation completed!")
    print("Default login: admin / admin123")
    print("Sample users created: admin, john.doe, jane.smith, mike.johnson, etc. (password: password123)")

if __name__ == "__main__":
    main()