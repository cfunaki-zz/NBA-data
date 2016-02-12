import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.patches import Circle, Rectangle, Arc

directory = "C:/Users/Chris/Documents/Shot charts"
year = 2015

# Read in clean file of all shots
shots = pd.read_csv('%s/NBA data project/processed_shots/shots_%d.csv' % (directory, year))

def draw_court(ax=None, color='black', lw=2, outer_lines=False):
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 18" so it has a radius of 9", which is a value
    # 7.5 in our coordinate system
    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    # Create backboard
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    # The paint
    # Create the outer box 0f the paint, width=16ft, height=19ft
    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    # Create the inner box of the paint, width=12ft, height=19ft
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, 
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the 
    # threes
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,
                           linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,
                           linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                      bottom_free_throw, restricted, corner_three_a, corner_three_b, 
                      three_arc, center_outer_arc, center_inner_arc]

    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

# Find which region a shot location is in
def find_region10(x, y):
    # 0.3971 .9806 2.3812 0.73815
    s1 = 0.3971
    s2 = 0.9806
    s3 = 2.3812
    s4 = (137.5 - (s2*80)) / 80
    
    region = -1
    # inside
    if (x >= -80) and (x <= 80) and (y <= 137.5 + s4*x) and (y <= 137.5 - s4*x):
        region = 1
    # baseline right
    if (x < -80) and (x >= -220) and (y < -s2*x) and (x**2 + y**2 <= 237.5**2):
        region = 2
    # midrange right
    if (x <= 0) and (y >= -s2*x) and (y > 137.5 + s4*x) and (x**2 + y**2 <= 237.5**2):
        region = 3
    # midrange left
    if (x > 0) and (y >= s2*x) and (y > 137.5 - s4*x) and (x**2 + y**2 <= 237.5**2):
        region = 4
    # baseline left
    if (x > 80) and (x <= 220) and (y < s2*x) and (x**2 + y**2 <= 237.5**2):
        region = 5
    # right corner
    if (x < -220) and (y < -s1*x):
        region = 6
    # outside right
    if (y >= -s1*x) and (y < -s3*x) and (x**2 + y**2 > 237.5**2):
        region = 7
    # outside middle
    if (y >= -s3*x) and (y >= s3*x) and (x**2 + y**2 > 237.5**2):
        region = 8
    # outside left
    if (y >= s1*x) and (y < s3*x) and (x**2 + y**2 > 237.5**2):
        region = 9
    # left corner
    if (x > 220) and (y < s1*x):
        region = 10
    return region

# Create grid of points
def point_matrix():
    point_matrix = []
    x = -245
    y = -47.5
    while x < 250:
        temp = pd.DataFrame({'x': [x],
                             'y': [y],
                             'region': [find_region10(x, y)]})
        point_matrix.append(temp)
        y = y + 10
        if y == 312.5:
            y = -47.5
            x = x + 10
    point_matrix = pd.concat(point_matrix, ignore_index=True)
    return point_matrix

def subset_shots(subsetby, filters):
    subset = shots[shots[subsetby].isin(filters)]
    return subset
    
def region_boxes(subset):
    subset = subset.sort(['region'])
    shots_reg = subset.groupby('region').made.count()
    made_reg = subset.groupby('region').made.sum()
    pts_reg = made_reg * subset.groupby('region').ppb.mean()
    fg_reg = made_reg / shots_reg
    pps_reg = pts_reg / shots_reg
    
    all_shots_reg = shots.groupby('region').made.count()
    all_made_reg = shots.groupby('region').made.sum()
    all_fg_reg = all_made_reg / all_shots_reg
    
    region_stats = pd.DataFrame({'region': subset['region'].unique(),
                                 'shots_reg': shots_reg,
                                 'made_reg': made_reg,
                                 'pts_reg': pts_reg,
                                 'fg_reg': fg_reg,
                                 'all_fg_reg': all_fg_reg[subset['region'].unique()],
                                                          'pps_reg': pps_reg})
    boxes = point_matrix()
    
    shots_box = subset.groupby(['x_box', 'y_box']).made.count()
    shots_box = shots_box.reset_index()
    shots_box.columns = ['x', 'y', 'shots']
    
    made_box = subset.groupby(['x_box', 'y_box']).made.sum()
    made_box = made_box.reset_index()
    made_box.columns = ['x', 'y', 'made']
    
    pts_box = made_box['made'] * subset.groupby(['x_box', 'y_box']).ppb.mean().reset_index()['ppb']
    fg_box = made_box['made'] / shots_box['shots']
    pps_box = pts_box / shots_box['shots']
    
    box_stats = pd.DataFrame({'x': shots_box['x'],
                              'y': shots_box['y'],
                              'shots_box': shots_box['shots'],
                              'made_box': made_box['made'],
                              'pts_box': pts_box,
                              'fg_box': fg_box,
                              'pps_box': pps_box})

    # Merge box matrix with the box stats
    boxes = pd.merge(boxes, box_stats, on=['x', 'y'], how='outer')
    # Merge the boxes with the region stats
    boxes = pd.merge(boxes, region_stats, on='region', how='left')
    
    boxes['fg_diff'] = boxes['fg_reg'] - boxes['all_fg_reg']
    boxes['logshots'] = np.log10(boxes['shots_box'] + 1)
    return boxes
    
    
# Choose filtering options for data here
filters = ['LeBron James']
subset = subset_shots('player', filters)
boxes = region_boxes(subset)

def scatter():
    cavg = 0
    crange = 0.1
    plt.scatter(boxes.x, boxes.y, s=boxes.logshots*40, marker='o',
                c=boxes.fg_diff, vmin=cavg-crange, vmax=cavg+crange, edgecolors='none')

    ax = plt.gca()
    draw_court(ax, color='1.0', outer_lines=True)
    ax.patch.set_facecolor('0.4')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(250, -250)
    ax.set_ylim(-47.5, 305)
    
    plt.set_cmap('RdBu_r')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0)
    cb = plt.colorbar(cax=cax)
    cb.set_label('FG%')

def hexplot():
    plt.hexbin(shots.x, shots.y, shots.made, gridsize = 50,
               bins='log',
               reduce_C_function = np.sum)
    ax = plt.gca()
    draw_court(ax, outer_lines=True)
    #ax.patch.set_facecolor('0.2')
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(250, -250)
    ax.set_ylim(-47.5, 340)    
    
    plt.set_cmap('Purples')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0)
    cb = plt.colorbar(cax=cax)
    cb.set_label('log of count')
    
scatter()
#hexplot()
