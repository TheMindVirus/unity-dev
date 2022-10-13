# Vertex Ordering is Flawed

The order of the vertices in the default Unity Cube Primitive is incorrect. \
It runs fragments 24 times from each corner of each side and the back face is interleaved with the top face. \
This is especially visible in the recorded videos which automate the selected SV_VertexID group. \
It should be noted that this is different from SV_InstanceID, shown in the different respective shaders. \
This is different again for Particle Instancing which provides the correct float3x4 object transform \
(position, rotation, scale [xyzw]) which both the default and Instancing shaders do not obtain. 

![screenshot](/VertexOrdering/screenshot.png)
![screenshot2](/VertexOrdering/screenshot2.png)
The Model-View-Projection matrix is also being wrongly upgraded by Unity which also produces \
inconsistent line endings on Windows which needs to be fixed by Notepad++. \
The above example was required for drawing Billboards on default Cube mentioned previously.

However, while this appears to draw and texture the Billboard, it does not respond correctly \
to fragment shader code to cull the square into a circle of radius 0.5.

Other such ranges are -0.5->0.5 for vertices (should be -1.0->1.0 for local space) \
and vertex position which gets pre-multiplied by \_ScreenParams to give the fragment position. \
This needs to be divided back down, multiplied by 2.0 and then -1.0 to give a range of -1.0->1.0.

The Workaround for this is to use sampler2D and GrabPass to shade a circle on-screen, \
restore the context with the grab pass (because there's no way of writing to sampler2D, backwards tex2D) \
and draw the framebuffer onto the billboard with alpha masked.

Unity CG and ShaderLab do not know the concept of Push/Pop of graphics contexts like GLES does. \
The outcome of using the grab pass is visual defects, input vertices multiplied by -2.0 and \
no option to turn off visibility culling for when a 2D shader is actually 3D and goes off-screen.

![screenshot3](/VertexOrdering/screenshot3.png)
```
/*
something has happened there...x is looking correct...but y, z and w are offset...
y and z are both 0.0, x and w are not 0.0, w is behaving consistently with the y axis...almost like a Vector3 alignment error
[x, .., .., y] .., .., z, .., .., w, .., ..
compiler rule will only let you read subscript [0]->[3], not any further where the data is
*/
```
The particle transform property is a float3x4 which is laid out with the following information:
```
/*
input.data.transform[0].x = Scale X
input.data.transform[0].y = Rotation Z
input.data.transform[0].z = Rotation Y
input.data.transform[0].w = Position X
input.data.transform[1].x = Rotation Z (Again?)
input.data.transform[1].y = Scale Y
input.data.transform[1].z = Rotation X
input.data.transform[1].w = Position Y
input.data.transform[2].x = Rotation Y (Again?)
input.data.transform[2].y = Rotation X (Again?)
input.data.transform[2].z = Scale Z
input.data.transform[2].w = Position Z
*/
```
![screenshot4](/VertexOrdering/screenshot4.png)

It should perhaps be laid out a bit more like this:
![screenshot5](/VertexOrdering/screenshot5.png)
Further to this, to remap the vertices back to something usable as a local position for a shader,
this mapping has to be added into the vertex program for Unity's primitive default cube:
```
uint id : SV_VERTEXID;
...
input.id = input.id % 24; //Only works on Unity 2021 Default Cube to circumvent WebGL Batching For Particles
if ((input.id ==  0) || (input.id == 13) || (input.id == 23)) { output.local = float3( 0.5, -0.5,  0.5); } //Magenta Corner
if ((input.id ==  1) || (input.id == 14) || (input.id == 16)) { output.local = float3(-0.5, -0.5,  0.5); } //Blue Corner
if ((input.id ==  2) || (input.id ==  8) || (input.id == 22)) { output.local = float3( 0.5,  0.5,  0.5); } //Most Significant Bit
if ((input.id ==  3) || (input.id ==  9) || (input.id == 17)) { output.local = float3(-0.5,  0.5,  0.5); } //Cyan Corner
if ((input.id ==  4) || (input.id == 10) || (input.id == 21)) { output.local = float3( 0.5,  0.5, -0.5); } //Yellow Corner
if ((input.id ==  5) || (input.id == 11) || (input.id == 18)) { output.local = float3(-0.5,  0.5, -0.5); } //Green Corner
if ((input.id ==  6) || (input.id == 12) || (input.id == 20)) { output.local = float3( 0.5, -0.5, -0.5); } //Red Corner
if ((input.id ==  7) || (input.id == 15) || (input.id == 19)) { output.local = float3(-0.5, -0.5, -0.5); } //Least Significant Bit
```
The Unity_ObjectToWorld matrix is similar to the first above float3x4 matrix but is a 4x4 matrix laid out the same way as the 3x4 one. \
This is consistent across all of Unity's transformation matrices and makes implementing multiplication for rotation a bit more complex.

These matrices are not filled in for particles and it is expected that only in Direct3D11 that you must use the input position or the \
Standard Particle Instancing extensions to get this data. This will then be different for e.g. a WebGL build. \
The hand-encoded local position remains a constant point of reference but a custom vertex stream must be added to offset 3D Rotation.
