# Vertex Ordering is Flawed

The order of the vertices in the default Unity Cube Primitive is incorrect. \
It runs fragments 24 times from each corner of each side and the back face is interleaved with the top face. \
This is especially visible in the recorded videos which automate the selected SV_VertexID group. \
It should be noted that this is different from SV_InstanceID, shown in the different respective shaders.

![screenshot](/VertexOrdering/screenshot.png)
