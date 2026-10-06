import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
from datetime import datetime


# ============================================================
# PARKING CONFIGURATION
# ============================================================

ROWS = 6
COLS = 7
DRIVEWAY_COL = 3

parking_slots = {}

slot_number = 1

for row in range(ROWS):
    for col in range(COLS):

        # Center column is driveway
        if col != DRIVEWAY_COL:

            parking_slots[(row, col)] = {
                "number": slot_number,
                "occupied": False,
                "vehicle_id": None,
                "entry_time": None
            }

            slot_number += 1


# ============================================================
# STATE MACHINE
# ============================================================

IDLE = "IDLE"
VEHICLE_DETECTED = "VEHICLE_DETECTED"
CHECK_SPACE = "CHECK_SPACE"
GATE_OPENING = "GATE_OPENING"
GATE_OPEN = "GATE_OPEN"
PARKING = "PARKING"
GATE_CLOSING = "GATE_CLOSING"
GATE_CLOSED = "GATE_CLOSED"

current_state = GATE_CLOSED


# ============================================================
# SYSTEM VARIABLES
# ============================================================

gate_open = False

ultrasonic_distance = 100

vehicle_counter = 0

ir_sensors = {}
rgb_leds = {}

for position in parking_slots:
    ir_sensors[position] = False
    rgb_leds[position] = "GREEN"


# ============================================================
# LOGGING
# ============================================================

def log(message):

    timestamp = datetime.now().strftime("%H:%M:%S")

    text = f"[{timestamp}] {message}"

    serial_text.insert(tk.END, text + "\n")
    serial_text.see(tk.END)


# ============================================================
# LCD
# ============================================================

def update_lcd():

    free_slots = 0

    for slot in parking_slots.values():

        if not slot["occupied"]:
            free_slots += 1

    lcd_free.config(
        text=f"FREE SLOTS: {free_slots}"
    )

    if free_slots == 0:

        lcd_status.config(
            text="PARKING FULL",
            fg="red"
        )

    else:

        lcd_status.config(
            text="SPACE AVAILABLE",
            fg="lime"
        )


# ============================================================
# IR SENSOR SIMULATION
# ============================================================

def update_ir_sensors():

    for position, slot in parking_slots.items():

        ir_sensors[position] = slot["occupied"]


# ============================================================
# RGB LED SIMULATION
# ============================================================

def update_rgb_leds():

    for position, slot in parking_slots.items():

        if slot["occupied"]:

            rgb_leds[position] = "RED"

        else:

            rgb_leds[position] = "GREEN"


# ============================================================
# GATE CONTROL
# ============================================================

def open_gate():

    global gate_open
    global current_state

    gate_open = True

    current_state = GATE_OPEN

    gate_label.config(
        text="GATE OPEN",
        bg="lightgreen"
    )

    servo_label.config(
        text="SERVO: 90°"
    )

    log("[GATE] Gate opened")
    log("[SERVO] Servo moved to 90°")


def close_gate():

    global gate_open
    global current_state

    gate_open = False

    current_state = GATE_CLOSED

    gate_label.config(
        text="GATE CLOSED",
        bg="tomato"
    )

    servo_label.config(
        text="SERVO: 0°"
    )

    log("[GATE] Gate closed")
    log("[SERVO] Servo moved to 0°")


# ============================================================
# GET FREE SLOTS
# ============================================================

def get_free_slots():

    free = []

    for position, slot in parking_slots.items():

        if not slot["occupied"]:

            free.append(position)

    return free


# ============================================================
# BFS SHORTEST PATH
# ============================================================

def shortest_path(start, target):

    queue = deque([start])

    visited = {start}

    parent = {}

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    while queue:

        current = queue.popleft()

        if current == target:

            path = []

            while current != start:

                path.append(current)

                current = parent[current]

            path.append(start)

            path.reverse()

            return path

        row, col = current

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            if not (0 <= new_row < ROWS):
                continue

            if not (0 <= new_col < COLS):
                continue

            next_position = (new_row, new_col)

            if next_position in visited:
                continue

            # Driveway is always traversable
            if new_col == DRIVEWAY_COL:

                visited.add(next_position)

                parent[next_position] = current

                queue.append(next_position)

                continue

            # Parking slot
            if next_position in parking_slots:

                if parking_slots[next_position]["occupied"]:
                    continue

                visited.add(next_position)

                parent[next_position] = current

                queue.append(next_position)

    return []


