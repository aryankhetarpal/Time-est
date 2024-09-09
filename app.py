from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

machine_data = [
    {'ID': 1, 'Machine Name': 'ITL1', 'Capacity': (1500, 610), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 2, 'Machine Name': 'ITL2', 'Capacity': (1550, 610), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 3, 'Machine Name': 'K1', 'Capacity': (1000, 750), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 4, 'Machine Name': 'K2', 'Capacity': (400, 350), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2.8},
    {'ID': 5, 'Machine Name': 'K3', 'Capacity': (460, 350), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2.8},
    {'ID': 6, 'Machine Name': 'K4', 'Capacity': (660, 660), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 7, 'Machine Name': 'K5', 'Capacity': (780, 800), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 8, 'Machine Name': 'K6', 'Capacity': (430, 400), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 9, 'Machine Name': 'K7', 'Capacity': (485, 400), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 10, 'Machine Name': 'K8', 'Capacity': (620, 500), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 11, 'Machine Name': 'K9', 'Capacity': (1300, 1050), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 12, 'Machine Name': 'J1', 'Capacity': (800, 800), 'Feed PMS (mm/min)': 2.5, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 13, 'Machine Name': 'J2', 'Capacity': (500, 500), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 14, 'Machine Name': 'V3', 'Capacity': (800, 1500), 'Feed PMS (mm/min)': 2.2, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 15, 'Machine Name': 'V5', 'Capacity': (1500, 1500), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 16, 'Machine Name': 'V6', 'Capacity': (1200, 2500), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 2},
    {'ID': 17, 'Machine Name': 'V7', 'Capacity': (2000, 2500), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1},
    {'ID': 18, 'Machine Name': 'V8', 'Capacity': (2000, 2500), 'Feed PMS (mm/min)': 2, 'Feed 2714/2316/Nitro B (mm/min)': 1},
    {'ID': 19, 'Machine Name': 'BITL', 'Capacity': (1500, 1800), 'Feed PMS (mm/min)': 0.9, 'Feed 2714/2316/Nitro B (mm/min)': 0.7},
    {'ID': 20, 'Machine Name': 'B', 'Capacity': (1500, 1800), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 21, 'Machine Name': 'R', 'Capacity': (600, 500), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 1.5},
    {'ID': 22, 'Machine Name': 'ITM2', 'Capacity': (490, 500), 'Feed PMS (mm/min)': 3, 'Feed 2714/2316/Nitro B (mm/min)': 2.8},
    {'ID': 23, 'Machine Name': 'ITM3', 'Capacity': (1060, 1060), 'Feed PMS (mm/min)': 2.8, 'Feed 2714/2316/Nitro B (mm/min)': 1.5}
]

def get_closest_machines(selected_dimensions, steel_grade):
    dim_1, dim_2 = selected_dimensions
    closest_machines = []

    for machine in machine_data:
        capacity_1, capacity_2 = machine['Capacity']
        feed_rate = machine[f'Feed {steel_grade} (mm/min)'] if steel_grade != "PMS" else machine['Feed PMS (mm/min)']

        if capacity_1 >= dim_1 and capacity_2 >= dim_2:
            dim_1_diff = abs(capacity_1 - dim_1)
            dim_2_diff = abs(capacity_2 - dim_2)
            total_diff = dim_1_diff + dim_2_diff
            closest_machines.append({'Machine Name': machine['Machine Name'], 'Feed Rate': feed_rate, 'Difference': total_diff})

    closest_machines.sort(key=lambda x: x['Difference'])
    return closest_machines[:5]

def calculate_cutting_time(feed_rate, block_dimensions, cut_type):
    block_w, block_h, block_l = block_dimensions
    if cut_type == 'length':
        cut_dim = min(block_h, block_w)
    elif cut_type == 'height':
        cut_dim = min(block_w, block_l)
    elif cut_type == 'width':
        cut_dim = min(block_h, block_l)
    else:
        raise ValueError("Invalid cut type. Choose 'length', 'height', or 'width'.")

    time_required = cut_dim / feed_rate
    return time_required

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    height = int(data['height'])
    width = int(data['width'])
    length = int(data['length'])
    steel_grade = data['steel_grade']
    cut_type = data['cut_type']
    final_dim = int(data['final_dimension'])

    block_dimensions = (width, height, length)

    if cut_type == 'length':
        length = final_dim
        selected_dimensions = (width, height)
    elif cut_type == 'height':
        height = final_dim
        selected_dimensions = (width, length)
    elif cut_type == 'width':
        width = final_dim
        selected_dimensions = (height, length)

    block_dimensions = (width, height, length)
    closest_machines = get_closest_machines(selected_dimensions, steel_grade)

    results = []
    for machine in closest_machines:
        time = calculate_cutting_time(machine['Feed Rate'], block_dimensions, cut_type)
        results.append({
            'machine_name': machine['Machine Name'],
            'cutting_time': round(time, 2)
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)