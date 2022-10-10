Shader "VolumeRendering/SwarmVolumeShader"
{
    Properties
    {
        _Color("Colour", Color) = (1,1,1,1)
        _Texture("Texture", 3D) = "" {}
        _Steps("Steps", Float) = 512
        _Frame("Frame", Float) = 0
        _DebugOrigin("DebugOrigin", Vector) = (0,0,0,0)
        _DebugDirection("DebugDirection", Vector) = (0,0,0,0)
        _DebugScale("DebugScale", Vector) = (1,1,1,1)
    }
    SubShader //Input Vertex Data is Wildly Offset by known value...
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Transparent" }
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Front
        //ZWrite Off
        //ZTest LEqual //NotEqual

        Pass
        {
            CGPROGRAM
            #pragma exclude_renderers gles //This had better compile on WebGL though
            #pragma target 4.0
            #pragma vertex vertex_shader
            #pragma fragment fragment_shader
            #pragma multi_compile_instancing //This defines INSTANCING_ON which breaks positioning
            #pragma instancing_options procedural:vertInstancingSetup
            #define UNITY_PARTICLE_INSTANCE_DATA particle
            struct particle
            {
                float3x4 transform;
                uint color;
                float speed;
            };
            #define UNITY_PARTICLE_INSTANCE_DATA_NO_ANIM_FRAME
            #include "UnityCG.cginc"
            #include "UnityStandardParticleInstancing.cginc" //Must be this way round
            //#include "Lighting.cginc"
            //#include "AutoLight.cginc"

            float4 _Color;
            sampler3D _Texture;
            uint _Steps;
            uint _Frame;
            float4 _DebugOrigin;
            float4 _DebugDirection;
            float4 _DebugScale;

            struct supplicant //ideally use appdata_full
            {
                #if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                float3 vertex : POSITION;
                float3 normal : NORMAL;
                float4 color : COLOR;
                float2 texcoord : TEXCOORD0; //As per default custom vertex streams
                UNITY_VERTEX_INPUT_INSTANCE_ID
                #else
                float3 vertex : POSITION;
                float3 normal : NORMAL;
                float2 texcoord : TEXCOORD0;
                #endif
            };

            struct data
            {
                float4 vertex : SV_POSITION;
                float3 normal : NORMAL;
                float2 texcoord : TEXCOORD0;
                float3 blend : TEXCOORD20;
                float4 color : INSTANCED0;
                float3 unmodified : TEXCOORD21;
                #if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                UNITY_PARTICLE_INSTANCE_DATA data : TEXCOORD1;
                #endif
            };

            data vertex_shader(supplicant input)
            {
                data output;
                output.unmodified = input.vertex;
                output.texcoord = input.texcoord;
                #if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                UNITY_SETUP_INSTANCE_ID(input);
                vertInstancingColor(input.color);
                vertInstancingUVs(input.texcoord, output.texcoord, output.blend);
                output.data = unity_ParticleInstanceData[unity_InstanceID];
                output.color = input.color;
                #else
                output.color = _Color;
                output.blend = output.color;
                #endif
                output.vertex = UnityObjectToClipPos(input.vertex);
                output.normal = UnityObjectToWorldNormal(input.normal);
                return output;
            }

            float4 fragment_shader(data input) : COLOR
            {
                float4 output;
                float4 previous;
                int tmp = _Steps; if (tmp < 0) { tmp = 0; }
                uint steps = tmp;
                const float stride = 2.0f / steps;

                #if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                //float3 input_vertex = input.blend; //float3(input.texcoord, 0.0); //input.vertex;
                float3 input_vertex = input.unmodified * _DebugScale.xyz; //input.unmodified; //This is offset/rotated
                #else
                float3 input_vertex = input.unmodified; //This is correct
                #endif
                
                float3 origin = input_vertex + float3(0.5f, 0.5f, 0.5f) + _DebugOrigin;
                float3 direction = normalize(ObjSpaceViewDir(float4(input_vertex, 0.0f))) * _DebugDirection;

                origin += direction * stride;

                for (uint i = 0; i < steps; ++i)
                {
                    float3 position = origin + direction * (i * stride);
                    if (position.x < 0.0f
                    ||  position.x > 1.0f
                    ||  position.y < 0.0f
                    ||  position.y > 1.0f
                    ||  position.z < 0.0f
                    ||  position.z > 1.0f) { break; }

                    float4 source = tex3Dlod(_Texture, float4(position.x, position.y, position.z, _Frame));
                    if (i == 0) { previous = source; }
                    //output = (previous + source) * 0.5f;
                    output.rgb = (source.rgb * 0.5f) + (1.0f - source.a) * (output.rgb);
                    output.a = (source.a * 0.5f) + (1.0f - source.a) * output.a;
                    previous = source;
                }
                #if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                //return output;
                //return float4(input.blend.xyz, 0.5);
                //return float4(input.data.Position.xyz, 0.5);
                //return float4(input.data.transform[0].xyz, 0.5);
                //return float4(1.0, 0.0, 0.0, 0.5);
                //return float4(input.unmodified, 0.5); //return float4(direction, 0.5); //These look fine
                //float4 ppp = float4(input.data.transform[0].xyz * input.data.transform[0].w, 0.5);
                float4 ppp = float4(input.data.transform[0].x * input.data.transform[0].w,
                                    input.data.transform[0].w, // * input.data.transform[0].w,
                                    input.data.transform[0].z, // * input.data.transform[0].w,
                                    0.5);
                //ppp.x = 0.0;
                //ppp.y = 0.0;
                //ppp.z = 0.0;
                ppp.y = (input.data.transform[0].x == 0.0) ? 1.0 : 0.0;
                return ppp; //Per-Particle Position??? //Vector3-based alignment error?
/*
something has happened there...x is looking correct...but y, z and w are offset...
y and z are both 0.0, x and w are not 0.0, w is behaving consistently with the y axis...almost like a Vector3 alignment error
[x, .., .., y] .., .., z, .., .., w, .., ..
compiler rule will only let you read subscript [0]->[3], not any further where the data is
*/
                #else
                return output;
                //return float4(input_vertex.xyz, 0.5);
                //return float4(0.0, 0.0, 1.0, 0.5);
                //return float4(input.unmodified, 0.5); //return float4(direction, 0.5); //These look fine
                #endif
            }
            ENDCG
        }
    }
}
