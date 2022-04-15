Shader "Custom/Fog"
{
    Properties
    {
        _Color("Colour", Color) = (1,1,1,1)
        _Texture("Texture", 3D) = "" {}
        _Steps("Steps", Float) = 2500
    }
    SubShader
    {
        Tags { "Queue" = "Transparent+1" "RenderType" = "Transparent" "LightMode" = "Always" }
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Front
        ZWrite Off
        ZTest LEqual //NotEqual

        Pass
        {
            CGPROGRAM
            #pragma target 4.0
            #pragma vertex vertex_shader
            #pragma fragment fragment_shader
            #include "UnityCG.cginc"
            
            float4 _Color;
            sampler3D _Texture;

            struct appdata
            {
                float3 vertex : TEXCOORD1;
                float4 screen : SV_POSITION;
            };

            appdata vertex_shader(appdata_full input)
            {
                appdata output;
                output.vertex = input.vertex;
                output.screen = UnityObjectToClipPos(input.vertex);
                return output;
            }

            float4 fragment_shader(appdata input) : COLOR
            {
                float alpha = tex3Dlod(_Texture, float4(input.vertex.xyz, 0.0f)).a;
                return _Color * float4(alpha, alpha, alpha, 1.0f);
            }
            ENDCG
        }
    }
}
