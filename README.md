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



# Final Assignemnt

## Load 3D Geometry
  - Downloaded object from The Stanford 3D Scanning Repository (https://graphics.stanford.edu/data/3Dscanrep/)
  - Used blender to create a wavefront
  - Used  PyWavefront library to load the object
  - When loading the object, the values were too small, so I scaled them up and placed them at WC 0, 0, 2
  - Also when resizing, I made it so that the the smallest to biggest z had a difference of 2

## Shading
  - Used Phong equation to calculate local illumination.
  - It simulates diffuce and speculat materials
  - It uses a materia class that has 3 fields
    - diffuce: the diffuce coefficient, that has 3 values, 1 for each color of the RGB
    - specular: the specular coefficient that has 3 values too
    - shininess: Shininess controls how sharp and concentrated the specular highlight is on a surface.
  - It also uses a lighting class
    - position: the position of the light
    - intensity: the intensity of the light for each color (3 values), from 0 to 1


### Example of Diffuse material
  - The light position is at 500, 500, -500
![armadillo_diffuse_1](https://github.com/user-attachments/assets/ec068029-7530-427b-ac15-10beb2dd0bc7)

### Example of Specular material
![armadillo_shiny_1](https://github.com/user-attachments/assets/62a51b9f-6a23-41ba-a859-82fd7374bc96)


## Camera
  - The camera has the following fields
    - position: the xyz position of the camera
    - look at vector: the xyz vector for where to look
    - up vector: the xyz vector for where is up
    - field of view: how wide the camera will be in angles

### Example of different cameras
  - Front View
![armadillo_shiny_1](https://github.com/user-attachments/assets/34ad039b-1144-40d5-ba07-0a070018f103)

  - Down View
![armadillo_shiny_4](https://github.com/user-attachments/assets/f9b74123-d125-4ef8-9afe-3b5e8c75fe08)

  - Up View
![armadillo_shiny_3](https://github.com/user-attachments/assets/cc38b47f-6c61-407a-b997-a5ac27b1bba1)

  - Back View
![armadillo_shiny_2](https://github.com/user-attachments/assets/7d9a9f8d-25b7-4b57-a7c2-94284a36cf3f)

  - Left View
![armadillo_shiny_5](https://github.com/user-attachments/assets/798a1ff6-fe46-4609-9f49-13e3ce9d091c)

  - Right View
![armadillo_shiny_6](https://github.com/user-attachments/assets/eb925fec-10ac-4cb8-b93c-f22a33888000)





