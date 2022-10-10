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
to fragment shader code to cull the square into a circle of radius 0.5. \
Other such ranges are -0.5->0.5 for vertices (should be -1.0->1.0 for local space) \
and vertex position which gets multiplied by the screen resolution to give the fragment position.

The Workaround for this is to use sampler2D and GrabPass to shade a circle on-screen, \
restore the context with the grab pass (because there's no way of writing to sampler2D, backwards tex2D) \
and draw the framebuffer onto the billboard with alpha masked.

Unity CG and ShaderLab do not know the concept of Push/Pop of graphics contexts like GLES does. \
The outcome of using the grab pass is visual defects, input vertices multiplied by -2.0 and \
no option to turn off visibility culling for when a 2D shader is actually 3D and goes off-screen.
