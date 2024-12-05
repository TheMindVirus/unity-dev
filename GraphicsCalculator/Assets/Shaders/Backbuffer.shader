Shader "Hidden/Backbuffer"
{
    Properties
    {
        _MainTex("Texture", 2D) = "" {}
        _BackTex("Backbuffer", 2D) = "" {}
        _MainBlend("MainBlend", Float) = 0.5
        _BackBlend("BackBlend", Float) = 0.5
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Opaque" }
        Cull Off ZWrite Off ZTest Always
        Blend SrcAlpha OneMinusSrcAlpha

        Pass
        {
            CGPROGRAM
            #pragma vertex vertex
            #pragma fragment fragment
            #include "UnityCG.cginc"

            sampler2D _MainTex;
            sampler2D _BackTex;
            fixed4 _MainTex_ST;
            fixed4 _BackTex_ST;
            fixed _MainBlend;
            fixed _BackBlend;

            appdata_full vertex(appdata_full input)
            {
                appdata_full output = input;
                output.vertex = UnityObjectToClipPos(input.vertex);
                return output;
            }

            fixed4 fragment(appdata_full input) : SV_Target
            {
                fixed4 output = fixed4(0.0, 0.0, 0.0, 0.0);
                output.rgba += tex2D(_MainTex, (input.texcoord.xy * _MainTex_ST.xy) + _MainTex_ST.zw) * _MainBlend;
                output.rgba += tex2D(_BackTex, (input.texcoord.xy * _BackTex_ST.xy) + _BackTex_ST.zw) * _BackBlend;
                return output;
            }
            ENDCG
        }
    }
}
