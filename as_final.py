import pywavefront
from PIL import Image
import numpy as np
import math
from tqdm import tqdm

# ---------- Lighting and Material ----------

class Material:
    def __init__(self, diffuse, specular, shininess):
        self.diffuse = np.array(diffuse)
        self.specular = np.array(specular)
        self.shininess = shininess


class Light:
    def __init__(self, position, color):
        self.position = np.array(position)
        self.color = np.array(color)


def compute_phong(normal_cam, position_cam, light_pos_cam, light_color, material, two_sided=False):
    N = normal_cam / np.linalg.norm(normal_cam)
    L = light_pos_cam - position_cam
    L = L / np.linalg.norm(L)

    V = -position_cam
    V = V / np.linalg.norm(V)

    N_dot_L = max(0, np.dot(N, L))

    ambient = 0.3 * material.diffuse
    diffuse = material.diffuse * light_color * N_dot_L

    specular = np.zeros(3)
    if N_dot_L > 0:
        R = 2 * N * np.dot(N, L) - L
        R = R / np.linalg.norm(R + 1e-8)
        specular = material.specular * light_color * (max(0, np.dot(R, V)) ** material.shininess)

    result = ambient + diffuse + specular
    return np.clip(result, 0, 255).astype(np.uint8)


# ---------- Camera & Projection ----------

def look_at_matrix(eye, center, up):
    f = np.array(center) - np.array(eye)
    f = f / np.linalg.norm(f)

    u = np.array(up)
    u = u / np.linalg.norm(u)

    s = np.cross(f, u)
    s = s / np.linalg.norm(s)
    u = np.cross(s, f)

    rotation = np.vstack([s, u, -f])
    return rotation, np.array(eye)


def world_to_camera(P, rotation, eye):
    P = np.array(P)
    return rotation @ (P - eye)


def project_vertex(P_world, width, height, rotation, eye, fov_deg=60):
    P_cam = world_to_camera(P_world, rotation, eye)
    z = max(P_cam[2], 0.01)

    aspect_ratio = width / height
    fov_rad = math.radians(fov_deg)
    scale = math.tan(fov_rad / 2)

    x_ndc = (P_cam[0] / (scale * z)) / aspect_ratio
    y_ndc = (P_cam[1] / (scale * z))

    screen_x = int((x_ndc + 1) * width / 2)
    screen_y = int((1 - y_ndc) * height / 2)
    return (screen_x, screen_y, z)


def projection(triangle, width, height, rotation, eye, fov_deg):
    return tuple(project_vertex(v, width, height, rotation, eye, fov_deg) for v in triangle)


# ---------- Rasterization ----------

def draw_triangle(image, triangle, triangle_color, WIDTH, HEIGHT, depth_buffer, rotation, eye, fov_deg):
    projected = projection(triangle, WIDTH, HEIGHT, rotation, eye, fov_deg)
    v0, v1, v2 = projected

    v0 = (round(v0[0]), round(v0[1]), triangle[0][2])
    v1 = (round(v1[0]), round(v1[1]), triangle[1][2])
    v2 = (round(v2[0]), round(v2[1]), triangle[2][2])

    min_x = max(min(v0[0], v1[0], v2[0]), 0)
    max_x = min(max(v0[0], v1[0], v2[0]), image.width - 1)
    min_y = max(min(v0[1], v1[1], v2[1]), 0)
    max_y = min(max(v0[1], v1[1], v2[1]), image.height - 1)

    def edge_coeffs(A, B):
        a = B[1] - A[1]
        b = A[0] - B[0]
        c = B[0] * A[1] - A[0] * B[1]
        return a, b, c

    a0, b0, c0 = edge_coeffs(v1, v2)
    a1, b1, c1 = edge_coeffs(v2, v0)
    a2, b2, c2 = edge_coeffs(v0, v1)

    def edge_function(a, b, c, x, y):
        return a * x + b * y + c

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            E0 = edge_function(a0, b0, c0, x, y)
            E1 = edge_function(a1, b1, c1, x, y)
            E2 = edge_function(a2, b2, c2, x, y)

            if (E0 >= 0 and E1 >= 0 and E2 >= 0) or (E0 <= 0 and E1 <= 0 and E2 <= 0):
                area = edge_function(a0, b0, c0, v0[0], v0[1])
                if area == 0:
                    continue
                w0 = E0 / area
                w1 = E1 / area
                w2 = E2 / area
                depth = w0 * v0[2] + w1 * v1[2] + w2 * v2[2]

                if depth < depth_buffer[y][x]:
                    depth_buffer[y][x] = depth
                    image.putpixel((x, y), tuple(triangle_color))


