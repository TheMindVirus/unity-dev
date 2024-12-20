Shader "Custom/CableDebug"
{
    Properties
    {
        [HDR] _Emission("Emission", Color) = (1.0, 1.0, 1.0, 1.0)
        _Position1("Position 1", Vector) = (-0.5, -0.5, -0.5, 1.0)
        _Position2("Position 2", Vector) = (0.5, 0.5, 0.5, 1.0)
        _Rotation("Rotation", Vector) = (0.0, 0.0, 0.0, 0.0)
        _Scale("Scale", Float) = 100.0
        _Size("Size", Float) = 1.0
        _Sag("Sag", Float) = 1.0
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Opaque" }
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vertex_shader
            #pragma fragment fragment_shader
            #include "UnityCG.cginc"

            half4 _Emission;
            half4 _Position1;
            half4 _Position2;
            half4 _Rotation;
            uint _Scale;
            half _Size;
            half _Sag;

            half4 blend(half4 src, half4 dst)
            {
                half4 mix = half4(0.0, 0.0, 0.0, 0.0);
                mix.rgb = (src.rgb * 0.5) + ((1.0 - src.a) * dst.rgb);
                mix.a = (src.a * 0.5) + ((1.0 - src.a) * dst.a);
                return mix;
            }

            half2 linearise(appdata_full pos1, appdata_full pos2)
            {
                half m = (pos2.vertex.y - pos1.vertex.y)
                       / (pos2.vertex.x - pos1.vertex.x);
                if (m == 0.0) { m == 0.000001; }
                return half2(m, pos2.vertex.y - (m * pos2.vertex.x));
            }

            half3 rotation(half3 pos, half3 value, half3 pivot = half3(0.0, 0.0, 0.0))
            {
                half3 remap = half3(value.x, value.y, value.z);
                half3 moved = pos - pivot;
                half3x3 _matrix;
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

            half3 interpolation(half3 start, half3 end, half pos, half scale)
            {
                pos /= (scale - 1.0);
                end -= start;
                start += (end * pos);
                pos -= 0.5;
                pos *= 2.0;
                pos = 1.0 - ((pos / pos) * pow(abs(pos), 2.0));
                start.y -= pos * _Sag;
                return start;
            }

            half4 projection(half4 input, half aspect)
            {
                input = UnityObjectToClipPos(input); //This is not querying 3D->2D as expected
                //input = mul(UNITY_MATRIX_P, mul(UNITY_MATRIX_MV, half4(0.0, 0.0, 0.0, 1.0))
                //     + half4(input.x, input.y, 0.0, 0.0)); //Billboard Aspect

                //input = mul(UNITY_MATRIX_P, mul(UNITY_MATRIX_MV, half4(input.xyz, 1.0)));
                //input = div(input, UNITY_MATRIX_P); //<-- requires inverse matrix I_P and I_MV
                input = mul(unity_ObjectToWorld, half4(input.xyz, 1.0));
                return input;
            }

            //appdata_full vertex_shader(appdata_full input) { input.vertex.xyz *= 2.0; return input; }
            //appdata_full vertex_shader(appdata_full input) { input.vertex = UnityObjectToClipPos(input.vertex); return input; }

            struct appdata_vertex { half4 vertex : SV_POSITION; half4 origin : TEXCOORD0; };
            appdata_vertex vertex_shader(appdata_full input)
            {
                appdata_vertex output;
                output.vertex = input.vertex;
                output.vertex.xyz *= 2.0;
                //output.vertex = UnityObjectToClipPos(input.vertex);
                output.origin = UnityObjectToClipPos(half4(0.0, 0.0, 0.0, 1.0));
                return output;
            }

            half4 fragment_shader(appdata_vertex input) : COLOR
            {
                half4 output = half4(1.0, 1.0, 1.0, 0.0);
                half2 vertex = (input.vertex.xy / _ScreenParams.xy) - 0.5;
                half aspect = _ScreenParams.x / _ScreenParams.y;
                vertex.x *= 4.0;
                vertex.y *= -4.0;

                //BEGIN_GEOMETRY_SHADER
                bool condition = false;
                bool subcondition = false;
                appdata_full geometry[4];
                half size = (_Size * 0.1);
                for (uint i = 0; i < _Scale; ++i)
                {
                    //BEGIN_SLICE_SHADER
                    half3 pos = interpolation(_Position1, _Position2, i, _Scale);

                    geometry[0].vertex = half4(0.0, 0.0, 0.0, 0.0); //half4(pos.x - size, pos.y - size, pos.z, 0.0);
                    //geometry[0].vertex = half4(rotation(geometry[0].vertex, _Rotation.xyz, pos), 0.0);
                    geometry[0].vertex = projection(geometry[0].vertex, aspect);

                    geometry[1].vertex = half4(pos.x + size, pos.y - size, pos.z, 0.0);
                    //geometry[1].vertex = half4(rotation(geometry[1].vertex, _Rotation.xyz, pos), 0.0);
                    geometry[1].vertex = projection(geometry[1].vertex, aspect);

                    geometry[2].vertex = half4(pos.x + size, pos.y + size, pos.z, 0.0);
                    //geometry[2].vertex = half4(rotation(geometry[2].vertex, _Rotation.xyz, pos), 0.0);
                    geometry[2].vertex = projection(geometry[2].vertex, aspect);

                    geometry[3].vertex = half4(pos.x - size, pos.y + size, pos.z, 0.0);
                    //geometry[3].vertex = half4(rotation(geometry[3].vertex, _Rotation.xyz, pos), 0.0);
                    geometry[3].vertex = projection(geometry[3].vertex, aspect);
                    
                    condition = true;
                    //Based on 3D Linear Equation, y = mx + c but also with z
                    //although if already in screen space coordinates then y = mx + c is fine

                    //if ((abs(geometry[0].vertex.x - (vertex.x * aspect)) < 0.1)
                    //&& (abs(geometry[0].vertex.y - vertex.y) < 0.1))
                    //{ output.rgb = _Emission.rgb; output.a = 0.5; }

                    half r1 = abs(geometry[0].vertex.x - (vertex.x * aspect));
                    half r2 = abs(geometry[0].vertex.y - vertex.y);
                    if (sqrt((r1 * r1) + (r2 * r2)) < 0.1)
                    { output.rgb = _Emission.rgb; output.a = 0.5; }

                    half l1 = abs(input.origin.x - (vertex.x * aspect));
                    half l2 = abs(input.origin.y - vertex.y);
                    if (sqrt((l1 * l1) + (l2 * l2)) < 0.1)
                    { output.rgb = 1.0 - _Emission.rgb; output.a = 0.5; }

                    //BEGIN_GRADIENT_SHADER
                    half3 gap = half3(0.0, 0.0, 0.0);
///*
                    gap.xz = linearise(geometry[0], geometry[1]);
                    gap[1] = (gap[0] * vertex.x) + gap[2];
                    subcondition = (vertex.y < gap.y); if (subcondition) { output = blend(half4(1.0, 0.0, 0.0, 0.5), output); }
                    condition = condition & subcondition;

                    gap.xz = linearise(geometry[1], geometry[2]);
                    gap[1] = (gap[0] * vertex.x) + gap[2];
                    subcondition = (vertex.y < gap.y); if (subcondition) { output = blend(half4(0.0, 1.0, 0.0, 0.5), output); }
                    condition = condition & subcondition;

                    gap.xz = linearise(geometry[2], geometry[3]);
                    gap[1] = (gap[0] * vertex.x) + gap[2];
                    subcondition = (vertex.y > gap.y); if (subcondition) { output = blend(half4(0.0, 0.0, 1.0, 0.5), output); }
                    condition = condition & subcondition;

                    gap.xz = linearise(geometry[3], geometry[0]);
                    gap[1] = (gap[0] * vertex.x) + gap[2];
                    subcondition = (vertex.y > gap.y); if (subcondition) { output = blend(half4(1.0, 1.0, 0.0, 0.5), output); }
                    condition = condition & subcondition;

                    if (condition) { output.rgb = 1.0; output.a = 1.0; }

//*/
                    //END_GRADIENT_SHADER
                    break;

                    //END_SLICE_SHADER
                }
                //END_GEOMETRY_SHADER

                return output;
            }
            ENDCG //!!!BUG: Alpha Blending Mode prevents Gizmos from rendering clearly
        }
    }
}
