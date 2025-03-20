# epl607_render

## Team members
  Stylanos Vassiliou

## The programming language you chose
  Python

## The image processing library you chose for that language
  PIL

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