# ---------- Model Loading ----------

def load_model(filename, desired_depth=1.0, camera_distance=5.0):
    scene = pywavefront.Wavefront(filename, collect_faces=True)
    triangles = []

    used_indices = [idx for mesh in scene.meshes.values() for face in mesh.faces for idx in face]
    used_vertices = [scene.vertices[i] for i in used_indices]

    zs = [v[2] for v in used_vertices]
    min_z = min(zs)
    max_z = max(zs)
    model_depth = max_z - min_z if max_z != min_z else 1.0

    scale = desired_depth / model_depth
    z_offset = camera_distance - (min_z * scale)

    print(f"Loading model: {filename}")
    for mesh in scene.meshes.values():
        for face in tqdm(mesh.faces, desc="Processing faces", unit="face", total=len(mesh.faces)):
            if len(face) == 3:
                v0 = scene.vertices[face[0]]
                v1 = scene.vertices[face[1]]
                v2 = scene.vertices[face[2]]

                v0 = np.array([v0[0] * scale, v0[1] * scale, v0[2] * scale + z_offset])
                v1 = np.array([v1[0] * scale, v1[1] * scale, v1[2] * scale + z_offset])
                v2 = np.array([v2[0] * scale, v2[1] * scale, v2[2] * scale + z_offset])

                triangles.append((v0, v1, v2))
    return triangles


# ---------- Rendering ----------

def render_scene(triangles, filename, position, direction, up, fov_deg, WIDTH, HEIGHT, light, material):
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")
    depth_buffer = [[float("inf") for _ in range(WIDTH)] for _ in range(HEIGHT)]

    position = np.array(position)
    direction = np.array(direction)
    center = position + direction

    rotation, _ = look_at_matrix(position, center, up)
    light_pos_cam = rotation @ (light.position - position)

    print(f"Rendering to: {filename}")
    for triangle in tqdm(triangles, desc="Rendering triangles", unit="triangle"):
        v0, v1, v2 = triangle
        normal_world = np.cross(v1 - v0, v2 - v0)
        if np.linalg.norm(normal_world) == 0:
            continue
        normal_world /= np.linalg.norm(normal_world)

        normal_cam = rotation @ normal_world
        center_world = (v0 + v1 + v2) / 3.0
        center_cam = rotation @ (center_world - position)

        if np.dot(normal_cam, -center_cam) <= 0:
            continue

        color = compute_phong(normal_cam, center_cam, light_pos_cam, light.color, material, two_sided=False)
        draw_triangle(image, triangle, color, WIDTH, HEIGHT, depth_buffer, rotation, position, fov_deg)

    image.save(filename)
    print(f"Saved: {filename}")
    image.show()


# ---------- Main ----------

def main():
    # ---- Config ----
    model_file = "armadillo.obj"
    output_prefix = "armadillo"
    desired_depth = 1.0
    camera_distance = 3.0
    WIDTH, HEIGHT = 1000, 1000
    fov_deg = 60

    light = Light(position=[0, 500, -500], color=[1.0, 1.0, 1.0])
    material = Material(diffuse=[200, 100, 100], specular=[255, 255, 255], shininess=32)

    camera_views = [
        ([0, 0, 0], [0, 0, -1], [0, 1, 0], fov_deg),
        ([0, 0, 6], [0, 0, 1], [0, 1, 0], fov_deg),
        ([0, 3, 3], [0, 1, 0], [0, 0, 1], fov_deg),
        ([0, -3, 3], [0, -1, 0], [0, 0, -1], fov_deg),
        ([3, 0, 3], [1, 0, 0], [0, 1, 0], fov_deg),
        ([-3, 0, 3], [-1, 0, 0], [0, 1, 0], fov_deg),
    ]

    # ---- Load Model ----
    triangles = load_model(model_file, desired_depth, camera_distance)

    # ---- Render Views ----
    for i, (pos, direction, up, fov) in enumerate(camera_views):
        filename = f"{output_prefix}_{i+1}.png"
        render_scene(triangles, filename, pos, direction, up, fov, WIDTH, HEIGHT, light, material)


if __name__ == "__main__":
    main()