# ============================================================
# FIND NEAREST SLOT
# ============================================================

def find_nearest_slot():

    free_slots = get_free_slots()

    if not free_slots:

        return None

    best_slot = None

    shortest_distance = float("inf")

    for slot in free_slots:

        path = shortest_path(
            ENTRANCE,
            slot
        )

        if path:

            distance = len(path)

            if distance < shortest_distance:

                shortest_distance = distance

                best_slot = slot

    return best_slot


# ============================================================
# GENERATE VEHICLE ID
# ============================================================

def generate_vehicle_id():

    global vehicle_counter

    vehicle_counter += 1

    return f"VEH-{vehicle_counter:03d}"


# ============================================================
# UPDATE EXIT DROPDOWN
# ============================================================

def update_vehicle_dropdown():

    parked_vehicles = []

    for slot in parking_slots.values():

        if slot["occupied"]:

            parked_vehicles.append(
                slot["vehicle_id"]
            )

    exit_vehicle_combo["values"] = parked_vehicles

    if parked_vehicles:

        exit_vehicle_combo.current(0)

    else:

        exit_vehicle_combo.set("")


# ============================================================
# UPDATE PARKING DISPLAY
# ============================================================

def update_display():

    update_ir_sensors()

    update_rgb_leds()

    for position, button in buttons.items():

        row, col = position

        # DRIVEWAY
        if col == DRIVEWAY_COL:

            if position == ENTRANCE:

                button.config(
                    text="ENTRANCE",
                    bg="lightblue"
                )

            elif position == EXIT:

                button.config(
                    text="EXIT",
                    bg="lightgray"
                )

            else:

                button.config(
                    text="DRIVEWAY\n↓",
                    bg="lightgray"
                )

        # PARKING SLOT
        else:

            slot = parking_slots[position]

            number = slot["number"]

            if slot["occupied"]:

                vehicle = slot["vehicle_id"]

                button.config(
                    text=f"S{number}\nOCCUPIED\n{vehicle}",
                    bg="tomato"
                )

            else:

                button.config(
                    text=f"S{number}\nEMPTY",
                    bg="lightgreen"
                )

    update_lcd()

    update_vehicle_dropdown()


# ============================================================
# VEHICLE DETECTION
# ============================================================

def detect_vehicle():

    global ultrasonic_distance
    global current_state

    ultrasonic_distance = 10

    ultrasonic_label.config(
        text="ULTRASONIC: 10 cm\nVEHICLE DETECTED"
    )

    log(
        "[ULTRASONIC] Vehicle detected at entrance"
    )

    current_state = VEHICLE_DETECTED

    check_parking_space()


# ============================================================
# CHECK PARKING SPACE
# ============================================================

def check_parking_space():

    global current_state

    free_slots = get_free_slots()

    # PARKING FULL
    if len(free_slots) == 0:

        current_state = GATE_CLOSED

        close_gate()

        log("[SYSTEM] Parking FULL")

        log("[GATE] Entry denied")

        messagebox.showwarning(
            "Parking Full",
            "No parking slots available!"
        )

        return False

    # SPACE AVAILABLE

    current_state = CHECK_SPACE

    log(
        f"[SYSTEM] Free slots: {len(free_slots)}"
    )

    nearest = find_nearest_slot()

    if nearest is not None:

        slot_num = parking_slots[
            nearest
        ]["number"]

        log(
            f"[BFS] Nearest available slot: S{slot_num}"
        )

    open_gate()

    return True


# ============================================================
# VEHICLE ENTRY
# ============================================================

