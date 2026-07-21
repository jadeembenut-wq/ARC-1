import numpy as np
import matplotlib.pyplot as plt

# Simplified normalized values for the first simulation
magnetic_field = 0.5
charge_to_mass_ratio = 1.0
initial_speed = 1.0
simulation_time = 12.0
number_of_points = 1_000

# Cyclotron angular frequency
angular_frequency = charge_to_mass_ratio * magnetic_field

# Time values
time = np.linspace(0, simulation_time, number_of_points)

# Radius of the circular path
radius = initial_speed / angular_frequency

# Simplified charged-particle trajectory
x_position = radius * np.sin(angular_frequency * time)
y_position = radius * (np.cos(angular_frequency * time) - 1)

# Create the graph
plt.figure(figsize=(7, 7))
plt.plot(x_position, y_position)

plt.title("ARC-1 Charged-Particle Simulation")
plt.xlabel("X position — normalized units")
plt.ylabel("Y position — normalized units")
plt.axis("equal")
plt.grid(True)

plt.savefig("graphs/initial_particle_trajectory.png", dpi=300)
plt.show()

print("ARC-1 simulation ran successfully.")