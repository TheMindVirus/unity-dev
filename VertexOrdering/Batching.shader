Shader "Custom/Batching"
{
    Properties
    {
        _Color("Colour", Color) = (1,1,1,1)
        _Texture("Texture", 2D) = "" {}
        _ID("ID", Int) = 0
    }
    SubShader
    {
        Tags { "Queue"="Transparent" "RenderType"="Opaque" }
        //Tags { "RenderType"="Opaque" "DisableBatching"="True" }
        Blend SrcAlpha OneMinusSrcAlpha

        Pass
        {
            Cull Front
            CGPROGRAM
            #pragma target 4.0
            #pragma vertex vertex  
            #pragma fragment fragment
            //#define UNITY_ENABLE_INSTANCING
            //#define INSTANCING_ON
            //#include "UnityInstancing.cginc"
            #include "UnityCG.cginc"

            float4 _Color;
            sampler2D _Texture;
            uint _ID;

            struct supplicant
            {
                float4 vertex : POSITION;
                float4 texcoord : TEXCOORD0;
                uint id : SV_VertexID;
            };

            struct data
            {
                float4 vertex : SV_POSITION;
                float4 texcoord : TEXCOORD0;
                float4 colour : COLOR;
            };

            data vertex(supplicant input)
            {
                data output;
                output.vertex = UnityObjectToClipPos(input.vertex);
                output.texcoord = input.texcoord;
                output.colour = float4(0.0, 0.0, 0.0, 0.0);
                //if (input.id == _ID) { output.colour = float4(1.0, 1.0, 1.0, 1.0); }
                if ((input.id >= _ID) && (input.id < _ID + 4)) { output.colour = float4(1.0, 1.0, 1.0, 1.0); }
                return output;
            }
            float4 fragment(data input) : COLOR { return input.colour; }
            ENDCG
        }
        Blend SrcAlpha OneMinusSrcAlpha
        Pass
        {
            Cull Back
            CGPROGRAM
            #pragma target 4.0
            #pragma vertex vertex  
            #pragma fragment fragment
            //#define UNITY_ENABLE_INSTANCING
            //#define INSTANCING_ON
            //#include "UnityInstancing.cginc"
            #include "UnityCG.cginc"

            float4 _Color;
            sampler2D _Texture;
            uint _ID;

            struct supplicant
            {
                float4 vertex : POSITION;
                float4 texcoord : TEXCOORD0;
                uint id : SV_VertexID;
            };

            struct data
            {
                float4 vertex : SV_POSITION;
                float4 texcoord : TEXCOORD0;
                float4 colour : COLOR;
            };

            data vertex(supplicant input)
            {
                data output;
                output.vertex = UnityObjectToClipPos(input.vertex);
                output.texcoord = input.texcoord;
                output.colour = float4(0.0, 0.0, 0.0, 0.0);
                //if (input.id == _ID) { output.colour = float4(1.0, 1.0, 1.0, 1.0); }
                if ((input.id >= _ID) && (input.id < _ID + 4)) { output.colour = float4(1.0, 1.0, 1.0, 1.0); }
                return output;
            }
            float4 fragment(data input) : COLOR { return input.colour; }
            ENDCG
        }
    }
}
