import tkinter as tk
import math
import random

def generate_mountain_range(width, height, num_mountains, peakiness, color):
    # Create a tkinter canvas with the given width and height
    canvas = tk.Canvas(width=width, height=height)

    # Generate a random seed value for the Perlin noise algorithm
    seed = random.randint(0, 100000)

    # Loop over the number of mountains to generate
    for i in range(num_mountains):
        # Calculate the peak height and width of the mountain
        peak_height = random.uniform(0.1, 0.5) * height
        peak_width = random.uniform(0.2, 0.5) * width

        # Generate a random x-coordinate for the left edge of the mountain
        x_offset = random.uniform(0, width - peak_width)

        # Create a list of points for the mountain shape
        mountain_points = []
        for x in range(int(x_offset), int(x_offset + peak_width)):
            # Calculate the y-coordinate for the mountain point using Perlin noise
            y = peakiness * peak_height * (1 + math.perlin(x / 100, seed))

            # Append the point to the mountain shape list
            mountain_points.append(x)
            mountain_points.append(height - y)

        # Close the mountain shape by adding the bottom right and bottom left corners
        mountain_points.append(int(x_offset + peak_width))
        mountain_points.append(height)
        mountain_points.append(int(x_offset))
        mountain_points.append(height)

        # Create a polygon object with the mountain shape points and add it to the canvas
        canvas.create_polygon(mountain_points, fill=color, outline=color)

    # Return the canvas object
    return canvas
# Create a tkinter window with a mountain range
root = tk.Tk()
canvas = generate_mountain_range(800, 600, 5, 0.1, "grey")
canvas.pack()

# Run the tkinter main loop
root.mainloop()