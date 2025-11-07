"""
NCTracker Advanced Demo Data Generator
Creates 100+ realistic Non-Conformance Report (NCR) records for dashboard demonstration
"""

import random
import sqlite3
import hashlib
from datetime import datetime, timedelta
from database import db
import json

def create_comprehensive_users():
    """Create comprehensive set of demo users with different roles"""
    demo_users = [
        ('john.doe', 'john.doe@company.com', 'John Doe', 'ncr_owner', 'Manufacturing'),
        ('jane.smith', 'jane.smith@company.com', 'Jane Smith', 'qe', 'Quality'),
        ('bob.johnson', 'bob.johnson@company.com', 'Bob Johnson', 'mrb_team', 'Engineering'),
        ('alice.williams', 'alice.williams@company.com', 'Alice Williams', 'ncr_owner', 'Production'),
        ('charlie.brown', 'charlie.brown@company.com', 'Charlie Brown', 'qe', 'Quality'),
        ('david.miller', 'david.miller@company.com', 'David Miller', 'mrb_team', 'Supply Chain'),
        ('emma.davis', 'emma.davis@company.com', 'Emma Davis', 'ncr_owner', 'Maintenance'),
        ('frank.wilson', 'frank.wilson@company.com', 'Frank Wilson', 'admin', 'Management'),
    ]
    
    password_hash = hashlib.sha256('password123'.encode()).hexdigest()
    
    for username, email, full_name, role, department in demo_users:
        try:
            db.execute_update('''
                INSERT OR IGNORE INTO users (username, email, full_name, role, department, password_hash)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, full_name, role, department, password_hash))
        except Exception as e:
            print(f"Note: User {username} may already exist - {e}")

def generate_100_realistic_ncrs():
    """Generate 100+ realistic NCR records with diverse data"""
    
    # Data pools for realistic variation
    statuses = ['NEW', 'IN_PROGRESS', 'PENDING_APPROVAL', 'CLOSED', 'CLOSED', 'CLOSED']  # More closed for realism
    status_weights = [15, 30, 15, 40]  # Distribution percentages
    
    nc_levels = [1, 2, 3, 4]
    nc_level_weights = [5, 15, 50, 30]  # Critical, Adverse, Moderate, Low
    
    departments = ['Manufacturing', 'Quality', 'Engineering', 'Production', 'Supply Chain', 'Maintenance']
    
    sites = ['Site A - Main Facility', 'Site B - Secondary', 'Site C - Assembly', 'Site D - Testing']
    
    # Realistic part number prefixes by type
    part_prefixes = {
        'PCB': ['Board', 'Assembly', 'Main'],
        'IC': ['Chip', 'Controller', 'Processor'],
        'ASSY': ['Sub-assembly', 'Module', 'Unit'],
        'MECH': ['Bracket', 'Housing', 'Mount'],
        'ELEC': ['Cable', 'Connector', 'Harness'],
        'SENS': ['Temperature', 'Pressure', 'Flow']
    }
    
    # Expanded problem categories with subcategories
    problem_categories = {
        'Document': ['Drawing error', 'Spec mismatch', 'Missing documentation'],
        'Design': ['Tolerance issue', 'Material selection', 'Interface problem'],
        'Manufacturing': ['Process deviation', 'Tooling issue', 'Workmanship'],
        'Supplier': ['Quality issue', 'Late delivery', 'Wrong material'],
        'Equipment': ['Calibration', 'Malfunction', 'Setup error'],
        'Process': ['Parameter drift', 'Procedure not followed', 'Training gap'],
        'Software': ['Configuration error', 'Version mismatch', 'Logic flaw'],
        'Customer': ['Requirement change', 'Feedback', 'Complaint']
    }
    
    # Realistic issue titles by category
    issue_templates = {
        'Document': [
            'Drawing dimension tolerance not specified',
            'Bill of materials missing critical component',
            'Work instruction procedure unclear',
            'Specification version mismatch',
            'Change notice not incorporated'
        ],
        'Design': [
            'Hole pattern misalignment in PCB design',
            'Insufficient creepage distance on high voltage traces',
            'Material thermal expansion coefficient incompatible',
            'Connector pin assignment error',
            'Structural stress analysis missing'
        ],
        'Manufacturing': [
            'Solder joint cold solder detected on multiple connections',
            'Surface finish roughness exceeds specification',
            'Component placement offset beyond tolerance',
            'Coating thickness measurement out of range',
            'Assembly torque specification not met'
        ],
        'Supplier': [
            'Incoming inspection found dimensional deviation',
            'Material certificate missing or incomplete',
            'Parts received with cosmetic damage',
            'Wrong revision level components shipped',
            'Supplier quality audit findings require action'
        ],
        'Equipment': [
            'Test equipment calibration overdue',
            'Temperature chamber temperature drift detected',
            'Pick and place machine vision system misalignment',
            'Reflow oven temperature profile outside limits',
            'Measurement instrument accuracy degraded'
        ],
        'Process': [
            'Soldering temperature parameter drift observed',
            'Cleaning process chemical concentration low',
            'Cure time for adhesive not per procedure',
            'Inspection frequency not per work instruction',
            'ESD protocol violation documented'
        ],
        'Software': [
            'Firmware version incompatible with hardware revision',
            'Configuration file parameter incorrect',
            'Software update caused regression in functionality',
            'Embedded code memory overflow issue',
            'Interface protocol timing violation'
        ],
        'Customer': [
            'Customer reported intermittent failure in field',
            'Return merchandise authorization issued for quality',
            'Customer audit finding requires corrective action',
            'Product performance not meeting customer expectation',
            'Field service report indicates design concern'
        ]
    }
    
    disposition_actions = {
        'Rework': 50,  # Most common
        'Repair': 20,
        'Use-As-Is': 15,
        'Reject - Return to Supplier': 10,
        'Reject - Scrap': 5
    }
    
    projects = [
        'Project Alpha - Medical Device', 'Project Beta - Automotive System',
        'Project Gamma - Aerospace Component', 'Project Delta - Industrial Control',
        'Project Epsilon - Consumer Electronics', 'Project Zeta - Defense System',
        'Project Eta - Telecommunications', 'Project Theta - Energy Management'
    ]
    
    suppliers = [
        'ABC Electronics Ltd', 'TechSupply Corporation', 'Precision Manufacturing Inc',
        'Global Components Co', 'Advanced Materials LLC', 'Integrated Systems Ltd',
        'Metro Electronics Corp', 'Prime Manufacturing', 'Vertex Solutions Inc',
        'Quantum Technologies', 'Allied Industries Group', 'Apex Components Ltd'
    ]
    
    # Get users for proper assignment
    users = db.get_all_users()
    if not users or len(users) < 5:
        create_comprehensive_users()
        users = db.get_all_users()
    
    # Separate users by role for realistic assignment
    qe_users = [u for u in users if u['role'] == 'qe']
    ncr_owners = [u for u in users if u['role'] == 'ncr_owner']
    mrb_users = [u for u in users if u['role'] == 'mrb_team']
    all_users = users if users else []
    
    created_count = 0
    failed_count = 0
    
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        
        for i in range(120):  # Generate 120 to ensure we get 100+
            try:
                # Generate NCR number
                cursor.execute("SELECT COUNT(*) FROM ncrs")
                count_existing = cursor.fetchone()[0]
                ncr_number = f"NCR-{count_existing + 1:04d}"
                
                # Random dates - distributed over past 12 months
                days_ago = random.randint(0, 365)
                created_date = datetime.now() - timedelta(days=days_ago)
                
                # Choose status with realistic distribution
                status = random.choices(
                    ['NEW', 'IN_PROGRESS', 'PENDING_APPROVAL', 'CLOSED'],
                    weights=status_weights
                )[0]
                
                # NC level with realistic distribution
                nc_level = random.choices(nc_levels, weights=nc_level_weights)[0]
                
                # Select random category
                category = random.choice(list(problem_categories.keys()))
                subcategory = random.choice(problem_categories[category])
                
                # Generate part number
                part_type = random.choice(list(part_prefixes.keys()))
                part_desc = random.choice(part_prefixes[part_type])
                part_number = f'{part_type}-{random.randint(1000, 9999)}-{random.choice(["A", "B", "C"])}{random.randint(1, 9)}'
                
                # Select issue title
                title = random.choice(issue_templates[category])
                
                # Realistic problem statements
                problem_is = f'{title} - {subcategory}. The {part_number} shows deviation from specification requirements affecting quality standards.'
                problem_should_be = f'The {part_number} should meet all specified requirements within established tolerance limits and quality standards.'
                
                # Assign users based on roles
                creator = random.choice(ncr_owners if ncr_owners else all_users)
                assigned_qe = random.choice(qe_users if qe_users else all_users) if random.random() > 0.3 else None
                
                # Disposition based on NC level
                disposition_action = random.choices(
                    list(disposition_actions.keys()),
                    weights=list(disposition_actions.values())
                )[0]
                
                # Calculate realistic resolution time based on status and NC level
                if status == 'CLOSED':
                    # Higher NC levels take longer to resolve
                    base_days = {1: 45, 2: 30, 3: 15, 4: 7}[nc_level]
                    resolution_days = base_days + random.randint(-5, 15)
                    updated_date = created_date + timedelta(days=random.randint(1, resolution_days // 2))
                    closed_date = created_date + timedelta(days=resolution_days)
                    closure_date_str = closed_date.strftime('%Y-%m-%d')
                    closed_at_str = closed_date.isoformat()
                else:
                    updated_days = random.randint(0, min(days_ago, 30))
                    updated_date = created_date + timedelta(days=updated_days)
                    closure_date_str = None
                    closed_at_str = None
                
                # CAPA required for critical and adverse
                capa_required = nc_level in [1, 2]
                capa_number = f'CAPA-2024-{random.randint(100, 999)}' if capa_required and random.random() > 0.3 else ''
                
                # Build the complete data tuple with all 41 columns
                ncr_data = (
                    ncr_number,  # 1
                    f'{part_number}, {title}',  # 2 - title
                    status,  # 3
                    nc_level,  # 4 - priority
                    random.choice(sites),  # 5 - site
                    part_number,  # 6
                    random.choice(['A', 'B', 'C', 'D']) + str(random.randint(1, 5)),  # 7 - part_number_rev
                    random.randint(1, 500),  # 8 - quantity_affected
                    random.choice(['pieces', 'units', 'assemblies', 'lots']),  # 9 - units_affected
                    random.choice(projects),  # 10 - project_affected
                    f'SN{random.randint(100000, 999999)}',  # 11 - serial_number
                    f'WO-{random.randint(1000, 9999)}',  # 12 - other_id
                    f'PO{random.randint(10000, 99999)}',  # 13 - po_number
                    random.choice(suppliers),  # 14 - supplier
                    f'{random.choice(departments)}-Op{random.randint(10, 50)}',  # 15 - build_group_operation
                    problem_is,  # 16 - problem_is
                    problem_should_be,  # 17 - problem_should_be
                    random.choice([True, False]),  # 18 - is_contained
                    'Parts segregated and quarantined per procedure' if random.choice([True, False]) else '',  # 19 - how_contained
                    'Low risk - immediate containment not required' if random.choice([True, False]) else '',  # 20 - containment_justification
                    nc_level,  # 21 - nc_level
                    capa_required,  # 22 - capa_required
                    capa_number,  # 23 - capa_number
                    True if random.random() > 0.2 else False,  # 24 - qe_assigned
                    True if random.random() > 0.3 else False,  # 25 - nc_owner_assigned
                    nc_level == 1 and random.choice([True, False]),  # 26 - external_notification_required
                    'Customer notification per contract requirement' if nc_level == 1 and random.choice([True, False]) else '',  # 27
                    category,  # 28 - problem_category
                    disposition_action,  # 29 - disposition_action
                    f'Follow procedure {random.choice(["WI", "PR", "SOP"])}-{random.randint(100, 999)}' if random.choice([True, False]) else '',  # 30
                    f'{disposition_action} is technically feasible and cost-effective solution' if random.choice([True, False]) else '',  # 31
                    json.dumps([f'Approver-{random.randint(1, 5)}' for _ in range(random.randint(2, 4))]),  # 32 - required_approvals
                    json.dumps(random.sample(['RCCA/CAPA', 'Process Update', 'Training', 'Supplier Action', 'Design Change'], k=random.randint(1, 3))),  # 33
                    'Corrective actions completed and verified effective' if status == 'CLOSED' else '',  # 34 - evidence_of_completion
                    closure_date_str,  # 35 - closure_date
                    status == 'CLOSED',  # 36 - qe_audit_complete
                    creator['id'],  # 37 - created_by
                    assigned_qe['id'] if assigned_qe else None,  # 38 - assigned_to
                    created_date.isoformat(),  # 39 - created_at
                    updated_date.isoformat(),  # 40 - updated_at
                    closed_at_str  # 41 - closed_at
                )
                
                # Insert the NCR with all 41 columns
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
                ''', ncr_data)
                
                created_count += 1
                
                # Add realistic comments to some NCRs
                if random.random() > 0.4:  # 60% get comments
                    add_realistic_comments(cursor.lastrowid, users, cursor, status, nc_level)
                
                # Print progress every 20 NCRs
                if created_count % 20 == 0:
                    print(f"   ✅ Created {created_count} NCRs...")
                    
            except Exception as e:
                failed_count += 1
                print(f"   ⚠️ Error on NCR {i+1}: {e}")
                continue
        
        conn.commit()
    
    return created_count, failed_count

