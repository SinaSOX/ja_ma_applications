import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
from datetime import datetime, timedelta

# Set style for cleaner look
plt.style.use('default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(14, 8))

# Define timeline (3 months before launch)
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 4, 1)
total_days = (end_date - start_date).days

# Define main tasks and their timelines
tasks = {
    'Development & Design': {'start': 0, 'duration': 28, 'phase': 'Development'},
    'Localization': {'start': 7, 'duration': 21, 'phase': 'Localization'},
    'Pre-registration Setup': {'start': 21, 'duration': 14, 'phase': 'Marketing'},
    'Gamification System': {'start': 28, 'duration': 21, 'phase': 'Marketing'},
    'Local Events Planning': {'start': 35, 'duration': 21, 'phase': 'Marketing'},
    'Campaign Execution': {'start': 49, 'duration': 35, 'phase': 'Marketing'},
    'Beta Testing': {'start': 70, 'duration': 14, 'phase': 'Development'},
    'Final Preparation': {'start': 84, 'duration': 14, 'phase': 'Launch'},
    'App Store Submission': {'start': 98, 'duration': 7, 'phase': 'Launch'},
    'Launch & Monitoring': {'start': 105, 'duration': 21, 'phase': 'Launch'}
}

# Define colors for different phases
phase_colors = {
    'Development': '#2E86AB',      # Blue
    'Localization': '#A23B72',     # Purple
    'Marketing': '#F18F01',        # Orange
    'Launch': '#C73E1D'            # Red
}

# Y-axis positions for tasks
y_positions = list(range(len(tasks)))
task_names = list(tasks.keys())

# Create the Gantt chart
for i, (task_name, task_info) in enumerate(tasks.items()):
    start_day = task_info['start']
    duration = task_info['duration']
    phase = task_info['phase']
    color = phase_colors[phase]
    
    # Create rectangle for task
    rect = Rectangle((start_day, i-0.3), duration, 0.6, 
                    facecolor=color, edgecolor='white', linewidth=1, alpha=0.8)
    ax.add_patch(rect)
    
    # Add task label
    ax.text(start_day + duration/2, i, task_name, 
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')

# Customize the chart
ax.set_xlim(0, total_days)
ax.set_ylim(-0.5, len(tasks)-0.5)
ax.set_yticks(y_positions)
ax.set_yticklabels(task_names)

# Set x-axis labels (months)
month_labels = ['Jan', 'Feb', 'Mar', 'Apr']
month_positions = [0, 30, 60, 90]

ax.set_xticks(month_positions)
ax.set_xticklabels(month_labels, fontsize=12)

# Add phase separators
phase_boundaries = {
    'Phase 1': 28,
    'Phase 2': 56,
    'Phase 3': 84,
    'Phase 4': 98
}

for phase_name, boundary in phase_boundaries.items():
    ax.axvline(x=boundary, color='gray', linestyle='--', alpha=0.5, linewidth=1)

# Add key milestones
milestones = {
    'Pre-registration': 35,
    'Gamification': 49,
    'Beta Test': 70,
    'Launch': 105
}

for milestone_name, day in milestones.items():
    ax.axvline(x=day, color='red', linestyle='-', linewidth=2, alpha=0.8)
    ax.text(day, -0.8, milestone_name, rotation=90, ha='center', va='top', 
            fontsize=9, fontweight='bold', color='red')

# Add legend
legend_elements = [patches.Patch(color=color, label=phase) 
                  for phase, color in phase_colors.items()]
ax.legend(handles=legend_elements, loc='upper right', framealpha=0.9)

# Add title
plt.title('Iran Market Entry: Publishing Timeline', 
          fontsize=16, fontweight='bold', pad=20)

# Add grid (subtle)
ax.grid(True, alpha=0.2, axis='x')

# Add key metrics box
metrics_text = """Key Goals:
• Pre-registration: 10,000+ users
• Gamification: 60,000+ downloads  
• Local Events: 5,000+ participants
• Budget: 500M Tomans
• ROI Target: 300%+"""

ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))

# Clean up appearance
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Adjust layout and save
plt.tight_layout()
plt.savefig('iran_market_entry_timeline.png', dpi=300, bbox_inches='tight', facecolor='white')
# plt.show()  # Commented out to avoid display window

print("Clean Gantt chart generated successfully!")
print("File saved as: iran_market_entry_timeline.png")

# Print simple summary
print("\n" + "="*50)
print("TIMELINE SUMMARY")
print("="*50)
print("Phase 1 (Weeks 1-4): Development & Localization")
print("Phase 2 (Weeks 5-8): Marketing Setup")
print("Phase 3 (Weeks 9-12): Campaign Execution")
print("Phase 4 (Weeks 13-14): Launch Preparation")
print("Launch Date: April 1, 2024")
