plt.figure(figsize=(10, 6))
below_80 = costs < 80
above_80 = costs >= 80

# Plot costs that are below 80
plt.plot(percentages[below_80], costs[below_80], label='Costs below $80', color='blue')

# Plot costs that are equal to or above 80
plt.plot(percentages[above_80], costs[above_80], label='Costs at or above $80', color='red')

# Adding labels and title
plt.xlabel('Percentage Increase (%)')
plt.ylabel('Cost ($)')
plt.title('Evolution of Overcost from 1% to 20%')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
