---
layout: post
title:  Creating a background for Fortune Street
---

# Introduction

This is a blog post how I will be creating a new background for Fortune Street. What I want to do is to create a simple background using public sources like [sketchfab.com](https://sketchfab.com) and use it to create a new background for Fortune Street. 

At this point I would like to give a special thanks to nikkums for the very first guide how to get 3d models into Fortune Street.

## Step 1: Getting the background to load in blender

So I'm heading over to sketchfab and search for a some terms to find a background I would like to use. 
![Sketchfab Search](/assets/images/sketchfab_search.png)

So there are lots of cool 3d models you can find. After some looking around I decided to pick the [Floating Space Rocks](https://sketchfab.com/3d-models/floating-space-rocks-018829759661494080f08368bb742ca4).
![Sketchfab Floating Space Rocks](/assets/images/sketchfab_floating_space_rocks.png)

Shoutout to [dark-minaz](https://sketchfab.com/dark-minaz) for this cool floating space rocks model. It's giving me some Smash Bros Final Destination vibes, which is why I decided to go for it.

So I download it in .obj format and open it up in Blender. Whenever Blender starts, it will give you a default scene with some default objects. So I delete these objects first and then I use the File->Import->Wavefront (.obj) dialog to load the Floating Space Rocks scene into Blender.
![Delete Default Objects](/assets/images/blender_delete_initial_stuff.png)

Now after importing it, it seems to have lost its textures and looks very strange.
![Strange](/assets/images/floating_rocks_blender_imported.png)

So lets fix it by assigning the materials of the Rocks object a Base Color as Image. I select the emissive.jpeg texture which has been provided alongside the model download. After playing around with the Color Space values, I'm kinda satisfied with the results.
![Textures Assigned](/assets/images/floating_rocks_blender_textures_assigned.png)

However, now we may notice that the model has a lot of polygons. This may be too much to handle for our poor Wii hardware. So lets assign a `simplify geometry` modifier to our model.