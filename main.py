"""
Smart Hostel Complaint Management System - Main Application
Orchestrates the complaint management workflow
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from complaint_generator import ComplaintDataGenerator
from complaint_analytics import ComplaintAnalytics
from dashboard_visualizer import DashboardVisualizer

def main():
    """Main application flow."""
    
    print("\n" + "="*70)
    print("SMART HOSTEL COMPLAINT MANAGEMENT SYSTEM")
    print("="*70)
    
    # Step 1: Generate complaint data
    print("\n[1/3] Generating complaint data...")
    generator = ComplaintDataGenerator(num_complaints=500)
    complaints = generator.generate_complaints()
    generator.save_to_csv('/home/ubuntu/hostel_complaint_system/data/complaints.csv')
    generator.save_to_json('/home/ubuntu/hostel_complaint_system/data/complaints.json')
    print(f"✓ Generated {len(complaints)} complaints")
    
    # Step 2: Analyze complaints
    print("\n[2/3] Analyzing complaint data...")
    analytics = ComplaintAnalytics('/home/ubuntu/hostel_complaint_system/data/complaints.csv')
    results = analytics.analyze_all()
    analytics.save_analytics('/home/ubuntu/hostel_complaint_system/data/analytics_results.json')
    
    # Print summary
    summary = results['summary_statistics']
    print(f"✓ Total Complaints: {summary['total_complaints']}")
    print(f"  - Submitted: {summary['submitted']}")
    print(f"  - Assigned: {summary['assigned']}")
    print(f"  - In Progress: {summary['in_progress']}")
    print(f"  - Resolved: {summary['resolved']}")
    print(f"  - Escalated: {summary['escalated']}")
    print(f"  - Resolution Rate: {summary['resolution_rate']}%")
    
    # Step 3: Create visualizations
    print("\n[3/3] Creating dashboard visualizations...")
    visualizer = DashboardVisualizer('/home/ubuntu/hostel_complaint_system/data/analytics_results.json')
    visualizer.create_all_visualizations('/home/ubuntu/hostel_complaint_system/results')
    
    print("\n" + "="*70)
    print("✓ SYSTEM EXECUTION COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\nGenerated Files:")
    print("  - Data: /home/ubuntu/hostel_complaint_system/data/complaints.csv")
    print("  - Analytics: /home/ubuntu/hostel_complaint_system/data/analytics_results.json")
    print("  - Visualizations: /home/ubuntu/hostel_complaint_system/results/*.png")
    print("\n")

if __name__ == "__main__":
    main()