def add_realistic_comments(ncr_id, users, cursor, status, nc_level):
    """Add realistic comments based on NCR status and level"""
    
    comment_templates_by_status = {
        'NEW': [
            'NCR initiated. Containment actions being evaluated.',
            'Initial investigation started. Root cause analysis underway.',
            'Parts have been segregated and tagged pending disposition.',
            'Preliminary investigation indicates process parameter deviation.',
            'Quality team notified and investigation assigned.'
        ],
        'IN_PROGRESS': [
            'Root cause analysis in progress. Additional data being collected.',
            'Containment actions implemented. All affected units identified.',
            'Investigation results indicate equipment calibration issue.',
            'Supplier has been contacted regarding material quality concern.',
            'Temporary corrective action implemented pending permanent fix.',
            'CAPA team reviewing for systemic issues.',
            'Engineering analysis confirms design margin adequate for use-as-is.',
            'Process parameters adjusted and verified within specification.'
        ],
        'PENDING_APPROVAL': [
            'Disposition recommendation submitted for MRB review.',
            'CAPA plan developed and submitted for approval.',
            'Engineering analysis complete. Awaiting management approval.',
            'Supplier corrective action plan received and under review.',
            'Use-as-is justification documented with supporting analysis.',
            'Quality Manager approval requested for disposition.',
            'Customer notification prepared pending final approval.',
            'All required approvals documented in system.'
        ],
        'CLOSED': [
            'All corrective actions verified effective.',
            'CAPA completed successfully. Effectiveness verified.',
            'Final disposition implemented. NCR closed.',
            'Follow-up audit confirms corrective actions sustained.',
            'Lessons learned documented for future reference.',
            'Process improvements implemented across all shifts.',
            'Training completed for all affected personnel.',
            'Supplier corrective action verified through audit.',
            'Customer notification completed. Issue resolved.',
            'Quality metrics show sustained improvement.'
        ]
    }
    
    # More comments for higher severity
    num_comments = {1: random.randint(4, 8), 2: random.randint(3, 6), 3: random.randint(2, 4), 4: random.randint(1, 3)}[nc_level]
    
    comments = random.sample(comment_templates_by_status.get(status, comment_templates_by_status['NEW']), 
                           min(num_comments, len(comment_templates_by_status.get(status, []))))
    
    for comment in comments:
        user = random.choice(users)
        comment_date = datetime.now() - timedelta(days=random.randint(1, 30))
        try:
            cursor.execute('''
                INSERT INTO comments (ncr_id, user_id, content, created_at)
                VALUES (?, ?, ?, ?)
            ''', (ncr_id, user['id'], comment, comment_date.isoformat()))
        except:
            pass

