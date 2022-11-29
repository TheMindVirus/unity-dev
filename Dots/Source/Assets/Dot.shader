Shader "Custom/Dot"
{
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

            appdata_full vertex_shader(appdata_full input) { input.vertex.xyz *= 2.0; return input; }

            half4 fragment_shader(appdata_full input) : COLOR
            {
                half4 output = half4(0.0, 0.0, 0.0, 0.0);
                half2 vertex = (input.vertex.xy / _ScreenParams.xy) - 0.5;
                //vertex.x *= (vertex.x / vertex.y); //Hourglass
                vertex.x *= (_ScreenParams.x / _ScreenParams.y);
                if ((vertex.x * vertex.x) + (vertex.y * vertex.y) > 0.1) { output.a = 1.0; }
                return output;
            }
            ENDCG
        }
    }
}
