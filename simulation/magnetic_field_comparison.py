from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# Particle properties: proton
particle_charge = 1.602e-19
particle_mass = 1.673e-27

# Initial velocity in meters per second
initial_velocity_x = 100_000.0
initial_velocity_y = 0.0

# Simulation settings
time_step = 5e-10
number_of_steps = 40_000

# Magnetic-field strengths to compare
magnetic_fields = [0.005, 0.01, 0.02]


def simulate_particle(magnetic_field):
    """Calculate a particle's trajectory for one magnetic-field value."""

    x_position = np.zeros(number_of_steps + 1)
    y_position = np.zeros(number_of_steps + 1)

    x_velocity = np.zeros(number_of_steps + 1)
    y_velocity = np.zeros(number_of_steps + 1)

    x_velocity[0] = initial_velocity_x
    y_velocity[0] = initial_velocity_y

    for step in range(number_of_steps):
        acceleration_x = (
            particle_charge
            / particle_mass
            * y_velocity[step]
            * magnetic_field
        )

        acceleration_y = (
            -particle_charge
            / particle_mass
            * x_velocity[step]
            * magnetic_field
        )

        x_velocity[step + 1] = (
            x_velocity[step] + acceleration_x * time_step
        )

        y_velocity[step + 1] = (
            y_velocity[step] + acceleration_y * time_step
        )

        x_position[step + 1] = (
            x_position[step]
            + x_velocity[step + 1] * time_step
        )

        y_position[step + 1] = (
            y_position[step]
            + y_velocity[step + 1] * time_step
        )

    return x_position, y_position


# Create the graph
fig, ax = plt.subplots(figsize=(8, 8))

# Run the simulation once for each magnetic field
for magnetic_field in magnetic_fields:
    x_position, y_position = simulate_particle(magnetic_field)

    ax.plot(
        x_position,
        y_position,
        label=f"B = {magnetic_field} T",
    )

ax.scatter(0, 0, s=60, label="Starting position")

ax.set_title("Effect of Magnetic Field on Proton Trajectory")
ax.set_xlabel("X position (meters)")
ax.set_ylabel("Y position (meters)")
ax.set_aspect("equal", adjustable="box")
ax.grid(True)
ax.legend()

fig.tight_layout()


# Save the result
project_folder = Path(__file__).resolve().parents[1]
results_folder = project_folder / "graphs"
results_folder.mkdir(exist_ok=True)

output_file = results_folder / "magnetic_field_comparison.png"

fig.savefig(output_file, dpi=300)

print(f"Graph saved to: {output_file}")

plt.show()