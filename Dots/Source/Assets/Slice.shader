Shader "Custom/Slice"
{
    Properties
    {
        [HDR] _Emission("Emission", Color) = (1.0, 1.0, 1.0, 1.0)
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Opaque" }
        Blend SrcAlpha OneMinusSrcAlpha //!!!BUG: Alpha Blending Mode prevents Gizmos from rendering clearly
        Cull Off

        Pass
        {
            CGPROGRAM
            #pragma vertex vertex_shader
            #pragma fragment fragment_shader
            #include "UnityCG.cginc"

            half4 _Emission;

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

            appdata_full vertex_shader(appdata_full input) { input.vertex.xyz *= 2.0; return input; }

            half4 fragment_shader(appdata_full input) : COLOR
            {
                half4 output = half4(1.0, 1.0, 1.0, 0.0);
                half2 vertex = (input.vertex.xy / _ScreenParams.xy) - 0.5;

                //BEGIN_SLICE_SHADER
                bool condition = true;
                bool subcondition = false;
                appdata_full geometry[3];
                half3 gap = half3(0.0, 0.0, 0.0);

                geometry[0].vertex = half4(0.0, 0.25, 0.0, 0.0);
                geometry[1].vertex = half4(0.25, -0.25, 0.0, 0.0);
                geometry[2].vertex = half4(-0.25, -0.25, 0.0, 0.0);

                //condition = (vertex.y > 0.0);
                //if (condition) { output = blend(half4(1.0, 0.0, 0.0, 0.5), output); }

                gap.xz = linearise(geometry[0], geometry[1]);
                gap[1] = (gap[0] * vertex.x) + gap[2];
                subcondition = (vertex.y < gap.y); //if (subcondition) { output = blend(half4(1.0, 0.0, 0.0, 0.5), output); }
                condition = condition & subcondition;

                gap.xz = linearise(geometry[1], geometry[2]);
                gap[1] = (gap[0] * vertex.x) + gap[2];
                subcondition = (vertex.y > gap.y); //if (subcondition) { output = blend(half4(0.0, 1.0, 0.0, 0.5), output); }
                condition = condition & subcondition;

                gap.xz = linearise(geometry[2], geometry[0]);
                gap[1] = (gap[0] * vertex.x) + gap[2];
                subcondition = (vertex.y < gap.y); //if (subcondition) { output = blend(half4(0.0, 0.0, 1.0, 0.5), output); }
                condition = condition & subcondition;
                
                if (condition) { output.rgb *= _Emission.rgb; output.a = 1.0; } //_Emission.a; }
                //END_SLICE_SHADER

                return output; //TODO: Use Circular Function instead of an array of geometry for cables
            }
            ENDCG
        }
    }
}
