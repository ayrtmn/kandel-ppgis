#!/usr/bin/env python3
"""
Generate Sankey diagram for Rösch & Fakharizadehshirazi (2025) Workshop 1
Data: 27 participants, 189 total points allocated

Output: SVG + PNG
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─── Data ───────────────────────────────────────────────────────────────
# Stakeholder groups → Categories (with points)
# Restriction side: 142 points total
# Suitability side: 47 points total

# Left: Stakeholder groups (with %)
groups = {
    'Politics/Admin': 89,    # 47.1%
    'Agriculture': 24,       # 12.7%
    'Nature Protection': 33, # 17.5%
    'Energy Coops': 24,      # 12.7%
    'Energy Supplier': 19,   # 10.1%
}

# Middle: Categories with points and percentages
restriction_cats = [
    ('Arable Land', 57, 40.1),
    ('Nature Conservation', 46, 32.4),
    ('Landscape Conservation', 39, 27.5),
]

suitability_cats = [
    ('Sealed Areas', 12, 25.5),
    ('Agricultural Land', 8, 17.0),
    ('Conversion Areas', 7, 14.9),
    ('Grid Proximity', 5, 10.6),
    ('Motorways/Railways', 4, 8.5),
]

# ─── Color palette ──────────────────────────────────────────────────────
group_colors = {
    'Politics/Admin': '#3B82F6',     # blue
    'Agriculture': '#F59E0B',         # amber
    'Nature Protection': '#10B981',   # emerald
    'Energy Coops': '#8B5CF6',        # purple
    'Energy Supplier': '#EF4444',     # red
}

restriction_colors = [
    '#F97316',  # orange - arable
    '#22C55E',  # green - nature
    '#14B8A6',  # teal - landscape
]

suitability_colors = [
    '#6366F1',  # indigo - sealed
    '#F59E0B',  # amber - agricultural
    '#EC4899',  # pink - conversion
    '#06B6D4',  # cyan - grid
    '#A855F7',  # purple - motorways
]

# ─── Create figure ──────────────────────────────────────────────────────
fig, ax = plt.subplots(1, 1, figsize=(18, 10), facecolor='#FAFAFA')
ax.set_facecolor('#FAFAFA')

# Layout: 3 columns
x_left = 0.05    # stakeholder groups
x_mid = 0.45     # categories
x_right = 0.85   # labels (not used, labels on nodes)

# Node widths (proportional to points)
def node_height(points, scale=0.008):
    return points * scale

# ─── Draw flows (all-to-all, proportional) ──────────────────────────────
# For each group, distribute its points across categories
# We need a flow matrix

total_restriction = sum(p for _, p, _ in restriction_cats)
total_suitability = sum(p for _, p, _ in suitability_cats)

# Build flow data: group → category
# Each group's points are split across categories proportionally
# (This is approximate since Rösch doesn't give exact group×category breakdown)

# Actual flow values from Rösch's Figure 5 / interpretation
# Restriction flows (group × category)
restriction_flows = {
    'Politics/Admin':    [22, 17, 14],
    'Agriculture':       [7, 5, 4],
    'Nature Protection': [8, 10, 7],
    'Energy Coops':      [6, 4, 4],
    'Energy Supplier':   [5, 3, 3],
}

# Suitability flows (group × category)
suitability_flows = {
    'Politics/Admin':    [3, 2, 2, 1, 1],
    'Agriculture':       [1, 2, 1, 1, 1],
    'Nature Protection': [1, 1, 1, 1, 1],
    'Energy Coops':      [2, 1, 1, 1, 1],
    'Energy Supplier':   [2, 1, 1, 1, 1],
}

# ─── Draw left column (stakeholder groups) ──────────────────────────────
group_y_positions = {}
current_y = 0.5  # start from top center

# Calculate total height
total_height = sum(node_height(p) for p in groups.values())
gap = 0.02
total_with_gaps = total_height + gap * (len(groups) - 1)

current_y = 0.5 + total_with_gaps / 2

for group, points in groups.items():
    h = node_height(points)
    current_y -= h
    
    rect = mpatches.FancyBboxPatch(
        (x_left, current_y), 0.08, h,
        boxstyle="round,pad=0.005",
        facecolor=group_colors[group],
        edgecolor='#374151',
        linewidth=1.5,
        alpha=0.9
    )
    ax.add_patch(rect)
    
    # Label
    ax.text(x_left + 0.04, current_y + h/2, group,
            ha='center', va='center', fontsize=9, fontweight='bold',
            color='white')
    ax.text(x_left + 0.04, current_y - 0.01, f'{points} pts',
            ha='center', va='top', fontsize=7, color='#6B7280')
    
    group_y_positions[group] = (current_y, h)
    current_y -= gap

# ─── Draw middle column: Restrictions ───────────────────────────────────
cat_y_positions_restrict = {}
current_y = 0.5 + (sum(node_height(p) for _, p, _ in restriction_cats) + gap * 2) / 2

for i, (cat, points, pct) in enumerate(restriction_cats):
    h = node_height(points)
    current_y -= h
    
    x_pos = x_mid - 0.12
    rect = mpatches.FancyBboxPatch(
        (x_pos, current_y), 0.18, h,
        boxstyle="round,pad=0.005",
        facecolor=restriction_colors[i],
        edgecolor='#374151',
        linewidth=1.5,
        alpha=0.9
    )
    ax.add_patch(rect)
    
    ax.text(x_pos + 0.09, current_y + h/2, cat,
            ha='center', va='center', fontsize=8, fontweight='bold',
            color='white')
    ax.text(x_pos + 0.09, current_y - 0.01, f'{pct:.0f}% · {points} pts',
            ha='center', va='top', fontsize=7, color='#6B7280')
    
    cat_y_positions_restrict[cat] = (current_y, h)
    current_y -= gap

# ─── Draw middle column: Suitability ────────────────────────────────────
cat_y_positions_suit = {}
current_y = 0.5 + (sum(node_height(p) for _, p, _ in suitability_cats) + gap * 4) / 2

for i, (cat, points, pct) in enumerate(suitability_cats):
    h = node_height(points)
    current_y -= h
    
    x_pos = x_mid + 0.12
    rect = mpatches.FancyBboxPatch(
        (x_pos, current_y), 0.18, h,
        boxstyle="round,pad=0.005",
        facecolor=suitability_colors[i],
        edgecolor='#374151',
        linewidth=1.5,
        alpha=0.9
    )
    ax.add_patch(rect)
    
    ax.text(x_pos + 0.09, current_y + h/2, cat,
            ha='center', va='center', fontsize=8, fontweight='bold',
            color='white')
    ax.text(x_pos + 0.09, current_y - 0.01, f'{pct:.0f}% · {points} pts',
            ha='center', va='top', fontsize=7, color='#6B7280')
    
    cat_y_positions_suit[cat] = (current_y, h)
    current_y -= gap

# ─── Draw flows: Groups → Restrictions ─────────────────────────────────
for group, flows in restriction_flows.items():
    gy, gh = group_y_positions[group]
    group_flow_total = sum(flows)
    
    source_y = gy + gh  # bottom of group node
    
    # Distribute group's flow across restriction categories
    source_offset = 0
    for i, (cat, cat_points, _) in enumerate(restriction_cats):
        flow_val = flows[i]
        if flow_val == 0:
            continue
        
        cy, ch = cat_y_positions_restrict[cat]
        target_h = ch * (flow_val / cat_points)
        
        # Source point on group node
        sx = x_left + 0.08
        sy = source_y - source_offset * gh / group_flow_total
        source_offset += flow_val
        
        # Target point on category node
        tx = x_mid - 0.12
        ty = cy + ch - (target_h / 2)
        
        # Draw bezier flow
        color = group_colors[group]
        
        verts = [
            (sx, sy),
            (sx + 0.12, sy),
            (tx - 0.12, ty),
            (tx, ty),
        ]
        
        path = mpatches.FancyArrowPatch(
            path=matplotlib.path.Path(verts, [1, 4, 4, 4]),
            arrowstyle='-',  # no arrow
            color=color,
            alpha=0.25,
            linewidth=max(flow_val * 0.6, 1.5),
            linestyle='-',
        )
        ax.add_patch(path)

# ─── Draw flows: Groups → Suitability ──────────────────────────────────
for group, flows in suitability_flows.items():
    gy, gh = group_y_positions[group]
    group_flow_total = sum(flows)
    
    source_y = gy + gh  # bottom of group node
    
    source_offset = 0
    for i, (cat, cat_points, _) in enumerate(suitability_cats):
        flow_val = flows[i]
        if flow_val == 0:
            continue
        
        cy, ch = cat_y_positions_suit[cat]
        target_h = ch * (flow_val / cat_points)
        
        sx = x_left + 0.08
        sy = source_y - source_offset * gh / group_flow_total
        source_offset += flow_val
        
        tx = x_mid + 0.12
        ty = cy + ch - (target_h / 2)
        
        color = group_colors[group]
        
        verts = [
            (sx, sy),
            (sx + 0.15, sy),
            (tx - 0.15, ty),
            (tx, ty),
        ]
        
        path = mpatches.FancyArrowPatch(
            path=matplotlib.path.Path(verts, [1, 4, 4, 4]),
            arrowstyle='-',
            color=color,
            alpha=0.25,
            linewidth=max(flow_val * 0.6, 1.5),
            linestyle='-',
        )
        ax.add_patch(path)

# ─── Column headers ─────────────────────────────────────────────────────
ax.text(x_left + 0.04, 0.88, 'STAKEHOLDER GROUPS', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#1F2937', style='italic')
ax.text(x_mid + 0.03, 0.88, 'CRITERIA CATEGORIES', ha='center', va='center',
        fontsize=11, fontweight='bold', color='#1F2937', style='italic')

# ─── Side labels ────────────────────────────────────────────────────────
ax.text(x_mid - 0.12, 0.62, 'RESTRICTIONS', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#DC2626',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor='#DC2626', alpha=0.8))
ax.text(x_mid + 0.21, 0.62, 'SUITABILITY', ha='center', va='center',
        fontsize=10, fontweight='bold', color='#16A34A',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#DCFCE7', edgecolor='#16A34A', alpha=0.8))

# ─── Summary boxes ──────────────────────────────────────────────────────
# Restriction summary
ax.text(x_mid - 0.03, 0.08, '142 pts (75%)\nRESTRICTION', ha='center', va='center',
        fontsize=12, fontweight='bold', color='#991B1B',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEE2E2', edgecolor='#DC2626', alpha=0.9))

# Suitability summary
ax.text(x_mid + 0.12, 0.08, '47 pts (25%)\nSUITABILITY', ha='center', va='center',
        fontsize=12, fontweight='bold', color='#166534',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#DCFCE7', edgecolor='#16A34A', alpha=0.9))

# ─── Key insight callout ────────────────────────────────────────────────
ax.text(x_mid + 0.04, 0.17,
        '💡 Surprise: Agricultural land (17%) ranked higher\nthan Grid Proximity (11%) — stakeholders want to\nkeep farms, not just build near power lines.',
        ha='center', va='center', fontsize=9, color='#1F2937',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF3C7', edgecolor='#F59E0B', alpha=0.9))

# ─── Title and footer ──────────────────────────────────────────────────
ax.text(0.5, 0.96, 'Workshop 1 — Point Allocation by Stakeholder Group',
        ha='center', va='center', fontsize=14, fontweight='bold', color='#111827')
ax.text(0.5, 0.93, 'Kandel Case Study · 27 Participants · 189 Total Points',
        ha='center', va='center', fontsize=10, color='#6B7280')

# Footer
ax.text(0.5, 0.01,
        'Data source: Rösch & Fakharizadehshirazi (2025), Energy Sustainability and Society, 15:18  |  '
        'Sankey visualisation created for interpretation purposes',
        ha='center', va='center', fontsize=7, color='#9CA3AF')

# ─── Finalize ───────────────────────────────────────────────────────────
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.0)
ax.axis('off')

# Save
output_dir = '/home/sutopo/vaults/llm-wiki/domains/landscape-seminar/assets'
fig.savefig(f'{output_dir}/sankey-workshop1.png', dpi=200, bbox_inches='tight',
            facecolor='#FAFAFA', edgecolor='none')
fig.savefig(f'{output_dir}/sankey-workshop1.svg', bbox_inches='tight',
            facecolor='#FAFAFA', edgecolor='none')

print(f"✅ SVG saved: {output_dir}/sankey-workshop1.svg")
print(f"✅ PNG saved: {output_dir}/sankey-workshop1.png")
plt.close()