def vehicle_arrival():

    global current_state

    log("----------------------------------------")

    log("[ENTRY] Vehicle arrival initiated")

    # Detect vehicle
    detect_vehicle()

    # Gate remains closed if parking full
    if not gate_open:

        return

    # Automatically generate ID
    vehicle_id = generate_vehicle_id()

    log(
        f"[SYSTEM] Generated Vehicle ID: {vehicle_id}"
    )

    # Find nearest slot
    target = find_nearest_slot()

    if target is None:

        close_gate()

        return

    slot = parking_slots[target]

    # Store vehicle
    slot["occupied"] = True

    slot["vehicle_id"] = vehicle_id

    slot["entry_time"] = datetime.now()

    current_state = PARKING

    log(
        f"[PARKING] {vehicle_id} assigned to "
        f"S{slot['number']}"
    )

    # Calculate path
    path = shortest_path(
        ENTRANCE,
        target
    )

    if path:

        log(
            f"[BFS] Shortest path = "
            f"{len(path) - 1} steps"
        )

        highlight_path(path)

    # Update display
    update_display()

    # Close gate
    close_gate()

    current_state = GATE_CLOSED

    # Show status
    status.config(
        text=f"{vehicle_id} parked at S{slot['number']}"
    )

    log(
        f"[ENTRY] {vehicle_id} successfully parked"
    )

    log("----------------------------------------")


# ============================================================
# VEHICLE EXIT
# ============================================================

def vehicle_exit():

    vehicle_id = exit_vehicle_combo.get().strip()

    if vehicle_id == "":

        messagebox.showwarning(
            "Vehicle Exit",
            "No parked vehicle selected!"
        )

        return

    for position, slot in parking_slots.items():

        if slot["vehicle_id"] == vehicle_id:

            slot_number = slot["number"]

            # Free slot
            slot["occupied"] = False

            slot["vehicle_id"] = None

            slot["entry_time"] = None

            log("----------------------------------------")

            log(
                f"[EXIT] {vehicle_id} leaving S{slot_number}"
            )

            # Update sensors
            update_display()

            status.config(
                text=f"{vehicle_id} exited from S{slot_number}"
            )

            log(
                f"[IR SENSOR] S{slot_number} → GREEN"
            )

            log(
                "[LCD] Parking availability updated"
            )

            log("----------------------------------------")

            return

    messagebox.showwarning(
        "Vehicle Not Found",
        "Selected vehicle is not currently parked."
    )


# ============================================================
# HIGHLIGHT BFS PATH
# ============================================================

def highlight_path(path):

    update_display()

    for position in path:

        if position == ENTRANCE:
            continue

        if position in buttons:

            if position in parking_slots:

                buttons[position].config(
                    bg="yellow"
                )

            else:

                buttons[position].config(
                    bg="khaki"
                )


# ============================================================
# RESET ULTRASONIC
# ============================================================

def reset_ultrasonic():

    global ultrasonic_distance

    ultrasonic_distance = 100

    ultrasonic_label.config(
        text="ULTRASONIC: 100 cm\nNO VEHICLE"
    )


# ============================================================
# GUI
# ============================================================

root = tk.Tk()

root.title(
    "Smart Parking System"
)

root.geometry(
    "1200x900"
)

root.configure(
    bg="#1e1e1e"
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="SMART PARKING SYSTEM",
    font=("Arial", 24, "bold"),
    bg="#1e1e1e",
    fg="white"
)

title.pack(pady=10)


# ============================================================
# GATE
# ============================================================

gate_label = tk.Label(
    root,
    text="GATE CLOSED",
    font=("Arial", 16, "bold"),
    bg="tomato",
    width=20,
    height=2
)

gate_label.pack(pady=5)


servo_label = tk.Label(
    root,
    text="SERVO: 0°",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white"
)

servo_label.pack()


# ============================================================
# PARKING GRID
# ============================================================

parking_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

parking_frame.pack(pady=10)


buttons = {}


for row in range(ROWS):

    for col in range(COLS):

        button = tk.Button(
            parking_frame,
            width=12,
            height=4,
            font=("Arial", 8, "bold")
        )

        button.grid(
            row=row,
            column=col,
            padx=3,
            pady=3
        )

        buttons[(row, col)] = button


