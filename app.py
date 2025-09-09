from flask import Flask, render_template, request, jsonify

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

# ------------------- helpers -------------------

def get_feed_rate_for_grade(machine, steel_grade):
    g = (steel_grade or "").strip().lower()
    if g == 'pms':
        return machine.get('Feed PMS (mm/min)')
    if g in ('2714', '2316', 'nitro b', 'nitrob', 'nitro_b'):
        return machine.get('Feed 2714/2316/Nitro B (mm/min)')
    return machine.get(f'Feed {steel_grade} (mm/min)', machine.get('Feed PMS (mm/min)', None))

def get_closest_machines(selected_dimensions, steel_grade, cut_type):
    dim_1, dim_2 = selected_dimensions
    closest_machines = []

    for machine in machine_data:
        if cut_type == "dia" and machine['Machine Name'].startswith("V"):
            continue

        capacity_1, capacity_2 = machine['Capacity']
        feed_rate = get_feed_rate_for_grade(machine, steel_grade)
        if feed_rate is None:
            continue

        if capacity_1 >= dim_1 and capacity_2 >= dim_2:
            diff = abs(capacity_1 - dim_1) + abs(capacity_2 - dim_2)
            closest_machines.append({
                'Machine Name': machine['Machine Name'],
                'Feed Rate': feed_rate,
                'Difference': diff
            })

    closest_machines.sort(key=lambda x: x['Difference'])
    return closest_machines

def calculate_cutting_time(feed_rate, block_dimensions, cut_type, num_cuts, final_dim=None):
    w, h, l = block_dimensions

    if cut_type == 'length':
        cut_dim = min(w, h)
    elif cut_type == 'height':
        cut_dim = min(w, l)
    elif cut_type == 'width':
        cut_dim = min(h, l)
    elif cut_type == 'dia':
        cut_dim = final_dim if final_dim else w
    else:
        raise ValueError("Invalid cut type.")

    return round((cut_dim / feed_rate) * num_cuts, 2)

def calculate_sq_inches(block_dimensions, cut_type, num_cuts, final_dim=None):
    w, h, l = block_dimensions

    if cut_type == "height":
        area_mm2 = w * l
    elif cut_type == "length":
        area_mm2 = w * h
    elif cut_type == "width":
        area_mm2 = h * l
    elif cut_type == "dia":
        diameter = final_dim if final_dim else w
        r = diameter / 2
        area_mm2 = 3.141592653589793 * (r ** 2)
    else:
        raise ValueError("Invalid cut type.")

    area_in2 = area_mm2 / (25.4 ** 2)
    return round(area_in2 * num_cuts, 2)

# ------------------- routes -------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    h = int(data['height'])
    w = int(data['width'])
    l = int(data['length'])
    steel_grade = data['steel_grade']
    cut_type = data['cut_type']
    final_dim = int(data['final_dimension'])
    num_cuts = int(data.get('num_cuts', 1))

    block_dimensions = (w, h, l)

    if cut_type == 'length':
        l = final_dim
        selected_dimensions = (w, h)
    elif cut_type == 'height':
        h = final_dim
        selected_dimensions = (w, l)
    elif cut_type == 'width':
        w = final_dim
        selected_dimensions = (h, l)
    elif cut_type == 'dia':
        w = final_dim
        h = final_dim
        block_dimensions = (w, h, l)
        selected_dimensions = (final_dim, final_dim)
    else:
        raise ValueError("Invalid cut type.")

    block_dimensions = (w, h, l)
    closest_machines = get_closest_machines(selected_dimensions, steel_grade, cut_type)

    results = []
    for machine in closest_machines:
        time_total = calculate_cutting_time(
            machine['Feed Rate'],
            block_dimensions,
            cut_type,
            num_cuts,
            final_dim
        )
        sq_inches = calculate_sq_inches(block_dimensions, cut_type, num_cuts, final_dim)
        results.append({
            'machine_name': machine['Machine Name'],
            'cutting_time_minutes': time_total,
            'sq_inches': sq_inches
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
