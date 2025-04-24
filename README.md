# epl607_render

## Team members
  Stylanos Vassiliou

## The programming language you chose
  Python

## The image processing library you chose for that language
  PIL

# Assignemnt 1

## The process you used to render your test triangle
  - To render my triangle, I used the rusterizaton process.
  - I gave the program the 3 points of the triangle, its color, and the size of the image (coded in the program)
  - It creates the bounding box by finding the minimum and maximum between the 3 points and the border, so that it will iterate only through the pixels within those bounds
  - Then I calculate the a, b and c for each edge for the equation E(x, y) = ax + by + c
    - a is the rate of change on the edge for x
    - b is the rate of change on the edge for y
    - c is the point where the line intersects with the x-axis
  - I then iterate over each pixel and check if it is within or at the edges, meaning that the E(x, y) = ax + by + c is positive for all 3, it colors it
    - by replacing the x,y with those of the pixel, i basicaly compare the position of the pixel relative of the line, to find if it is left, right, or on the line.
    - If it is right (or left) of all the lines, or on them, then it means that it is inside the triangle, or on it.

## The test image you created
![red_triangle](https://github.com/user-attachments/assets/1ecfcc98-22c5-4802-9ed6-d17f297255b4)


# Assignemnt 2


## Projection
  - First, to project an image, we have to move the triangles so that the center of the image is the 0,0. By default, the 0,0 is the top left corner
  - Then we divide x and y by z, to place the triangles in their correct projected position. If the depth is 0, we ignore the triangle

## Rasterizarion
 - The process is still, mostly the same as in Assignment 1
 - After Projection a triangle, it finds its bounding boxes
 - For each pixel:
   - It calculates the 3 edges and finds if a point os in the triangle
   - It gives a weight of how close a point is to the 3 vertexes of the triangle, to calculate the point's depth. This helps determine the color of triangles overlap, or clip
   - Finaly, if the depth is smaller than the current depth of the  pixel, it colors it, and adds the depth to a depth buffer
  
## Example image of overlapping triangles
![triangles](https://github.com/user-attachments/assets/df0e2d89-1cb6-49b1-8cfe-d588d98adf16)


## Example image of clipping triangles
![triangles_clipping](https://github.com/user-attachments/assets/7568fb4e-000f-41c3-883e-3ef7545cb95d)


## Example image of a pyramid
![pyramid](https://github.com/user-attachments/assets/7e52ae07-1b7e-432d-b734-fe2dd7a30534)


