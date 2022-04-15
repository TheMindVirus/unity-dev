Shader "Unlit/Sheen"
{
    Properties
    {
        _Color ("Color", Color) = (1, 1, 1, 1)
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" }
        Blend SrcAlpha OneMinusSrcAlpha

        Pass
        {
            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag

            struct vertdata
            {
                float4 vertex : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct fragdata
            {
                fixed4 colour : _Color;
                float2 uv : TEXCOORD0;
                float4 vertex : SV_POSITION;
            };

            fixed4 _Color;

            vertdata vert(vertdata input)
            {
                vertdata output = input;
                float2 center = UnityObjectToClipPos(float4(0.0, 0.0, 0.0, 0.0));
                output.vertex = UnityObjectToClipPos(input.vertex);
                output.uv = center.xy - output.vertex.xy;
                output.uv.x *= -1.0;
                return output;
            }

            fixed4 frag(fragdata input) : SV_Target
            {
                fragdata output = input;
                output.colour = _Color;
                float a = 1.0;
                float b = 1.0;
                float f = 8.0;
                float ax = a * input.uv.x;
                float by = b * input.uv.y;
                output.colour.a *= (sqrt(pow(ax, f) + pow(by, f)));
                return output.colour;
            }
            ENDCG
        }
    }
}
