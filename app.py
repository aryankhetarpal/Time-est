from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# =====================================================
# MACHINE DATA — ALL 27 MACHINES
# =====================================================

machine_data = [

    # ================= HORIZONTAL MACHINES =================
    {'ID': 1, 'Machine Name': 'ITL1', 'Type': 'Horizontal',
     'Capacity': (1500, 610), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 1.5},

    {'ID': 2, 'Machine Name': 'ITL2', 'Type': 'Horizontal',
     'Capacity': (1550, 610), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 1.5},

    {'ID': 3, 'Machine Name': 'K1', 'Type': 'Horizontal',
     'Capacity': (1000, 750), 'Feed PMS (mm/min)': 2.5, 'Feed DS (mm/min)': 2},

    {'ID': 4, 'Machine Name': 'K2', 'Type': 'Horizontal',
     'Capacity': (400, 350), 'Feed PMS (mm/min)': 3, 'Feed DS (mm/min)': 2.8},

    {'ID': 5, 'Machine Name': 'K3', 'Type': 'Horizontal',
     'Capacity': (460, 350), 'Feed PMS (mm/min)': 3, 'Feed DS (mm/min)': 2.8},

    {'ID': 6, 'Machine Name': 'K4', 'Type': 'Horizontal',
     'Capacity': (660, 660), 'Feed PMS (mm/min)': 2.8, 'Feed DS (mm/min)': 2},

    {'ID': 7, 'Machine Name': 'K5', 'Type': 'Horizontal',
     'Capacity': (780, 800), 'Feed PMS (mm/min)': 3, 'Feed DS (mm/min)': 1.5},

    {'ID': 8, 'Machine Name': 'K6', 'Type': 'Horizontal',
     'Capacity': (430, 400), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 2},

    {'ID': 9, 'Machine Name': 'K7', 'Type': 'Horizontal',
     'Capacity': (485, 400), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 2},

    {'ID': 10, 'Machine Name': 'K8', 'Type': 'Horizontal',
     'Capacity': (620, 500), 'Feed PMS (mm/min)': 2.5, 'Feed DS (mm/min)': 2},

    {'ID': 11, 'Machine Name': 'K9', 'Type': 'Horizontal',
     'Capacity': (1300, 1050), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 1.5},

    {'ID': 12, 'Machine Name': 'K10', 'Type': 'Horizontal',
     'Capacity': (640, 640), 'Feed PMS (mm/min)': 2.2, 'Feed DS (mm/min)': 1.5},

    {'ID': 13, 'Machine Name': 'J1', 'Type': 'Horizontal',
     'Capacity': (800, 800), 'Feed PMS (mm/min)': 2.5, 'Feed DS (mm/min)': 2},

    {'ID': 14, 'Machine Name': 'J2', 'Type': 'Horizontal',
     'Capacity': (500, 500), 'Feed PMS (mm/min)': 3, 'Feed DS (mm/min)': 2},

    {'ID': 15, 'Machine Name': 'BITL', 'Type': 'Horizontal',
     'Capacity': (2300, 1800), 'Feed PMS (mm/min)': 0.9, 'Feed DS (mm/min)': 0.7},

    {'ID': 16, 'Machine Name': 'B1', 'Type': 'Horizontal',
     'Capacity': (1500, 1800), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 1.5},

    {'ID': 17, 'Machine Name': 'R', 'Type': 'Horizontal',
     'Capacity': (600, 500), 'Feed PMS (mm/min)': 3, 'Feed DS (mm/min)': 1.5},

    {'ID': 18, 'Machine Name': 'ITM2', 'Type': 'Horizontal',
     'Capacity': (490, 500), 'Feed PMS (mm/min)': 3, 'Feed DS (mm/min)': 2.8},

    {'ID': 19, 'Machine Name': 'ITM3', 'Type': 'Horizontal',
     'Capacity': (1060, 1060), 'Feed PMS (mm/min)': 2.8, 'Feed DS (mm/min)': 1.5},

    {'ID': 20, 'Machine Name': 'Friggi', 'Type': 'Horizontal',
     'Capacity': (900, 900), 'Feed PMS (mm/min)': 2.5, 'Feed DS (mm/min)': 1.5},

    {'ID': 21, 'Machine Name': 'B2', 'Type': 'Horizontal',
     'Capacity': (800, 800), 'Feed PMS (mm/min)': 3, 'Feed DS (mm/min)': 1.5},

    # ================= VERTICAL MACHINES =================
    {'ID': 22, 'Machine Name': 'V3', 'Type': 'Vertical',
     'Capacity': (800, 1500), 'Feed PMS (mm/min)': 2.2, 'Feed DS (mm/min)': 2},

    {'ID': 23, 'Machine Name': 'V5', 'Type': 'Vertical',
     'Capacity': (1500, 1500), 'Feed PMS (mm/min)': 2.8, 'Feed DS (mm/min)': 2},

    {'ID': 24, 'Machine Name': 'V6', 'Type': 'Vertical',
     'Capacity': (1200, 3500), 'Feed PMS (mm/min)': 2.8, 'Feed DS (mm/min)': 2},

    {'ID': 25, 'Machine Name': 'V7', 'Type': 'Vertical',
     'Capacity': (2000, 3500), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 1},

    {'ID': 26, 'Machine Name': 'V8', 'Type': 'Vertical',
     'Capacity': (2000, 3500), 'Feed PMS (mm/min)': 2, 'Feed DS (mm/min)': 1},
    
    {'ID': 27, 'Machine Name': 'K11', 'Type': 'Vertical',
     'Capacity': (1100, 6000), 'Feed PMS (mm/min)': 6, 'Feed DS (mm/min)': 4},
    
    {'ID': 27, 'Machine Name': 'K12', 'Type': 'Vertical',
     'Capacity': (1100, 6000), 'Feed PMS (mm/min)': 6, 'Feed DS (mm/min)': 4},
]

