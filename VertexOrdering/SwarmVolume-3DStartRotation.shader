Shader "Swarm/Volume"
{
    Properties
    {
        _Color("Colour", Color) = (1,1,1,1)
        _Texture("Texture", 3D) = ""
        _Steps("Steps", Float) = 256
        _DebugRotation("DebugRotation", Vector) = (0,0,0,0)
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Opaque" }
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Front
        ZWrite Off
        ZTest LEqual //NotEqual //"SortMode" = "ByDepth" also helps in the particle renderer settings

        Pass
        {
            CGPROGRAM
            #pragma target 4.0
            #pragma vertex vertex_shader
            #pragma fragment fragment_shader
            #include "UnityCG.cginc"
            #include "UnityStandardParticleInstancing.cginc"
            #define PI    3.141592653589793
            #define TAU   6.283185307179586

            float4 _Color;
            sampler3D _Texture;
            uint _Steps;
            float4 _DebugRotation;

            struct supplied //ideally use appdata_full
            {
                float3 vertex : POSITION;
                float3 normal : NORMAL;
                float3 tangent : TANGENT;
                float4 texcoord0 : TEXCOORD0; //Turn Custom Texture Stream On and send it 3D Rotation xyz!
                float4 texcoord1 : TEXCOORD1;
                float4 texcoord2 : TEXCOORD2;
                float4 texcoord3 : TEXCOORD3;
                uint id : SV_VERTEXID;
            };

            struct data
            {
                float3 vertex : AV_VERTEX;
                float4 screen : SV_POSITION;
                float3 local : AV_LOCAL;
                float3 world : AV_WORLD;
                float3 center : AV_CENTER;

                float4 texcoord0 : AV_TEXCOORD0;
                float4 texcoord1 : AV_TEXCOORD1;
                float4 texcoord2 : AV_TEXCOORD2;
                float4 texcoord3 : AV_TEXCOORD3;

                float3 position : UNITY_POSITION;
                float3 rotation : UNITY_ROTATION;
                float3 scale : UNITY_SCALE;

                float3 normal : AV_NORMAL;
                float3 tangent : AV_TANGENT;

                float3 id : AV_ID;
            };

            data vertex_shader(supplied input)
            {
                data output;
                output.vertex = input.vertex;
                output.screen = UnityObjectToClipPos(input.vertex);
                output.local = float3(0.0, 0.0, 0.0);
                input.id = input.id % 24; //Only works on Unity 2021 Default Cube to circumvent WebGL Batching
                if ((input.id ==  0) || (input.id == 13) || (input.id == 23)) { output.local = float3( 0.5, -0.5,  0.5); } //Magenta Corner
                if ((input.id ==  1) || (input.id == 14) || (input.id == 16)) { output.local = float3(-0.5, -0.5,  0.5); } //Blue Corner
                if ((input.id ==  2) || (input.id ==  8) || (input.id == 22)) { output.local = float3( 0.5,  0.5,  0.5); } //Most Significant Bit
                if ((input.id ==  3) || (input.id ==  9) || (input.id == 17)) { output.local = float3(-0.5,  0.5,  0.5); } //Cyan Corner
                if ((input.id ==  4) || (input.id == 10) || (input.id == 21)) { output.local = float3( 0.5,  0.5, -0.5); } //Yellow Corner
                if ((input.id ==  5) || (input.id == 11) || (input.id == 18)) { output.local = float3(-0.5,  0.5, -0.5); } //Green Corner
                if ((input.id ==  6) || (input.id == 12) || (input.id == 20)) { output.local = float3( 0.5, -0.5, -0.5); } //Red Corner
                if ((input.id ==  7) || (input.id == 15) || (input.id == 19)) { output.local = float3(-0.5, -0.5, -0.5); } //Least Significant Bit
                output.position = float3(unity_ObjectToWorld[0].w,
                                         unity_ObjectToWorld[1].w,
                                         unity_ObjectToWorld[2].w); //But not for particles...
                output.rotation = float3(abs(unity_ObjectToWorld[1].z) + abs(unity_ObjectToWorld[2].y), //This is daft encoding
                                         abs(unity_ObjectToWorld[0].z) + abs(unity_ObjectToWorld[2].x), //ArcSine of this returns 2 results
                                         abs(unity_ObjectToWorld[0].y) + abs(unity_ObjectToWorld[1].x)); //But not for particles...they're linear
                output.scale    = float3(unity_ObjectToWorld[0].x,
                                         unity_ObjectToWorld[1].y,
                                         unity_ObjectToWorld[2].z); //But not for particles...
                output.world = output.vertex + output.position; //This will probably break when they fix this
                output.center = (output.world - output.local);
                output.normal = UnityObjectToWorldNormal(input.normal);
                output.tangent = input.tangent;
                output.texcoord0 = input.texcoord0;
                output.texcoord1 = input.texcoord1;
                output.texcoord2 = input.texcoord2;
                output.texcoord3 = input.texcoord3;
                output.id = input.id;
                return output;
            }

            float3 sq_rt(float3 value)
            {
                return float3((value.r >= 0.0) ? pow(value.r, 0.5) : -pow(-value.r, 0.5),
                              (value.g >= 0.0) ? pow(value.g, 0.5) : -pow(-value.g, 0.5),
                              (value.b >= 0.0) ? pow(value.b, 0.5) : -pow(-value.b, 0.5));
            }

            float3 cb_rt(float3 value)
            {
                float onethird = 1.0 / 3.0;
                return float3((value.r >= 0.0) ? pow(value.r, onethird) : -pow(-value.r, onethird),
                              (value.g >= 0.0) ? pow(value.g, onethird) : -pow(-value.g, onethird),
                              (value.b >= 0.0) ? pow(value.b, onethird) : -pow(-value.b, onethird));
            }

            float3 radius(float3 value) { return sq_rt(pow(value.r, 2) + pow(value.g, 2) + pow(value.b, 2)); }
            float3 inv_radius(float3 value) { return 1.0 - sq_rt(pow(value.r, 2) + pow(value.g, 2) + pow(value.b, 2)); }

            float3 sphere2cube(float3 value) //expects inv_radius() or cube2sphere()
            {
                return float3(value.r * (value.r + (sqrt(2) * min(min(value.r, value.g), value.b))),
                              value.g * (value.g + (sqrt(2) * min(min(value.r, value.g), value.b))),
                              value.b * (value.b + (sqrt(2) * min(min(value.r, value.g), value.b))));
            }
            float3 cube2sphere(float3 value) { return inv_radius(value); }

            //float3 visualiser(float3 value) { return radius(value) * (1.0 + (value - inv_radius(value))); }
            float3 visualiser(float3 value)
            {
                value *= 0.5;
                float3 r = radius(value);
                float3 ir = 1.0 - r;
                return float3(r.r * (1.0 + (value.r - ir.r)),
                              r.g * (1.0 + (value.g - ir.g)),
                              r.b * (1.0 + (value.b - ir.b)));
            }

            float3 rotate(float3 pos, float3 value, float3 pivot = float3(0.0, 0.0, 0.0))
            {
                float3 remap = float3(value.y, value.x, value.z);
                float3 moved = pos - pivot;
                float3x3 _matrix;
                _matrix[0].x = cos(remap.x) * cos(remap.z);
                _matrix[0].y = (-1.0 * cos(remap.y) * sin(remap.z)) + (sin(remap.y) * sin(remap.x) * cos(remap.z));
                _matrix[0].z = (sin(remap.y) * sin(remap.z)) + (cos(remap.y) * sin(remap.x) * cos(remap.z));
                _matrix[1].x = cos(remap.x) * sin(remap.z);
                _matrix[1].y = (cos(remap.y) * cos(remap.z)) + (sin(remap.y) * sin(remap.x) * sin(remap.z));
                _matrix[1].z = (-1.0 * sin(remap.y) * cos(remap.z)) + (cos(remap.y) * sin(remap.x) * sin(remap.z));
                _matrix[2].x = (-1.0 * sin(remap.x));
                _matrix[2].y = sin(remap.y) * cos(remap.x);
                _matrix[2].z = cos(remap.y) * cos(remap.x);
                float3 rotated = float3((moved.x * _matrix[0].x) + (moved.y * _matrix[0].y) + (moved.z * _matrix[0].z),
                                        (moved.x * _matrix[1].x) + (moved.y * _matrix[1].y) + (moved.z * _matrix[1].z),
                                        (moved.x * _matrix[2].x) + (moved.y * _matrix[2].y) + (moved.z * _matrix[2].z));
                return rotated + pivot;
            }

            float4 fragment_shader(data input) : COLOR
            {
/*
                float3 rgb = input.world;
                float a = 0.5;
                //float t = 1.0;
                //a = ((abs(input.center.x) <= t) && (abs(input.center.y) <= t) && (abs(input.center.z) <= t)) ? 0.5 : 0.0;
                //rgb = inv_radius(input.local - 0.5);
                //a = 0.5 * rgb.r;
                return float4(rgb, a);
*/
///*
                float4 output;
                float3 origin = input.local + 0.5;
                //float3 direction = ObjSpaceViewDir(float4(input.world, 1.0)); //The 0.5 should be done in vertex shader
                float3 direction = normalize(_WorldSpaceCameraPos.xyz - input.world);

                //!!!Serious Bug Here with x-axis of 3D Start Rotation, otherwise it correctly offsets Y and Z Dual Rotation
                direction = rotate(direction, (-sin(input.texcoord0.xyz / TAU) * TAU) + _DebugRotation); //Only for Particles
                //direction = rotate(direction, -input.rotation);
                //direction = rotate(direction, _DebugRotation, input.local);

                int tmp = _Steps; if (tmp < 0) { tmp = 0; }
                uint steps = tmp;
                const float stride = 2.0 / steps;

                float3 position = float3(0.0, 0.0, 0.0);
                origin += direction * stride;

                for (uint i = 0; i < steps; ++i)
                {
                    position = origin + (direction * (i * stride));
                    if ((position.x < 0.0 || position.x > 1.0)
                    ||  (position.y < 0.0 || position.y > 1.0)
                    ||  (position.z < 0.0 || position.z > 1.0)) { break; }
                    //should be continue or flag for compatibility on some systems

                    //position = rotate(position, _DebugRotation, float3(0.5, 0.5, 0.5));
                    float4 source = tex3Dlod(_Texture, float4(position.x, position.y, position.z, 0.0)) * _Color;
                    //float4 source = float4(direction, 0.5);
                    //float4 source = float4(input.texcoord0.xyz, 0.5);
                    //float4 source = float4(rotate(input.local, _DebugRotation.xyz), 0.5);
                    output.rgb = (output.rgb * (1.0 - source.a)) + (source.rgb * 0.5);
                    output.a = (output.a * (1.0 - source.a)) + (source.a * 0.5);
                }
                return output;
//*/
            }
            ENDCG
        }
    }
}
