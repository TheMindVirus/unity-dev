//https://docs.unity3d.com/Manual/PartSysInstancing.html
//https://github.com/TwoTailsGames/Unity-Built-in-Shaders/blob/master/CGIncludes/UnityStandardParticles.cginc
//https://github.com/TwoTailsGames/Unity-Built-in-Shaders/blob/master/CGIncludes/UnityStandardParticleInstancing.cginc

Shader "Instanced/ParticleMeshesCustomStreams"
{
    Properties
    {
        _Color("Colour", Color) = (1.0, 1.0, 1.0, 1.0)
        _Texture("Texture", 3D) = "white" {}
        _Steps("Steps", Range(0, 512)) = 512
    }
    SubShader
    {
        Tags{ "Queue" = "Transparent" "RenderType" = "Transparent" }
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Front

        Pass
        {
            CGPROGRAM
            #pragma exclude_renderers gles
            #pragma vertex vert
            #pragma fragment frag
            #pragma multi_compile_instancing
            #pragma instancing_options procedural:vertInstancingSetup
            #define UNITY_PARTICLE_INSTANCE_DATA MyParticleInstanceData
            #define UNITY_PARTICLE_INSTANCE_DATA_NO_ANIM_FRAME
            struct MyParticleInstanceData
            {
                float3x4 transform;
                uint color;
                float speed;
            };
            #include "UnityCG.cginc"
            #include "UnityStandardParticleInstancing.cginc"
            struct appdata
            {
                float4 vertex : POSITION;
                fixed4 color : COLOR;
                float2 texcoord : TEXCOORD0;
                float3 normal : NORMAL;
                float4 unmodified : TEXCOORD1;
                UNITY_VERTEX_INPUT_INSTANCE_ID
            };
            struct v2f
            {
                float4 vertex : SV_POSITION;
                fixed4 color : COLOR;
                float2 texcoord : TEXCOORD0;
                float3 normal : NORMAL;
                float4 unmodified : TEXCOORD10;
#if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                UNITY_PARTICLE_INSTANCE_DATA data : TEXCOORD1;
#endif
            };
            uint _Steps;
            float4 _Color;
            sampler3D _Texture;
            float4 _MainTex_ST;
            v2f vert(appdata v)
            {
                v2f o;
                UNITY_SETUP_INSTANCE_ID(v);
                o.color = v.color;
                o.texcoord = v.texcoord;
                vertInstancingColor(o.color);
                vertInstancingUVs(v.texcoord, o.texcoord);
#if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                UNITY_PARTICLE_INSTANCE_DATA data = unity_ParticleInstanceData[unity_InstanceID];
                o.data = data;
                o.color.rgb += data.speed;
#endif
                o.vertex = UnityObjectToClipPos(v.vertex);
                o.normal = UnityObjectToWorldNormal(v.vertex);
                o.unmodified = v.vertex;
                return o;
            }
            float3 illuminate(float3 input, float3 normal, float3 light, float3 direction, float intensity)
            {
                float3 diffuse = input * dot(normal, light);
                float specular = pow(max(dot(normalize(reflect(-light, normal)), direction), 0.0f), intensity);
                return diffuse + specular;
            }
            fixed4 frag(v2f i) : SV_Target
            {
/*
                half4 albedo = tex3D(_Texture, float3(i.texcoord.xy, 0.0)); albedo.a = 0.5;
#if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                albedo.a = 0.1 + i.data.transform[0][1]; //what is the schema, position, rotation, scale? seems like it, scale definitely works
                //if (i.data.transform[2][1] > 1.0) { albedo.a = 1.0; }
#endif
                //return i.color * albedo; //TODO: Make Instancing 3D in combination with PixelFire ProperVolume Shader (or HazeVolume)
                return albedo;
*/
//PIXELFIRE//
                float4 input_vertex = float4(0.0, 0.0, 0.0, 1.0);
                float4 input_colour = float4(1.0, 1.0, 1.0, 1.0);
                float3 input_normal = float3(1.0, 1.0, 1.0);
#if defined(UNITY_PARTICLE_INSTANCING_ENABLED)
                input_vertex = float4(i.unmodified.xyz, 1.0); // - i.data.transform[0];
                input_colour = _Color; //i.data.color * _Color;
                input_normal = i.normal; //i.data.transform[0].xyz; //This might be incorrect...XD
#else
                input_vertex = i.unmodified;
                input_colour = _Color;
                input_normal = i.normal;
#endif
                float4 output; float4 src; float3 position;
                float3 origin = input_vertex + float3(0.5f, 0.5f, 0.5f);
                float3 direction = normalize(ObjSpaceViewDir(float4(input_vertex.xyz, 0.0f)));
                float3 light = normalize(ObjSpaceViewDir(input_colour));
                const float intensity = 32.0f;
                const float stride = 1.732f / _Steps;
                origin += (25.0f * stride * direction);

                for (uint i = 0; i < _Steps; ++i)
                {
                    position = origin + (direction * (i * stride));
                    if (position.x < 0.0f
                    ||  position.x > 1.0f
                    ||  position.y < 0.0f
                    ||  position.y > 1.0f
                    ||  position.z < 0.0f
                    ||  position.z > 1.0f) { break; }

                    src = tex3Dlod(_Texture, float4(input_vertex.xyz, 1.0f));
                    src.rgb = illuminate(src.rgb, input_normal, light, direction, intensity);
                    src.a = 0.0114f;

                    output.rgb = ((src.a * src.rgb) + ((input_colour.a - src.a) * output.rgb) + input_colour.rgb) / 2.0f;
                    output.a = src.a + ((1.0f - src.a) * output.a);
                    output.a = ((position.z > 0.25) && (position.z < 0.75) && (position.y > 0.25) && (position.y < 0.75)) ? output.a : 0.0;
                    //max(max(position.x, position.y), position.z);
                }
                return output;
//PIXELFIRE//
            }
            ENDCG
        }
    }
}