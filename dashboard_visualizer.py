"""
Smart Hostel Complaint Management System - Dashboard Visualizer
Creates professional visualizations for the complaint management dashboard
"""

import matplotlib.pyplot as plt
import seaborn as sns
import json
from collections import Counter

class DashboardVisualizer:
    """Creates professional dashboard visualizations."""
    
    def __init__(self, analytics_file):
        with open(analytics_file, 'r') as f:
            self.analytics = json.load(f)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['font.size'] = 10
    
    def create_category_distribution(self, output_file):
        """Create category distribution pie chart."""
        categories = self.analytics['category_analysis']
        labels = list(categories.keys())
        sizes = [categories[cat]['count'] for cat in labels]
        
        fig, ax = plt.subplots(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(labels)))
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                            colors=colors, startangle=90)
        
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
        
        ax.set_title('Complaint Distribution by Category', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Category distribution chart saved: {output_file}")
    
    def create_priority_distribution(self, output_file):
        """Create priority distribution bar chart."""
        priorities = self.analytics['priority_analysis']['distribution']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#ff6b6b', '#ee5a6f', '#ffa500', '#4ecdc4']
        bars = ax.bar(priorities.keys(), priorities.values(), color=colors[:len(priorities)])
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_xlabel('Priority Level', fontsize=12, fontweight='bold')
        ax.set_ylabel('Number of Complaints', fontsize=12, fontweight='bold')
        ax.set_title('Complaint Distribution by Priority', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Priority distribution chart saved: {output_file}")
    
    def create_status_distribution(self, output_file):
        """Create status distribution chart."""
        statuses = self.analytics['status_analysis']['distribution']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#95e1d3', '#f38181', '#aa96da', '#fcbad3', '#a8d8ea']
        bars = ax.barh(list(statuses.keys()), list(statuses.values()), color=colors[:len(statuses)])
        
        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f'{int(width)}',
                   ha='left', va='center', fontweight='bold', fontsize=11)
        
        ax.set_xlabel('Number of Complaints', fontsize=12, fontweight='bold')
        ax.set_title('Complaint Status Distribution', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Status distribution chart saved: {output_file}")
    
    def create_department_performance(self, output_file):
        """Create department performance chart."""
        departments = self.analytics['department_analysis']
        dept_names = list(departments.keys())
        resolution_rates = [departments[d]['resolution_rate'] for d in dept_names]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ['#2ecc71' if rate >= 25 else '#f39c12' if rate >= 20 else '#e74c3c' 
                  for rate in resolution_rates]
        bars = ax.bar(dept_names, resolution_rates, color=colors)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Resolution Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Department Performance - Resolution Rate', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, max(resolution_rates) * 1.15)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Department performance chart saved: {output_file}")
    
    def create_resolution_time_analysis(self, output_file):
        """Create resolution time distribution chart."""
        res_time = self.analytics['resolution_time_analysis']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        metrics = ['Average', 'Median', 'Min', 'Max']
        values = [res_time['average_resolution_time'], res_time['median_resolution_time'],
                 res_time['min_resolution_time'], res_time['max_resolution_time']]
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
        
        bars = ax.bar(metrics, values, color=colors)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)} days',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Days', fontsize=12, fontweight='bold')
        ax.set_title('Resolution Time Analysis', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Resolution time chart saved: {output_file}")
    
    def create_satisfaction_analysis(self, output_file):
        """Create satisfaction score distribution."""
        sat = self.analytics['satisfaction_analysis']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Satisfied\n(≥4)', 'Neutral\n(2-3)', 'Dissatisfied\n(≤2)']
        values = [sat['satisfied_count'], 
                 sat.get('neutral_count', 0),
                 sat['dissatisfied_count']]
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        
        bars = ax.bar(categories, values, color=colors)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Number of Complaints', fontsize=12, fontweight='bold')
        ax.set_title('Satisfaction Score Distribution', fontsize=14, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Satisfaction analysis chart saved: {output_file}")
    
    def create_escalation_analysis(self, output_file):
        """Create escalation analysis chart."""
        esc = self.analytics['escalation_analysis']
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        metrics = ['Total Escalations', 'Escalated Complaints', 'Escalation Rate (%)']
        values = [esc['total_escalations'], esc['escalated_complaints'], esc['escalation_rate']]
        colors = ['#e74c3c', '#e67e22', '#c0392b']
        
        # Create bars with different scales
        ax2 = ax.twinx()
        
        bars1 = ax.bar([0, 1], values[:2], color=colors[:2], alpha=0.7, width=0.6)
        bars2 = ax2.bar([2], [values[2]], color=colors[2], alpha=0.7, width=0.6)
        
        ax.set_ylabel('Count', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
        ax.set_title('Escalation Analysis', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks([0, 1, 2])
        ax.set_xticklabels(metrics)
        
        # Add value labels
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontweight='bold')
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Escalation analysis chart saved: {output_file}")
    
    def create_warden_performance(self, output_file):
        """Create warden performance comparison."""
        wardens = self.analytics['warden_performance']
        warden_names = list(wardens.keys())
        resolution_rates = [wardens[w]['resolution_rate'] for w in warden_names]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.viridis(range(len(warden_names)))
        bars = ax.bar(warden_names, resolution_rates, color=colors)
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Resolution Rate (%)', fontsize=12, fontweight='bold')
        ax.set_title('Warden Performance - Resolution Rate', fontsize=14, fontweight='bold', pad=20)
        ax.set_ylim(0, max(resolution_rates) * 1.15)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Warden performance chart saved: {output_file}")
    
    def create_system_architecture(self, output_file):
        """Create system architecture diagram."""
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'Smart Hostel Complaint Management System Architecture', 
               ha='center', fontsize=14, fontweight='bold')
        
        # Components
        components = [
            {'pos': (2, 7.5), 'label': 'Student Portal', 'color': '#3498db'},
            {'pos': (5, 7.5), 'label': 'Admin Dashboard', 'color': '#2ecc71'},
            {'pos': (8, 7.5), 'label': 'Mobile App', 'color': '#e74c3c'},
            
            {'pos': (1.5, 5), 'label': 'Complaint\nRegistration', 'color': '#f39c12'},
            {'pos': (3.5, 5), 'label': 'Escalation\nEngine', 'color': '#9b59b6'},
            {'pos': (5.5, 5), 'label': 'Notification\nService', 'color': '#1abc9c'},
            {'pos': (7.5, 5), 'label': 'Analytics\nEngine', 'color': '#34495e'},
            
            {'pos': (5, 2), 'label': 'Database\n(Complaints & Users)', 'color': '#c0392b'},
        ]
        
        for comp in components:
            x, y = comp['pos']
            rect = plt.Rectangle((x-0.8, y-0.4), 1.6, 0.8, 
                                 facecolor=comp['color'], edgecolor='black', linewidth=2, alpha=0.7)
            ax.add_patch(rect)
            ax.text(x, y, comp['label'], ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='white')
        
        # Draw connections
        connections = [
            ((2, 7.1), (2, 5.4)),
            ((5, 7.1), (5, 5.4)),
            ((8, 7.1), (8, 5.4)),
            ((2, 4.6), (5, 2.4)),
            ((5, 4.6), (5, 2.4)),
            ((8, 4.6), (5, 2.4)),
        ]
        
        for start, end in connections:
            ax.arrow(start[0], start[1], end[0]-start[0], end[1]-start[1],
                    head_width=0.15, head_length=0.1, fc='gray', ec='gray', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ System architecture diagram saved: {output_file}")
    
    def create_all_visualizations(self, output_dir):
        """Create all visualizations."""
        self.create_category_distribution(f'{output_dir}/category_distribution.png')
        self.create_priority_distribution(f'{output_dir}/priority_distribution.png')
        self.create_status_distribution(f'{output_dir}/status_distribution.png')
        self.create_department_performance(f'{output_dir}/department_performance.png')
        self.create_resolution_time_analysis(f'{output_dir}/resolution_time_analysis.png')
        self.create_satisfaction_analysis(f'{output_dir}/satisfaction_analysis.png')
        self.create_escalation_analysis(f'{output_dir}/escalation_analysis.png')
        self.create_warden_performance(f'{output_dir}/warden_performance.png')
        self.create_system_architecture(f'{output_dir}/system_architecture.png')
        print("✓ All visualizations created successfully")


if __name__ == "__main__":
    visualizer = DashboardVisualizer('/home/ubuntu/hostel_complaint_system/data/analytics_results.json')
    visualizer.create_all_visualizations('/home/ubuntu/hostel_complaint_system/results')