# =====================================================
# STEEL GRADE BENCHMARKS (in²/min baseline)
# =====================================================

grade_feed_in2 = {
    "2311": 3.0, "2738": 3.0, "2738 HH": 2.9,
    "2738 EFF": 3.0, "TSHH": 2.9, "TSHG": 2.9,
    "BMS Extra": 2.6, "2711": 2.6, "TDHHH": 2.5,
    "2714": 2.5, "HIPERDIE": 2.2, "9966": 2.2,
    "Nitro-BHT": 2.6,
    "2316": 3.1, "2085": 3.0,
    "Nitro-BA": 3.8, "2083": 3.8,
    "Conqueror": 4.0, "HWS Supreme": 4.0,
    "Ex-Stahl": 4.0, "HWR MAX": 4.0,
    "2367": 4.0, "2344": 4.0
}

hard_feed_grades = {
    "2714", "2316", "HIPERDIE",
    "9966", "Nitro-BHT"
}

INCH2_PER_MM2 = 1 / 645.16

# =====================================================
# CUTTING TIME LOGIC
# =====================================================

import math

def calculate_cutting_time(feed_rate_mm, dimensions, cut_type,
                           steel_grade, num_cuts, machine_type):

    w, h, l = dimensions

    # ---------------- Horizontal Machines ----------------
    if machine_type == "Horizontal":

        if cut_type == "length":
            thickness = min(w, h)
            area_mm = w * h

        elif cut_type == "width":
            thickness = min(w, h)
            area_mm = w * h

        elif cut_type == "height":
            thickness = min(w, l)
            area_mm = w * l

        elif cut_type == "dia":
            thickness = w
            area_mm = math.pi * (w / 2) ** 2

        else:
            raise ValueError("Invalid cut type")

        time_mm = (thickness / feed_rate_mm) * num_cuts

    # ---------------- Vertical Machines ----------------
    else:

        if cut_type == "length":
            # Feed through larger of width/height
            thickness = max(w, h)
            area_mm = w * h

        elif cut_type == "width":
            # Feed through length
            thickness = l
            area_mm = h * l

        elif cut_type == "height":
            # Feed through length
            thickness = l
            area_mm = w * l

        elif cut_type == "dia":
            thickness = w
            area_mm = math.pi * (w / 2) ** 2

        else:
            raise ValueError("Invalid cut type")

        time_mm = (thickness / feed_rate_mm) * num_cuts

    # ---------------- Area Based Time ----------------
    area_in2 = area_mm * INCH2_PER_MM2

    benchmark = grade_feed_in2.get(steel_grade)
    if benchmark is None:
        raise ValueError(f"Steel grade '{steel_grade}' not defined.")

    time_area = (area_in2 / benchmark) * num_cuts

    # ---------------- Final Time ----------------
    if machine_type == "Horizontal":
        final_time = max(time_mm, time_area)
    else:
        vertical_factor = 1.15
        final_time = max(time_mm, time_area) * vertical_factor

    return round(final_time, 2), round(area_in2 * num_cuts, 2)


# =====================================================
# ROUTES
# =====================================================

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json

        width = float(data['width'])
        height = float(data['height'])
        length = float(data['length'])
        cut_type = data['cut_type']
        steel_grade = data['steel_grade']
        num_cuts = int(data.get('num_cuts', 1))

        dimensions = (width, height, length)
        results = []

        for machine in machine_data:

            feed_rate = (
                machine['Feed DS (mm/min)']
                if steel_grade in hard_feed_grades
                else machine['Feed PMS (mm/min)']
            )

            capacity_w, capacity_h = machine['Capacity']
            can_cut = capacity_w >= width and capacity_h >= height

            cutting_time, square_inches = calculate_cutting_time(
                feed_rate,
                dimensions,
                cut_type,
                steel_grade,
                num_cuts,
                machine['Type']
            )

            results.append({
                "machine_name": machine['Machine Name'],
                "machine_type": machine['Type'],
                "cutting_time": cutting_time,
                "square_inches": square_inches,
                "can_cut": can_cut
            })

        results.sort(key=lambda x: x["cutting_time"])

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)