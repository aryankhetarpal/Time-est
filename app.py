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
    # fallback: exact key or PMS
    return machine.get(f'Feed {steel_grade} (mm/min)', machine.get('Feed PMS (mm/min)', None))


def calculate_cutting_time(feed_rate, block_dimensions, cut_type, num_cuts, final_dim=None):
    """Return total time in minutes (float)."""
    if not feed_rate or feed_rate <= 0:
        return None  # feed missing

    block_w, block_h, block_l = block_dimensions

    if cut_type == 'length':
        cut_dim = min(block_w, block_h)
    elif cut_type == 'height':
        cut_dim = min(block_w, block_l)
    elif cut_type == 'width':
        cut_dim = min(block_h, block_l)
    elif cut_type == 'dia':
        cut_dim = final_dim if final_dim is not None else block_w
    else:
        return None

    time_per_cut = cut_dim / feed_rate  # minutes
    total_time = time_per_cut * num_cuts
    return round(total_time, 2)


def calculate_sq_inches(block_dimensions, cut_type, num_cuts, final_dim=None):
    """Return total square inches (float)."""
    block_w, block_h, block_l = block_dimensions

    if cut_type == "height":
        area_mm2 = block_w * block_l
    elif cut_type == "length":
        area_mm2 = block_w * block_h
    elif cut_type == "width":
        area_mm2 = block_h * block_l
    elif cut_type == "dia":
        diameter = final_dim if final_dim is not None else block_w
        radius = diameter / 2
        area_mm2 = 3.141592653589793 * (radius ** 2)
    else:
        return None

    area_in2 = area_mm2 / (25.4 ** 2)
    return round(area_in2 * num_cuts, 2)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    block_w = float(data.get('width', 0))
    block_h = float(data.get('height', 0))
    block_l = float(data.get('length', 0))
    steel_grade = data.get('steelGrade')
    cut_type = data.get('cutType')
    final_dim = float(data['finalDimension']) if data.get('finalDimension') else None
    num_cuts = int(data.get('numCuts', 1))

    block_dimensions = (block_w, block_h, block_l)

    # choose comparison dims for machine selection
    if cut_type == "height":
        selected_dimensions = (block_w, block_l)
    elif cut_type == "length":
        selected_dimensions = (block_w, block_h)
    elif cut_type == "width":
        selected_dimensions = (block_h, block_l)
    elif cut_type == "dia":
        selected_dimensions = (final_dim if final_dim else block_w, block_h)
    else:
        return jsonify({'error': 'Invalid cut type'}), 400

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
            'cutting_time_minutes': time_total if time_total is not None else "Feed rate missing",
            'sq_inches': sq_inches if sq_inches is not None else "Error calculating area"
        })

    return jsonify({'results': results})
