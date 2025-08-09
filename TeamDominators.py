import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import combinations
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

print("\n3D SHAPE VIEWER PRO")
print("------------------")

# Password Protection
password = "hacksphere"
user_input = input("Enter password: ")

if user_input != password:
    print("Access denied! Wrong password.")
    exit()

# Shape Menu
print("\nAvailable Shapes:")
print("1. Cube")
print("2. Sphere")
print("3. Pyramid")
print("4. Cylinder")
print("5. Cone")

shape_choice = input("\nEnter shape number (1-5): ")

# Parameters
try:
    size = float(input("Enter size (0.5-5): ") or 1.0)
    color = input("Enter color (r=red, g=green, b=blue, etc.): ") or 'b'
    transparency = float(input("Enter transparency (0-1): ") or 0.7)
except:
    print("Invalid input! Using defaults.")
    size, color, transparency = 1.0, 'b', 0.7

# Create Figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.grid(True)

# Shape Drawing Functions
def draw_cube():
    r = [-size, size]
    for s, e in combinations([(x, y, z) for x in r for y in r for z in r], 2):
        if sum([a != b for a, b in zip(s, e)]) == 1:
            ax.plot3D(*zip(s, e), color=color, linewidth=2, alpha=transparency)
    if size == 3.14:
        ax.text(0, 0, 0, "PI CUBE", color='gold', fontsize=12, ha='center')
    plt.title("3D Cube")

def draw_sphere():
    u = np.linspace(0, 2 * np.pi, 50)
    v = np.linspace(0, np.pi, 50)
    x = size * np.outer(np.cos(u), np.sin(v))
    y = size * np.outer(np.sin(u), np.sin(v))
    z = size * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color=color, alpha=transparency)
    plt.title("3D Sphere")

def draw_pyramid():
    vertices = [
        [0, 0, size],
        [-size, -size, 0],
        [size, -size, 0],
        [size, size, 0],
        [-size, size, 0]
    ]
    edges = [[0,1], [0,2], [0,3], [0,4], [1,2], [2,3], [3,4], [4,1]]
    for edge in edges:
        ax.plot3D(*zip(vertices[edge[0]], vertices[edge[1]]), color=color, lw=2)
    
    faces = [
        [vertices[0], vertices[1], vertices[2]],
        [vertices[0], vertices[2], vertices[3]],
        [vertices[0], vertices[3], vertices[4]],
        [vertices[0], vertices[4], vertices[1]],
        [vertices[1], vertices[2], vertices[3], vertices[4]]
    ]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, alpha=transparency))
    plt.title("3D Pyramid")

def draw_cylinder():
    theta = np.linspace(0, 2*np.pi, 50)
    z = np.linspace(0, size, 10)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = size * np.cos(theta_grid)
    y_grid = size * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=transparency)
    
    # Add caps
    ax.plot_trisurf(size*np.cos(theta), size*np.sin(theta), np.zeros_like(theta), color=color, alpha=transparency)
    ax.plot_trisurf(size*np.cos(theta), size*np.sin(theta), np.ones_like(theta)*size, color=color, alpha=transparency)
    plt.title("3D Cylinder")

def draw_cone():
    theta = np.linspace(0, 2*np.pi, 50)
    z = np.linspace(0, size, 10)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = (size - z_grid) * np.cos(theta_grid)
    y_grid = (size - z_grid) * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=transparency)
    
    # Base
    ax.plot_trisurf(size*np.cos(theta), size*np.sin(theta), np.zeros_like(theta), color=color, alpha=transparency)
    plt.title("3D Cone")

# Shape Selection
shapes = {
    '1': draw_cube,
    '2': draw_sphere,
    '3': draw_pyramid,
    '4': draw_cylinder,
    '5': draw_cone
}

if shape_choice in shapes:
    shapes[shape_choice]()
else:
    print("Invalid choice! Exiting.")
    exit()

# Auto-Rotation Animation
ani = FuncAnimation(fig, lambda frame: ax.view_init(elev=20, azim=frame),
                  frames=360, interval=50, repeat=True)

print("\nClose the window to exit.")
plt.tight_layout()
plt.show()