# ============================================================
# ENTRANCE / EXIT
# ============================================================

ENTRANCE = (ROWS - 1, DRIVEWAY_COL)

EXIT = (0, DRIVEWAY_COL)


# ============================================================
# CONTROLS
# ============================================================

controls = tk.Frame(
    root,
    bg="#1e1e1e"
)

controls.pack(pady=10)


# ENTRY

entry_button = tk.Button(
    controls,
    text="🚗 DETECT VEHICLE",
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    command=vehicle_arrival
)

entry_button.grid(
    row=0,
    column=0,
    padx=10
)


# EXIT

exit_vehicle_combo = ttk.Combobox(
    controls,
    width=22,
    state="readonly"
)

exit_vehicle_combo.grid(
    row=1,
    column=0,
    padx=10,
    pady=8
)


exit_button = tk.Button(
    controls,
    text="🚗 VEHICLE EXIT",
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    command=vehicle_exit
)

exit_button.grid(
    row=1,
    column=1,
    padx=10
)


# ============================================================
# LCD
# ============================================================

lcd_frame = tk.Frame(
    root,
    bg="black",
    padx=15,
    pady=10
)

lcd_frame.pack(pady=10)


lcd_title = tk.Label(
    lcd_frame,
    text="SMART PARKING LCD",
    fg="white",
    bg="black",
    font=("Courier", 12)
)

lcd_title.pack()


lcd_free = tk.Label(
    lcd_frame,
    text="FREE SLOTS: 36",
    fg="lime",
    bg="black",
    font=("Courier", 16, "bold")
)

lcd_free.pack()


lcd_status = tk.Label(
    lcd_frame,
    text="SPACE AVAILABLE",
    fg="lime",
    bg="black",
    font=("Courier", 12)
)

lcd_status.pack()


# ============================================================
# SENSOR STATUS
# ============================================================

sensor_frame = tk.Frame(
    root,
    bg="#1e1e1e"
)

sensor_frame.pack(pady=5)


ultrasonic_label = tk.Label(
    sensor_frame,
    text="ULTRASONIC: 100 cm\nNO VEHICLE",
    font=("Arial", 11),
    width=25,
    bg="#1e1e1e",
    fg="white"
)

ultrasonic_label.grid(
    row=0,
    column=0,
    padx=10
)


tk.Label(
    sensor_frame,
    text="IR SENSORS →\nGREEN = EMPTY\nRED = OCCUPIED",
    font=("Arial", 11),
    bg="#1e1e1e",
    fg="white"
).grid(
    row=0,
    column=1,
    padx=10
)


# ============================================================
# SERIAL MONITOR
# ============================================================

tk.Label(
    root,
    text="SERIAL MONITOR",
    font=("Arial", 12, "bold"),
    bg="#1e1e1e",
    fg="white"
).pack()


serial_text = tk.Text(
    root,
    height=8,
    width=100,
    bg="black",
    fg="white"
)

serial_text.pack(pady=5)


# ============================================================
# STATUS
# ============================================================

status = tk.Label(
    root,
    text="System ready — Gate closed",
    font=("Arial", 12, "bold"),
    bg="#1e1e1e",
    fg="white"
)

status.pack(pady=5)


# ============================================================
# INITIALIZE SYSTEM
# ============================================================

update_display()

close_gate()

log(
    "[SYSTEM] Smart Parking System initialized"
)

log(
    f"[SYSTEM] Total parking slots: "
    f"{len(parking_slots)}"
)

log(
    "[SYSTEM] IR sensors initialized"
)

log(
    "[SYSTEM] Ultrasonic sensor initialized"
)

log(
    "[SYSTEM] Servo motor initialized"
)

log(
    "[SYSTEM] RGB LEDs initialized"
)

log(
    "[SYSTEM] I2C LCD initialized"
)

log(
    "[SYSTEM] BFS path planner initialized"
)

log(
    "[SYSTEM] State machine initialized"
)

log(
    "[SYSTEM] Gate state: CLOSED"
)


# ============================================================
# START GUI
# ============================================================

root.mainloop()