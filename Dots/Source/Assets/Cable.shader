Shader "Custom/Cable"
{
    Properties
    {
        [HDR] _Emission("Emission", Color) = (1.0, 1.0, 1.0, 1.0)
        _MainTex("MainTex", 2D) = "" {}
        _Size("Size", Float) = 1.0
        _Sag("Sag", Float) = 1.0
        _Position1("Position 1", Vector) = (-0.5, -0.5, -0.5, 1.0)
        _Position2("Position 2", Vector) = (0.5, 0.5, 0.5, 1.0)

        _DebugRotation("Debug Rotation", Vector) = (0.0, 0.0, 0.0, 0.0)
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Opaque" }
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Off
        ZWrite Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vertex_shader
            #pragma geometry geometry_shader
            #pragma fragment fragment_shader
            #include "UnityCG.cginc"

            #define SCALE 256
            #define SUBSCALE (SCALE / 4)

            half4 _Emission;
            sampler2D _MainTex;
            half4 _MainTex_ST;
            half _Size;
            half _Sag;
            half4 _Position1;
            half4 _Position2;

            half4 _DebugRotation;

            struct geometry_data
            {
                half4 vertex : POSITION;
            };

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
                input = UnityObjectToClipPos(input);
                //input = mul(UNITY_MATRIX_P, mul(UNITY_MATRIX_MV, half4(0.0, 0.0, 0.0, 1.0))
                //     + half4(input.x, input.y, 0.0, 0.0)); //Billboard Aspect
                return input;
            }

            appdata_full vertex_shader(appdata_full input)
            {
                input.vertex = UnityObjectToClipPos(input.vertex);
                return input;
            }

            [maxvertexcount(SCALE)]
            void geometry_shader(point appdata_full input[1], inout TriangleStream<geometry_data> output)
            {
                geometry_data geometry;
                half size = (_Size * 0.1);
                half aspect = _ScreenParams.x / _ScreenParams.y;
                for (uint i = 0; i < SUBSCALE; ++i)
                {
                    half3 pos = interpolation(_Position1, _Position2, i, SUBSCALE);
                    half3 dir = normalize(ObjSpaceViewDir(UnityObjectToClipPos(half4(pos, 0.0))));
                    geometry.vertex = half4(pos.x - size, pos.y - size, pos.z, 0.0);
                    dir = normalize(ObjSpaceViewDir(UnityObjectToClipPos(geometry.vertex)));
                    geometry.vertex = half4(rotation(geometry.vertex, half3(dir + _DebugRotation.xyz), pos), 0.0);
                    geometry.vertex = projection(geometry.vertex, aspect);
                    output.Append(geometry);
                    geometry.vertex = half4(pos.x + size, pos.y - size, pos.z, 0.0);
                    dir = normalize(ObjSpaceViewDir(UnityObjectToClipPos(geometry.vertex)));
                    geometry.vertex = half4(rotation(geometry.vertex, half3(dir + _DebugRotation.xyz), pos), 0.0);
                    geometry.vertex = projection(geometry.vertex, aspect);
                    output.Append(geometry);
                    geometry.vertex = half4(pos.x - size, pos.y + size, pos.z, 0.0);
                    dir = normalize(ObjSpaceViewDir(UnityObjectToClipPos(geometry.vertex)));
                    geometry.vertex = half4(rotation(geometry.vertex, half3(dir + _DebugRotation.xyz), pos), 0.0);
                    geometry.vertex = projection(geometry.vertex, aspect);
                    output.Append(geometry);
                    geometry.vertex = half4(pos.x + size, pos.y + size, pos.z, 0.0);
                    dir = normalize(ObjSpaceViewDir(UnityObjectToClipPos(geometry.vertex)));
                    geometry.vertex = half4(rotation(geometry.vertex, half3(dir + _DebugRotation.xyz), pos), 0.0);
                    geometry.vertex = projection(geometry.vertex, aspect);
                    output.Append(geometry);
                    output.RestartStrip();
                }
            }

            half4 fragment_shader(appdata_full input) : COLOR
            {
                return _Emission;
                //return tex2D(_MainTex, (input.texcoord * _MainTex_ST.xy) + _MainTex_ST.zw) * _Emission;
            }
            ENDCG
        }
    }
}
