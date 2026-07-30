from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
import csv

import matplotlib.pyplot as plt


# --------------------------------------------------
# FILE LOCATIONS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parents[1]

input_file = (
    project_folder
    / "data"
    / "hall_sensor_distance_test.csv"
)

graphs_folder = project_folder / "graphs"
results_folder = project_folder / "results"

graphs_folder.mkdir(exist_ok=True)
results_folder.mkdir(exist_ok=True)

graph_file = (
    graphs_folder
    / "hall_sensor_voltage_vs_distance.png"
)

summary_file = (
    results_folder
    / "hall_sensor_summary.csv"
)


# --------------------------------------------------
# READ AND GROUP THE DATA
# --------------------------------------------------

grouped_data = defaultdict(
    lambda: {
        "raw_readings": [],
        "voltages": [],
    }
)

with input_file.open(
    mode="r",
    newline="",
    encoding="utf-8",
) as csv_file:

    reader = csv.DictReader(csv_file)

    for row in reader:
        test = row["test"].strip()
        pole = row["pole"].strip()
        distance_text = row["distance_cm"].strip()

        raw_reading = int(row["raw_reading"])
        voltage = float(row["voltage"])

        key = (test, pole, distance_text)

        grouped_data[key]["raw_readings"].append(
            raw_reading
        )

        grouped_data[key]["voltages"].append(
            voltage
        )


# --------------------------------------------------
# CALCULATE AVERAGES AND VARIATION
# --------------------------------------------------

summary_rows = []

for key, readings in grouped_data.items():
    test, pole, distance_text = key

    raw_values = readings["raw_readings"]
    voltage_values = readings["voltages"]

    average_raw = mean(raw_values)
    average_voltage = mean(voltage_values)

    if len(voltage_values) > 1:
        voltage_standard_deviation = stdev(
            voltage_values
        )
    else:
        voltage_standard_deviation = 0.0

    summary_rows.append(
        {
            "test": test,
            "pole": pole,
            "distance_cm": distance_text,
            "samples": len(voltage_values),
            "average_raw": average_raw,
            "average_voltage": average_voltage,
            "voltage_standard_deviation":
                voltage_standard_deviation,
        }
    )


# --------------------------------------------------
# SAVE THE SUMMARY CSV
# --------------------------------------------------

with summary_file.open(
    mode="w",
    newline="",
    encoding="utf-8",
) as csv_file:

    fieldnames = [
        "test",
        "pole",
        "distance_cm",
        "samples",
        "average_raw",
        "average_voltage",
        "voltage_standard_deviation",
    ]

    writer = csv.DictWriter(
        csv_file,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    for row in summary_rows:
        writer.writerow(
            {
                "test": row["test"],
                "pole": row["pole"],
                "distance_cm": row["distance_cm"],
                "samples": row["samples"],
                "average_raw":
                    f'{row["average_raw"]:.2f}',
                "average_voltage":
                    f'{row["average_voltage"]:.4f}',
                "voltage_standard_deviation":
                    f'{row["voltage_standard_deviation"]:.6f}',
            }
        )


# --------------------------------------------------
# FIND THE BASELINE VOLTAGE
# --------------------------------------------------

baseline_voltages = []

for row in summary_rows:
    pole_name = row["pole"].lower()

    if pole_name in {"none", "baseline", "no_magnet"}:
        baseline_voltages.append(
            row["average_voltage"]
        )

if baseline_voltages:
    baseline_voltage = mean(baseline_voltages)
else:
    baseline_voltage = None


# --------------------------------------------------
# PREPARE PLOT DATA
# --------------------------------------------------

plot_data = defaultdict(list)

for row in summary_rows:
    pole_name = row["pole"].lower()
    distance_text = row["distance_cm"]

    # Skip the no-magnet baseline for the distance plot
    if pole_name in {"none", "baseline", "no_magnet"}:
        continue

    try:
        distance = float(distance_text)
    except ValueError:
        continue

    plot_data[row["pole"]].append(
        (
            distance,
            row["average_voltage"],
            row["voltage_standard_deviation"],
        )
    )


# --------------------------------------------------
# CREATE THE GRAPH
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 6))

for pole, values in plot_data.items():
    values.sort(key=lambda item: item[0])

    distances = [
        item[0]
        for item in values
    ]

    average_voltages = [
        item[1]
        for item in values
    ]

    voltage_errors = [
        item[2]
        for item in values
    ]

    ax.errorbar(
        distances,
        average_voltages,
        yerr=voltage_errors,
        marker="o",
        capsize=4,
        label=pole.replace("_", " ").title(),
    )

if baseline_voltage is not None:
    ax.axhline(
        baseline_voltage,
        linestyle="--",
        label=(
            f"Baseline: "
            f"{baseline_voltage:.3f} V"
        ),
    )

ax.set_title(
    "49E Hall Sensor Voltage vs. Magnet Distance"
)

ax.set_xlabel("Magnet distance (cm)")
ax.set_ylabel("Average sensor voltage (V)")

ax.grid(True)
ax.legend()

fig.tight_layout()
fig.savefig(graph_file, dpi=300)

print("Hall sensor analysis complete.")
print(f"Summary saved to: {summary_file}")
print(f"Graph saved to: {graph_file}")

if baseline_voltage is not None:
    print(
        f"Average baseline voltage: "
        f"{baseline_voltage:.4f} V"
    )

plt.show()