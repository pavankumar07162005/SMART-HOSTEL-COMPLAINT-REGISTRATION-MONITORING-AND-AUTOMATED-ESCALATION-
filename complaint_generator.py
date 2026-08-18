"""
Smart Hostel Complaint Management System - Complaint Data Generator
Generates realistic synthetic complaint data for testing and demonstration
"""

import json
import random
from datetime import datetime, timedelta
import csv

class ComplaintDataGenerator:
    """Generates realistic synthetic hostel complaint data."""
    
    def __init__(self, num_complaints=500):
        self.num_complaints = num_complaints
        self.categories = ['Electricity', 'Water Supply', 'Internet', 'Maintenance', 
                          'Cleanliness', 'Security', 'Furniture', 'Plumbing']
        self.priorities = ['Low', 'Medium', 'High', 'Critical']
        self.statuses = ['Submitted', 'Assigned', 'In Progress', 'Resolved', 'Escalated']
        self.departments = ['Electrical', 'Plumbing', 'IT', 'Maintenance', 'Security', 'Housekeeping']
        self.rooms = [f'{floor}{room}' for floor in range(1, 6) for room in range(1, 21)]
        self.wardens = ['Warden_A', 'Warden_B', 'Warden_C', 'Warden_D']
        self.complaints = []
    
    def generate_complaints(self):
        """Generate synthetic complaint data."""
        base_date = datetime.now() - timedelta(days=180)
        
        for i in range(self.num_complaints):
            complaint_date = base_date + timedelta(days=random.randint(0, 180))
            
            category = random.choice(self.categories)
            priority = self._assign_priority(category)
            status = random.choice(self.statuses)
            
            resolution_days = random.randint(1, 30) if status == 'Resolved' else None
            resolution_date = complaint_date + timedelta(days=resolution_days) if resolution_days else None
            
            satisfaction = random.uniform(1, 5) if status == 'Resolved' else None
            
            complaint = {
                'complaint_id': f'COMP{i+1:05d}',
                'student_id': f'STU{random.randint(1000, 9999)}',
                'room_number': random.choice(self.rooms),
                'category': category,
                'priority': priority,
                'status': status,
                'date_submitted': complaint_date.strftime('%Y-%m-%d %H:%M:%S'),
                'date_assigned': (complaint_date + timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%d %H:%M:%S') if status != 'Submitted' else None,
                'date_resolved': resolution_date.strftime('%Y-%m-%d %H:%M:%S') if resolution_date else None,
                'resolution_days': resolution_days,
                'assigned_department': random.choice(self.departments),
                'assigned_warden': random.choice(self.wardens),
                'satisfaction_score': round(satisfaction, 1) if satisfaction else None,
                'description': self._generate_description(category),
                'escalation_count': random.randint(0, 3) if status == 'Escalated' else 0,
            }
            
            self.complaints.append(complaint)
        
        return self.complaints
    
    def _assign_priority(self, category):
        """Assign priority based on category."""
        priority_map = {
            'Security': ['High', 'Critical'],
            'Water Supply': ['High', 'Medium'],
            'Electricity': ['High', 'Medium'],
            'Internet': ['Medium', 'Low'],
            'Maintenance': ['Medium', 'Low'],
            'Cleanliness': ['Medium', 'Low'],
            'Furniture': ['Low', 'Medium'],
            'Plumbing': ['High', 'Medium']
        }
        return random.choice(priority_map.get(category, ['Medium']))
    
    def _generate_description(self, category):
        """Generate complaint description."""
        descriptions = {
            'Electricity': 'Light bulb not working, power outlet faulty, frequent power cuts',
            'Water Supply': 'No water pressure, water leakage, dirty water, water supply interrupted',
            'Internet': 'Slow internet speed, WiFi not connecting, frequent disconnections',
            'Maintenance': 'Door lock broken, window damaged, wall paint peeling',
            'Cleanliness': 'Room not cleaned, bathroom dirty, common area unhygienic',
            'Security': 'Suspicious activity, theft report, security concern',
            'Furniture': 'Bed broken, chair damaged, table unstable',
            'Plumbing': 'Toilet clogged, pipe leakage, drainage issue'
        }
        return descriptions.get(category, 'General maintenance issue')
    
    def save_to_csv(self, filename):
        """Save complaints to CSV file."""
        if not self.complaints:
            self.generate_complaints()
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.complaints[0].keys())
            writer.writeheader()
            writer.writerows(self.complaints)
        
        print(f"✓ Saved {len(self.complaints)} complaints to {filename}")
    
    def save_to_json(self, filename):
        """Save complaints to JSON file."""
        if not self.complaints:
            self.generate_complaints()
        
        with open(filename, 'w') as f:
            json.dump(self.complaints, f, indent=2)
        
        print(f"✓ Saved {len(self.complaints)} complaints to {filename}")


if __name__ == "__main__":
    generator = ComplaintDataGenerator(num_complaints=500)
    complaints = generator.generate_complaints()
    generator.save_to_csv('/home/ubuntu/hostel_complaint_system/data/complaints.csv')
    generator.save_to_json('/home/ubuntu/hostel_complaint_system/data/complaints.json')
    print(f"✓ Generated {len(complaints)} complaints")
