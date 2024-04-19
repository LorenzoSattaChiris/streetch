import numpy as np
import matplotlib.pyplot as plt

# Define the starting number as a global variable
base_cost = 65.96

# Create a range of percentages from 1% to 20%
percentages = np.arange(1, 31)

# Calculate the costs for each percentage increase
costs = base_cost * (1 + percentages / 100)

# Plotting the evolution of overcost
# Improved plotting to ensure clear visibility of the color change
plt.figure(figsize=(10, 6))

# Determine the exact point where the cost crosses £80
crossing_point = np.argmax(costs >= 80)

# Adjusting segments to include the exact crossing point in both segments if needed
if costs[crossing_point] >= 80 and crossing_point != 0:
    # Include the crossing point in both segments
    plt.plot(percentages[:crossing_point], costs[:crossing_point], label='Costs below £80', color='blue')
    plt.plot(percentages[crossing_point-1:], costs[crossing_point-1:], label='Costs at or above £80', color='red')
else:
    plt.plot(percentages[below_80], costs[below_80], label='Costs below £80', color='blue')
    plt.plot(percentages[above_80], costs[above_80], label='Costs at or above £80', color='red')

# Adding labels, title and grid
plt.xlabel('Percentage Increase (%)')
plt.ylabel('Cost (£)')
plt.title('Evolution of Overcost')
plt.legend()
plt.grid(True)

# Show the updated plot
plt.show()
