Shader "Custom/Origin"
{
    Properties
    {
        [HDR] _Emission("Emission", Color) = (1.0, 1.0, 1.0, 1.0)
    }
    SubShader //ROTATION AND SCALE BUGS PRESENT, MAINTAIN TRANSFORM OF THE CUBE.
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Opaque" "Occlude" = "Ignored" } //Ignored
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Off
        //Occlude Off //Ignored, Breaks
        ZWrite Off

        Pass
        {
            Tags { "Occlude" = "Off" }

            CGPROGRAM
            #pragma vertex vertex_shader
            #pragma fragment fragment_shader
            #pragma multi_compile Occlude //Ignored
            #include "UnityCG.cginc"
            #define TAU   6.283185307179586

            half4 _Emission;

            half3 rotation(half3 pos, half3 value, half3 pivot = half3(0.0, 0.0, 0.0))
            {
                half3 remap = half3(value.x * TAU, value.y * TAU, value.z * TAU);
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

            struct appdata_vertex { half4 vertex : SV_POSITION; half4 origin : TEXCOORD0; half4 worldPos : TEXCOORD1; half2 unmodified : TEXCOORD2; };
            appdata_vertex vertex_shader(appdata_full input)
            {
                appdata_vertex output;

                output.worldPos = mul(UNITY_MATRIX_M, half4(0.0, 0.0, 0.0, 1.0));
                output.worldPos.xyz = rotation(output.worldPos.xyz, half3(UNITY_MATRIX_M[1].z, 0.0, 0.0));
                half4 origin0 = half4(-output.worldPos.xyz, 1.0);
                //half4 origin0 = half4(0.0, 1.0, 0.0, 1.0); //<-- offset at origin works best
                half4 addition1 = half4(0.0, 0.0, 0.0, 0.0); //before any model view projection is done
                half4 addition2 = half4(0.0, 0.0, 0.0, 0.0);
                half4 addition3 = half4(input.vertex.x, input.vertex.y, 0.0, 0.0);
                half4 addition4 = half4(0.0, 0.0, 0.0, 0.0);
                output.vertex = mul(UNITY_MATRIX_P, mul(UNITY_MATRIX_V, mul(UNITY_MATRIX_M, origin0 + addition1)
                      + addition2)
                      + addition3)
                      + addition4; //Billboard Aspect

                output.unmodified = input.vertex.xy;

                return output;
            }

            half4 fragment_shader(appdata_vertex input) : COLOR
            {
                half4 output = half4(1.0, 1.0, 1.0, 0.0);
                half2 vertex = (input.vertex.xy / _ScreenParams.xy) - 0.5;
                half aspect = _ScreenParams.x / _ScreenParams.y;

                half rl1 = abs(input.unmodified.x);
                half rl2 = abs(input.unmodified.y);
                if (sqrt((rl1 * rl1) + (rl2 * rl2)) < 0.1)
                { output.rgb = _Emission.rgb; output.a = 0.5; }
                //output.rgb = input.unmodified.x; output.a = 0.5;
                //output.rgb = UNITY_MATRIX_M[1].z; //This should really be a transform instead of this matrix rubbish

                return output;
            }
            ENDCG
        }
    }
}
