from PIL import Image, ImageDraw
import math 




def draw_triangle(image, triangle, triangle_color):

    v0, v1, v2 = triangle

    # Compute bounding box and clip to screen limits
    min_x = max(min(v0[0], v1[0], v2[0]), 0)
    max_x = min(max(v0[0], v1[0], v2[0]), image.width - 1)
    min_y = max(min(v0[1], v1[1], v2[1]), 0)
    max_y = min(max(v0[1], v1[1], v2[1]), image.height - 1)

    # Compute edge properties
    # a0, b0, c0 = v1[1] - v2[1], v2[0] - v1[0], v1[0] * v2[1] - v2[0] * v1[1]
    # a1, b1, c1 = v2[1] - v0[1], v0[0] - v2[0], v2[0] * v0[1] - v0[0] * v2[1]
    # a2, b2, c2 = v0[1] - v1[1], v1[0] - v0[0], v0[0] * v1[1] - v1[0] * v0[1]

    a0, b0, c0 = v2[1] - v1[1], v1[0] - v2[0], v2[0] * v1[1] - v1[0] * v2[1]
    a1, b1, c1 = v0[1] - v2[1], v2[0] - v0[0], v0[0] * v2[1] - v2[0] * v0[1]
    a2, b2, c2 = v1[1] - v0[1], v0[0] - v1[0], v1[0] * v0[1] - v0[0] * v1[1]


    # Iterate over each pixel
    for y in range(min_y, max_y + 1):        
        for x in range(min_x, max_x + 1):
            # EvCalculatealuate edge equations 
            E0 = a0 * x + b0 * y + c0
            E1 = a1 * x + b1 * y + c1
            E2 = a2 * x + b2 * y + c2
            # print (E0, E1, E2)
            # Check if the point is left or right of all edges
            if E0 >= 0 and E1 >= 0 and E2 >= 0:
                # Sets a pixel on the image if within bounds
                if 0 <= x < image.width and 0 <= y < image.height:
                    image.putpixel((x, y), triangle_color)
            


def main():
# Image size (width, height)
    WIDTH, HEIGHT = 1024, 720
    triangle = [(250, 150), (150, 600), (850, 300)]
    triangle_color = (255, 0, 0)  # Red color


    # Create a blank white image
    image = Image.new("RGB", (WIDTH, HEIGHT), "white")

    draw_triangle(image, triangle, triangle_color)

    # Save or show the image
    image.show()  # Opens the image viewer
    image.save("red_triangle.png", "PNG")


main()
