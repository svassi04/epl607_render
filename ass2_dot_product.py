from PIL import Image
import math

def project_vertex(v, width, height):
    """Project a 3D vertex and shift to screen center. Keeps original Z for depth."""
    if v[2] == 0:
        return (v[0], v[1], v[2])
    x = v[0] / v[2]
    y = v[1] / v[2]
    screen_x = int(x + width / 2)
    screen_y = int(height / 2 - y)
    return (screen_x, screen_y, v[2])

def projection(triangle, width, height):
    return tuple(project_vertex(v, width, height) for v in triangle)

def edge(a, b, p):
    """Edge function using cross product (dot product alternative for orientation)."""
    ab = (b[0] - a[0], b[1] - a[1])
    ap = (p[0] - a[0], p[1] - a[1])
    return ab[0]*ap[1] - ab[1]*ap[0]

def is_inside(p, v0, v1, v2):
    """Check if point is inside triangle using consistent edge signs."""
    d0 = edge(v0, v1, p)
    d1 = edge(v1, v2, p)
    d2 = edge(v2, v0, p)
    has_neg = (d0 < 0) or (d1 < 0) or (d2 < 0)
    has_pos = (d0 > 0) or (d1 > 0) or (d2 > 0)
    inside = not (has_neg and has_pos)

    # Compute weights only if inside
    if not inside:
        return False, (0, 0, 0)

    # Barycentric weights from edge areas
    area = edge(v0, v1, v2)
    if area == 0:
        return False, (0, 0, 0)
    w0 = edge(v1, v2, p) / area
    w1 = edge(v2, v0, p) / area
    w2 = edge(v0, v1, p) / area
    return True, (w0, w1, w2)

def draw_triangle(image, triangle, triangle_color, WIDTH, HEIGHT, depth_buffer):
    projected = projection(triangle, WIDTH, HEIGHT)
    v0, v1, v2 = projected

    min_x = max(min(v0[0], v1[0], v2[0]), 0)
    max_x = min(max(v0[0], v1[0], v2[0]), WIDTH - 1)
    min_y = max(min(v0[1], v1[1], v2[1]), 0)
    max_y = min(max(v0[1], v1[1], v2[1]), HEIGHT - 1)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            inside, (w0, w1, w2) = is_inside((x, y), v0, v1, v2)
            if inside:
                depth = w0 * v0[2] + w1 * v1[2] + w2 * v2[2]
                if depth < depth_buffer[x][y]:
                    depth_buffer[x][y] = depth
                    image.putpixel((x, y), triangle_color)

def main():
    WIDTH, HEIGHT = 200, 200
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    depth_buffer = [[float("inf") for _ in range(HEIGHT)] for _ in range(WIDTH)]

    # Vertices for a tilted 4-sided pyramid
    vertices = [
        (0, 50, 1),        # Top (peak)
        (-50, -50, 2),     # Base Left
        (50, -50, 2),      # Base Right
        (50, 50, 2),       # Base Back-Right
        (-50, 50, 2),      # Base Back-Left
    ]

    # Triangles to make the pyramid
    triangles = [
        ([vertices[0], vertices[1], vertices[2]], (255, 0, 0)),    # Front face
        ([vertices[0], vertices[2], vertices[3]], (0, 255, 0)),    # Right face
        ([vertices[0], vertices[3], vertices[4]], (0, 0, 255)),    # Back face
        ([vertices[0], vertices[4], vertices[1]], (255, 255, 0)),  # Left face
        ([vertices[1], vertices[2], vertices[3]], (100, 100, 100)), # Base 1
        ([vertices[1], vertices[3], vertices[4]], (100, 100, 100)), # Base 2
    ]

    

    for triangle, color in triangles:
        draw_triangle(image, triangle, color, WIDTH, HEIGHT, depth_buffer)

    image.save("pyramid.png", "PNG")
    image.show()

if __name__ == "__main__":
    main()
