from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Chennai feed mapping (sq.in/min)
grade_feed_in2 = {
    "PMS": 3.72,
    "DS": 3.72,
    "2714": 2.79,
    "2316": 2.79,
    "Nitro B": 2.79
}

machine_data = [
    {'ID': 1, 'Machine Name': 'ITL1', 'Capacity': (1500, 610)},
    {'ID': 2, 'Machine Name': 'ITL2', 'Capacity': (1550, 610)},
    {'ID': 3, 'Machine Name': 'K1', 'Capacity': (1000, 750)},
    {'ID': 4, 'Machine Name': 'K2', 'Capacity': (400, 350)},
    {'ID': 5, 'Machine Name': 'K3', 'Capacity': (460, 350)},
    {'ID': 6, 'Machine Name': 'K4', 'Capacity': (660, 660)},
    {'ID': 7, 'Machine Name': 'K5', 'Capacity': (780, 800)},
    {'ID': 8, 'Machine Name': 'K6', 'Capacity': (430, 400)},
    {'ID': 9, 'Machine Name': 'K7', 'Capacity': (485, 400)},
    {'ID': 10, 'Machine Name': 'K8', 'Capacity': (620, 500)},
    {'ID': 11, 'Machine Name': 'K9', 'Capacity': (1300, 1050)},
    {'ID': 12, 'Machine Name': 'K10', 'Capacity': (640, 640)},
    {'ID': 13, 'Machine Name': 'J1', 'Capacity': (800, 800)},
    {'ID': 14, 'Machine Name': 'J2', 'Capacity': (500, 500)},
    {'ID': 15, 'Machine Name': 'V3', 'Capacity': (800, 1500)},
    {'ID': 16, 'Machine Name': 'V5', 'Capacity': (1500, 1500)},
    {'ID': 17, 'Machine Name': 'V6', 'Capacity': (1200, 3500)},
    {'ID': 18, 'Machine Name': 'V7', 'Capacity': (2000, 3500)},
    {'ID': 19, 'Machine Name': 'V8', 'Capacity': (2000, 3500)},
    {'ID': 20, 'Machine Name': 'BITL', 'Capacity': (1500, 1800)},
    {'ID': 21, 'Machine Name': 'B1', 'Capacity': (1500, 1800)},
    {'ID': 22, 'Machine Name': 'R', 'Capacity': (600, 500)},
    {'ID': 23, 'Machine Name': 'ITM2', 'Capacity': (490, 500)},
    {'ID': 24, 'Machine Name': 'ITM3', 'Capacity': (1060, 1060)},
    {'ID': 25, 'Machine Name': 'Friggi', 'Capacity': (900, 900)},
    {'ID': 26, 'Machine Name': 'B2', 'Capacity': (800, 800)}
]

# Calculate cutting time using Chennai sq.in/min logic
def calculate_cutting_time_sq_in(block_dimensions, cut_type, grade, num_cuts=1):
    block_w, block_h, block_l = block_dimensions
    
    # Compute cross-section area in sq.mm based on cut type
    if cut_type == "height":
        area_mm2 = block_w * block_l
    elif cut_type == "length":
        area_mm2 = block_w * block_h
    elif cut_type == "width":
        area_mm2 = block_h * block_l
    elif cut_type == "dia":
        diameter = block_w
        area_mm2 = math.pi * (diameter / 2) ** 2
    else:
        raise ValueError("Invalid cut type.")
    
    # Convert to sq.inches
    area_in2 = area_mm2 / 645
    feed_rate = grade_feed_in2[grade]  # sq.in/min
    time_min = (area_in2 / feed_rate) * num_cuts
    return round(time_min, 2), round(area_in2 * num_cuts, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    # Detect if height is "Dia" (case-insensitive)
    height_input = str(data['height']).strip()
    if height_input.lower() == 'dia':
        cut_type = 'dia'
        height = None  # will set later
    else:
        height = int(height_input)
        cut_type = data['cut_type']

    width = int(data['width'])
    length = int(data['length'])
    steel_grade = data['steel_grade']
    final_dim = int(data['final_dimension'])
    num_cuts = int(data.get('num_cuts', 1))

    # Set block dimensions based on cut type
    if cut_type == 'length':
        length = final_dim
        block_dimensions = (width, height, length)
        selected_dimensions = (width, height)
    elif cut_type == 'height':
        height = final_dim
        block_dimensions = (width, height, length)
        selected_dimensions = (width, length)
    elif cut_type == 'width':
        width = final_dim
        block_dimensions = (width, height, length)
        selected_dimensions = (height, length)
    elif cut_type == 'dia':
        diameter = width
        block_dimensions = (diameter, diameter, length)
        selected_dimensions = (diameter, diameter)
    else:
        raise ValueError("Invalid cut type.")

    results = []
    for machine in machine_data:
        if cut_type == "dia" and machine['Machine Name'].startswith("V"):
            continue  # exclude vertical machines for dia

        capacity_1, capacity_2 = machine['Capacity']
        can_cut = capacity_1 >= selected_dimensions[0] and capacity_2 >= selected_dimensions[1]

        cutting_time, sq_inches = calculate_cutting_time_sq_in(block_dimensions, cut_type, steel_grade, num_cuts)
        results.append({
            'machine_name': machine['Machine Name'],
            'cutting_time': cutting_time,
            'sq_inches': sq_inches,
            'can_cut': can_cut
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