def main():
    """Generate comprehensive demo dataset for NCTracker"""
    print("🚀 NCTracker Advanced Demo Data Generator")
    print("=" * 60)
    print("Creating comprehensive dataset for dashboard demonstration...")
    print()
    
    # Step 1: Create users
    print("📋 Step 1: Creating demo users...")
    create_comprehensive_users()
    users = db.get_all_users()
    print(f"   ✅ {len(users)} users ready for assignment")
    print()
    
    # Step 2: Generate NCRs
    print("📊 Step 2: Generating 100+ realistic NCR records...")
    print("   This may take a moment...")
    created, failed = generate_100_realistic_ncrs()
    print()
    
    # Step 3: Show statistics
    stats = db.get_dashboard_stats()
    print("=" * 60)
    print("🎉 DATA GENERATION COMPLETE!")
    print("=" * 60)
    print(f"✅ Successfully created: {created} NCRs")
    if failed > 0:
        print(f"⚠️  Failed to create: {failed} NCRs")
    print()
    print("📈 DASHBOARD STATISTICS:")
    print(f"   Total NCRs in database: {stats['total_ncrs']}")
    print(f"   Status Distribution: {stats['status_counts']}")
    print(f"   NC Level Distribution: {stats['nc_level_counts']}")
    print(f"   Recent NCRs (30 days): {stats['recent_ncrs']}")
    print(f"   Average Resolution Time: {stats['avg_resolution_days']:.1f} days")
    print()
    print("🎯 READY FOR DEMONSTRATION!")
    print("   Launch the application with: streamlit run app.py")
    print()
    print("🔐 LOGIN CREDENTIALS:")
    print("   Admin: admin / admin123")
    print("   Users: john.doe, jane.smith, bob.johnson, alice.williams, charlie.brown")
    print("   Password for all users: password123")
    print("=" * 60)

if __name__ == "__main__":
    main()