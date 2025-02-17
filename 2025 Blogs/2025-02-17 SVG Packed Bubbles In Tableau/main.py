import random
import math
import os
from svgpathtools import svg2paths
import xml.etree.ElementTree as ET
import csv

def parse_svg(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    paths, attributes = svg2paths(file_path)
    
    if not paths:
        raise ValueError("No path found in SVG file")
    
    boundaries = []
    for path in paths:
        boundary = []
        num_samples = max(100, int(path.length() / 10))
        boundary.extend([path.point(t/num_samples) for t in range(num_samples)])
        boundary = [(p.real, p.imag) for p in boundary]
        boundaries.append(boundary)
    
    # Scale all boundaries
    all_points = [p for b in boundaries for p in b]
    x_min = min(p[0] for p in all_points)
    x_max = max(p[0] for p in all_points)
    y_min = min(p[1] for p in all_points)
    y_max = max(p[1] for p in all_points)
    
    scale = 500 / max(x_max - x_min, y_max - y_min)
    scaled_boundaries = []
    for boundary in boundaries:
        scaled_boundary = [((p[0] - x_min) * scale, (p[1] - y_min) * scale) for p in boundary]
        scaled_boundaries.append(scaled_boundary)
    
    return scaled_boundaries

def is_inside_boundary(x, y, boundary):
    inside = False
    for i in range(len(boundary)):
        j = (i + 1) % len(boundary)
        if ((boundary[i][1] > y) != (boundary[j][1] > y)) and \
           (x < (boundary[j][0] - boundary[i][0]) * (y - boundary[i][1]) / 
           (boundary[j][1] - boundary[i][1]) + boundary[i][0]):
            inside = not inside
    return inside

def pack_circles(boundary, min_radius=2, max_radius=25, max_attempts=10000):
    circles = []
    attempts = 0
    
    x_min = min(p[0] for p in boundary)
    x_max = max(p[0] for p in boundary)
    y_min = min(p[1] for p in boundary)
    y_max = max(p[1] for p in boundary)
    
    while attempts < max_attempts:
        radius = random.uniform(min_radius, max_radius)
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        
        if is_inside_boundary(x, y, boundary):
            overlapping = False
            for circle in circles:
                distance = math.sqrt((x - circle[0])**2 + (y - circle[1])**2)
                if distance < radius + circle[2]:
                    overlapping = True
                    break
            
            if not overlapping:
                circles.append((x, y, radius))
                attempts = 0
            else:
                attempts += 1
        else:
            attempts += 1
    
    return circles

def create_packed_circle_svg(input_file, output_file):
    try:
        boundaries = parse_svg(input_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except ValueError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    if not boundaries:
        print("Error: Could not extract boundaries from SVG.")
        return

    all_circles = []
    for boundary in boundaries:
        circles = pack_circles(boundary)
        all_circles.extend(circles)
    
    all_points = [p for b in boundaries for p in b]
    x_min = min(p[0] for p in all_points)
    x_max = max(p[0] for p in all_points)
    y_min = min(p[1] for p in all_points)
    y_max = max(p[1] for p in all_points)
    
    svg = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", 
                     viewBox=f"{x_min} {y_min} {x_max-x_min} {y_max-y_min}")
    
    for boundary in boundaries:
        path = ET.SubElement(svg, 'path')
        path.set('d', 'M' + ' L'.join(f"{x},{y}" for x, y in boundary) + ' Z')
        path.set('fill', 'none')
        path.set('stroke', 'black')
    
    for x, y, r in all_circles:
        circle = ET.SubElement(svg, 'circle')
        circle.set('cx', str(x))
        circle.set('cy', str(y))
        circle.set('r', str(r))
        circle.set('fill', f"rgb({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)})")
    
    tree = ET.ElementTree(svg)
    tree.write(output_file)
    print(f"Packed circle SVG saved as {output_file}")
    print(f"Number of circles created: {len(all_circles)}")

    # Export circles data to CSV
    csv_file = '/Workspace/Users/..../circles.csv'
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'radius'])  # Write header
        writer.writerows(all_circles)  # Write data
    print(f"Circles data exported to {csv_file}")

# Updated input and output file paths
input_file = '/.../heart-solid.svg'
output_file = '/.../heart-solid-output.svg'
create_packed_circle_svg(input_file, output_file)
