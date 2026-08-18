"""
Smart Hostel Complaint Management System - Analytics Engine
Analyzes complaint data and generates insights
"""

import json
import csv
from datetime import datetime
from collections import defaultdict, Counter
import statistics

class ComplaintAnalytics:
    """Analyzes complaint data and generates analytics."""
    
    def __init__(self, complaints_file):
        self.complaints = self._load_complaints(complaints_file)
        self.analytics_results = {}
    
    def _load_complaints(self, filename):
        """Load complaints from CSV file."""
        complaints = []
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                if row.get('resolution_days'):
                    row['resolution_days'] = int(row['resolution_days'])
                if row.get('satisfaction_score'):
                    row['satisfaction_score'] = float(row['satisfaction_score'])
                if row.get('escalation_count'):
                    row['escalation_count'] = int(row['escalation_count'])
                complaints.append(row)
        return complaints
    
    def analyze_all(self):
        """Run all analytics."""
        self.analytics_results = {
            'summary_statistics': self._summary_statistics(),
            'category_analysis': self._category_analysis(),
            'priority_analysis': self._priority_analysis(),
            'status_analysis': self._status_analysis(),
            'department_analysis': self._department_analysis(),
            'resolution_time_analysis': self._resolution_time_analysis(),
            'satisfaction_analysis': self._satisfaction_analysis(),
            'escalation_analysis': self._escalation_analysis(),
            'warden_performance': self._warden_performance(),
            'temporal_analysis': self._temporal_analysis(),
        }
        return self.analytics_results
    
    def _summary_statistics(self):
        """Generate summary statistics."""
        return {
            'total_complaints': len(self.complaints),
            'submitted': len([c for c in self.complaints if c['status'] == 'Submitted']),
            'assigned': len([c for c in self.complaints if c['status'] == 'Assigned']),
            'in_progress': len([c for c in self.complaints if c['status'] == 'In Progress']),
            'resolved': len([c for c in self.complaints if c['status'] == 'Resolved']),
            'escalated': len([c for c in self.complaints if c['status'] == 'Escalated']),
            'resolution_rate': round(len([c for c in self.complaints if c['status'] == 'Resolved']) / len(self.complaints) * 100, 2),
        }
    
    def _category_analysis(self):
        """Analyze complaints by category."""
        categories = defaultdict(lambda: {'count': 0, 'avg_resolution_time': [], 'avg_satisfaction': []})
        
        for complaint in self.complaints:
            cat = complaint['category']
            categories[cat]['count'] += 1
            
            if complaint['resolution_days']:
                categories[cat]['avg_resolution_time'].append(complaint['resolution_days'])
            if complaint['satisfaction_score']:
                categories[cat]['avg_satisfaction'].append(complaint['satisfaction_score'])
        
        result = {}
        for cat, data in categories.items():
            result[cat] = {
                'count': data['count'],
                'percentage': round(data['count'] / len(self.complaints) * 100, 2),
                'avg_resolution_time': round(statistics.mean(data['avg_resolution_time']), 1) if data['avg_resolution_time'] else None,
                'avg_satisfaction': round(statistics.mean(data['avg_satisfaction']), 2) if data['avg_satisfaction'] else None,
            }
        
        return result
    
    def _priority_analysis(self):
        """Analyze complaints by priority."""
        priorities = Counter(c['priority'] for c in self.complaints)
        return {
            'distribution': dict(priorities),
            'percentages': {p: round(count / len(self.complaints) * 100, 2) for p, count in priorities.items()}
        }
    
    def _status_analysis(self):
        """Analyze complaints by status."""
        statuses = Counter(c['status'] for c in self.complaints)
        return {
            'distribution': dict(statuses),
            'percentages': {s: round(count / len(self.complaints) * 100, 2) for s, count in statuses.items()}
        }
    
    def _department_analysis(self):
        """Analyze complaints by department."""
        departments = defaultdict(lambda: {'count': 0, 'resolved': 0, 'avg_satisfaction': []})
        
        for complaint in self.complaints:
            dept = complaint['assigned_department']
            departments[dept]['count'] += 1
            
            if complaint['status'] == 'Resolved':
                departments[dept]['resolved'] += 1
            if complaint['satisfaction_score']:
                departments[dept]['avg_satisfaction'].append(complaint['satisfaction_score'])
        
        result = {}
        for dept, data in departments.items():
            result[dept] = {
                'total_complaints': data['count'],
                'resolved': data['resolved'],
                'resolution_rate': round(data['resolved'] / data['count'] * 100, 2),
                'avg_satisfaction': round(statistics.mean(data['avg_satisfaction']), 2) if data['avg_satisfaction'] else None,
            }
        
        return result
    
    def _resolution_time_analysis(self):
        """Analyze resolution times."""
        resolved_complaints = [c for c in self.complaints if c['resolution_days']]
        resolution_times = [c['resolution_days'] for c in resolved_complaints]
        
        if not resolution_times:
            return {}
        
        return {
            'average_resolution_time': round(statistics.mean(resolution_times), 1),
            'median_resolution_time': statistics.median(resolution_times),
            'min_resolution_time': min(resolution_times),
            'max_resolution_time': max(resolution_times),
            'std_dev': round(statistics.stdev(resolution_times), 1) if len(resolution_times) > 1 else 0,
            'fast_resolutions_5days': len([t for t in resolution_times if t <= 5]),
            'slow_resolutions_20days': len([t for t in resolution_times if t > 20]),
        }
    
    def _satisfaction_analysis(self):
        """Analyze satisfaction scores."""
        satisfied = [c for c in self.complaints if c['satisfaction_score']]
        satisfaction_scores = [c['satisfaction_score'] for c in satisfied]
        
        if not satisfaction_scores:
            return {}
        
        return {
            'average_satisfaction': round(statistics.mean(satisfaction_scores), 2),
            'median_satisfaction': statistics.median(satisfaction_scores),
            'satisfied_count': len([s for s in satisfaction_scores if s >= 4]),
            'satisfied_percentage': round(len([s for s in satisfaction_scores if s >= 4]) / len(satisfaction_scores) * 100, 2),
            'dissatisfied_count': len([s for s in satisfaction_scores if s <= 2]),
            'dissatisfied_percentage': round(len([s for s in satisfaction_scores if s <= 2]) / len(satisfaction_scores) * 100, 2),
        }
    
    def _escalation_analysis(self):
        """Analyze escalations."""
        escalated = [c for c in self.complaints if c['escalation_count'] > 0]
        escalation_counts = [c['escalation_count'] for c in escalated]
        
        return {
            'total_escalations': sum(escalation_counts),
            'escalated_complaints': len(escalated),
            'escalation_rate': round(len(escalated) / len(self.complaints) * 100, 2),
            'avg_escalations_per_complaint': round(sum(escalation_counts) / len(self.complaints), 2),
        }
    
    def _warden_performance(self):
        """Analyze warden performance."""
        wardens = defaultdict(lambda: {'count': 0, 'resolved': 0, 'avg_satisfaction': []})
        
        for complaint in self.complaints:
            warden = complaint['assigned_warden']
            wardens[warden]['count'] += 1
            
            if complaint['status'] == 'Resolved':
                wardens[warden]['resolved'] += 1
            if complaint['satisfaction_score']:
                wardens[warden]['avg_satisfaction'].append(complaint['satisfaction_score'])
        
        result = {}
        for warden, data in wardens.items():
            result[warden] = {
                'total_complaints': data['count'],
                'resolved': data['resolved'],
                'resolution_rate': round(data['resolved'] / data['count'] * 100, 2),
                'avg_satisfaction': round(statistics.mean(data['avg_satisfaction']), 2) if data['avg_satisfaction'] else None,
            }
        
        return result
    
    def _temporal_analysis(self):
        """Analyze temporal patterns."""
        monthly_complaints = defaultdict(int)
        
        for complaint in self.complaints:
            date_str = complaint['date_submitted']
            if date_str:
                month = date_str[:7]  # YYYY-MM
                monthly_complaints[month] += 1
        
        return {
            'monthly_distribution': dict(sorted(monthly_complaints.items())),
            'peak_month': max(monthly_complaints, key=monthly_complaints.get) if monthly_complaints else None,
            'lowest_month': min(monthly_complaints, key=monthly_complaints.get) if monthly_complaints else None,
        }
    
    def save_analytics(self, filename):
        """Save analytics results to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.analytics_results, f, indent=2)
        print(f"✓ Analytics saved to {filename}")
    
    def get_summary(self):
        """Get summary of analytics."""
        return self.analytics_results


if __name__ == "__main__":
    analytics = ComplaintAnalytics('/home/ubuntu/hostel_complaint_system/data/complaints.csv')
    results = analytics.analyze_all()
    analytics.save_analytics('/home/ubuntu/hostel_complaint_system/data/analytics_results.json')
    print("✓ Analytics completed")
