from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

machine_data = [
    {'ID': 1, 'Machine Name': 'ITL1', 'Capacity': (1500, 610), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 2, 'Machine Name': 'ITL2', 'Capacity': (1550, 610), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 3, 'Machine Name': 'K1', 'Capacity': (1000, 750), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 4, 'Machine Name': 'K2', 'Capacity': (400, 350), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2.8},
    {'ID': 5, 'Machine Name': 'K3', 'Capacity': (460, 350), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2.8},
    {'ID': 6, 'Machine Name': 'K4', 'Capacity': (660, 660), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 7, 'Machine Name': 'K5', 'Capacity': (780, 800), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 8, 'Machine Name': 'K6', 'Capacity': (430, 400), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 9, 'Machine Name': 'K7', 'Capacity': (485, 400), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 10, 'Machine Name': 'K8', 'Capacity': (620, 500), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 11, 'Machine Name': 'K9', 'Capacity': (1300, 1050), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 12, 'Machine Name': 'K10', 'Capacity': (640, 640), 'Feed PMS (mm/min)': 2.2, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 13, 'Machine Name': 'J1', 'Capacity': (800, 800), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 14, 'Machine Name': 'J2', 'Capacity': (500, 500), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 15, 'Machine Name': 'V3', 'Capacity': (800, 1500), 'Feed PMS (mm/min)': 2.2, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 16, 'Machine Name': 'V5', 'Capacity': (1500, 1500), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 17, 'Machine Name': 'V6', 'Capacity': (1200, 3500), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 18, 'Machine Name': 'V7', 'Capacity': (2000, 3500), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1},
    {'ID': 19, 'Machine Name': 'V8', 'Capacity': (2000, 3500), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1},
    {'ID': 20, 'Machine Name': 'BITL', 'Capacity': (1500, 1800), 'Feed PMS (mm/min)': 0.9, 'Feed 2714/2316/Nitro B (mm/min)': 0.7},
    {'ID': 21, 'Machine Name': 'B1', 'Capacity': (1500, 1800), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 22, 'Machine Name': 'R', 'Capacity': (600, 500), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 23, 'Machine Name': 'ITM2', 'Capacity': (490, 500), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2.8},
    {'ID': 24, 'Machine Name': 'ITM3', 'Capacity': (1060, 1060), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 25, 'Machine Name': 'Friggi', 'Capacity': (900, 900), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 26, 'Machine Name': 'B2', 'Capacity': (800, 800), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 1.5}
]

# Benchmark feed in square inches/min
grade_feed_in2 = {
    "PMS": 3.72,
    "2714": 2.79,
    "2316": 2.79,
    "Nitro B": 2.79
}
INCH2_PER_MM2 = 1 / 645.16  # mm² -> in²

def calculate_sq_inches(block_dimensions, cut_type, num_cuts=1):
    block_w, block_h, block_l = block_dimensions
    if cut_type == "height":
        area_mm = block_w * block_l
    elif cut_type == "length":
        area_mm = block_w * block_h
    elif cut_type == "width":
        area_mm = block_h * block_l
    elif cut_type == "dia":
        diameter = block_w
        area_mm = math.pi * (diameter / 2) ** 2
    else:
        raise ValueError("Invalid cut type")
    area_in2 = area_mm * INCH2_PER_MM2
    return round(area_in2 * num_cuts, 2)

def calculate_cutting_time(feed_rate_mm, block_dimensions, cut_type, machine_name, steel_grade, num_cuts=1):
    block_w, block_h, block_l = block_dimensions

    # For V machines, use larger of the cross-sectional dimensions
    if machine_name.startswith("V"):
        if cut_type == 'length':
            cut_thickness = max(block_h, block_w)
            area_mm = block_h * block_w
        elif cut_type == 'width':
            cut_thickness = max(block_h, block_l)
            area_mm = block_h * block_l
        elif cut_type == 'height':
            cut_thickness = max(block_w, block_l)
            area_mm = block_w * block_l
    else:  # For non-V machines, use smaller dimension
        if cut_type == 'length':
            cut_thickness = min(block_h, block_w)
            area_mm = block_h * block_w
        elif cut_type == 'width':
            cut_thickness = min(block_h, block_l)
            area_mm = block_h * block_l
        elif cut_type == 'height':
            cut_thickness = min(block_w, block_l)
            area_mm = block_w * block_l

    # For dia cuts
    if cut_type == 'dia':
        cut_thickness = block_w
        area_mm = math.pi * (cut_thickness / 2) ** 2

    # Time based on mm/min feed
    time_mm = (cut_thickness / feed_rate_mm) * num_cuts

    # Time based on benchmark sq.in/min
    area_in2 = area_mm * INCH2_PER_MM2
    benchmark_feed = grade_feed_in2[steel_grade]
    time_in2 = (area_in2 / benchmark_feed) * num_cuts

    # Use the larger of the two for realism
    time_min = max(time_mm, time_in2)
    return round(time_min, 2)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    height_input = str(data['height']).strip()
    cut_type = data['cut_type']
    steel_grade = data['steel_grade']
    final_dim = int(data['final_dimension'])
    num_cuts = int(data.get('num_cuts', 1))

    if height_input.lower() == 'dia':
        cut_type = 'dia'
        height = None
    else:
        height = int(height_input)

    width = int(data['width'])
    length = int(data['length'])

    # Adjust final dimension
    if cut_type == 'length':
        length = final_dim
        block_dimensions = (width, height, length)
        selected_dimensions = (width, height)
    elif cut_type == 'width':
        width = final_dim
        block_dimensions = (width, height, length)
        selected_dimensions = (height, length)
    elif cut_type == 'height':
        height = final_dim
        block_dimensions = (width, height, length)
        selected_dimensions = (width, length)
    elif cut_type == 'dia':
        diameter = width
        block_dimensions = (diameter, diameter, length)
        selected_dimensions = (diameter, diameter)

    results = []
    for machine in machine_data:
        if cut_type == "dia" and machine['Machine Name'].startswith("V"):
            continue  # skip vertical machines for dia cuts
        capacity_1, capacity_2 = machine['Capacity']
        feed_rate = machine.get(f'Feed {steel_grade} (mm/min)', machine.get('Feed PMS (mm/min)', None))
        if feed_rate is None:
            continue
        can_cut = capacity_1 >= selected_dimensions[0] and capacity_2 >= selected_dimensions[1]
        time = calculate_cutting_time(feed_rate, block_dimensions, cut_type, machine['Machine Name'], steel_grade, num_cuts)
        sq_inches = calculate_sq_inches(block_dimensions, cut_type, num_cuts)
        results.append({
            'machine_name': machine['Machine Name'],
            'cutting_time': time,
            'sq_inches': sq_inches,
            'can_cut': can_cut
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
