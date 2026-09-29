# IoT-Based-Energy-Monitoring
import time
import csv
import requests
from datetime import datetime

# ==========================================
# IoT ENERGY MONITORING SYSTEM
# ==========================================

# ThingSpeak configuration
THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# Electricity tariff
COST_PER_KWH = 7.00       # ₹ per kWh

# Monitoring interval
INTERVAL = 15             # seconds

# Total energy consumed
total_energy_kwh = 0.0


# ==========================================
# SENSOR READING
# ==========================================

def read_sensor():

    """
    Replace this function with actual
    voltage/current sensor readings.

    Example:
    voltage = PZEM voltage
    current = PZEM current
    """

    # Example sensor values
    voltage = 230.0
    current = 2.5

    return voltage, current


# ==========================================
# ENERGY CALCULATION
# ==========================================

def calculate_energy(power, time_seconds):

    # Convert seconds to hours
    time_hours = time_seconds / 3600

    # Power(W) × time(h) / 1000 = kWh
    energy = (power * time_hours) / 1000

    return energy


# ==========================================
# SAVE DATA TO CSV
# ==========================================

def save_data(voltage, current, power, energy, cost):

    filename = "energy_data.csv"

    with open(filename, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            voltage,
            current,
            power,
            energy,
            cost
        ])


# ==========================================
# SEND DATA TO THINGSPEAK
# ==========================================

def send_to_thingspeak(voltage, current, power, energy):

    data = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": voltage,
        "field2": current,
        "field3": power,
        "field4": energy
    }

    try:

        response = requests.get(
            THINGSPEAK_URL,
            params=data,
            timeout=10
        )

        if response.status_code == 200:
            print("IoT upload successful")

        else:
            print("IoT upload failed")

    except requests.RequestException as error:

        print("Internet error:", error)


# ==========================================
# CREATE CSV HEADER
# ==========================================

try:

    with open("energy_data.csv", "x", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Date & Time",
            "Voltage (V)",
            "Current (A)",
            "Power (W)",
            "Energy (kWh)",
            "Cost (Rs)"
        ])

except FileExistsError:

    pass


# ==========================================
# MAIN PROGRAM
# ==========================================

print("=" * 55)
print("       IoT BASED ENERGY MONITORING SYSTEM")
print("=" * 55)

previous_time = time.time()

try:

    while True:

        # Read sensor
        voltage, current = read_sensor()

        # Calculate power
        power = voltage * current

        # Calculate elapsed time
        current_time = time.time()

        elapsed_time = current_time - previous_time

        previous_time = current_time

        # Calculate energy
        energy = calculate_energy(
            power,
            elapsed_time
        )

        # Add to total energy
        total_energy_kwh += energy

        # Calculate electricity cost
        cost = total_energy_kwh * COST_PER_KWH

        # Display results
        print("\n---------------------------------------")

        print(
            "Time       :",
            datetime.now().strftime("%H:%M:%S")
        )

        print(
            f"Voltage    : {voltage:.2f} V"
        )

        print(
            f"Current    : {current:.2f} A"
        )

        print(
            f"Power      : {power:.2f} W"
        )

        print(
            f"Energy     : {total_energy_kwh:.6f} kWh"
        )

        print(
            f"Cost       : ₹{cost:.2f}"
        )

        # Save locally
        save_data(
            voltage,
            current,
            power,
            total_energy_kwh,
            cost
        )

        # Send to IoT
        send_to_thingspeak(
            voltage,
            current,
            power,
            total_energy_kwh
        )

        print("---------------------------------------")

        # Wait
        time.sleep(INTERVAL)


except KeyboardInterrupt:

    print("\n\nEnergy monitoring stopped.")
    print(f"Total Energy: {total_energy_kwh:.4f} kWh")
    print(f"Total Cost: ₹{total_energy_kwh * COST_PER_KWH:.2f}")
