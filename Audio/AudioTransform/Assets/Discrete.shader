Shader "Hidden/Discrete"
{
    Properties
    {
        
    }
    SubShader
    {
        Pass
        {
            CGPROGRAM
            #pragma vertex vertex
            #pragma fragment fragment
            #include "UnityCG.cginc"

            uint _Length;
            float _Levels[1000];

            appdata_full vertex(appdata_full input)
            {
                appdata_full output = input;
                output.vertex = UnityObjectToClipPos(input.vertex);
                return output;
            }

            fixed4 fragment(appdata_full input) : SV_Target
            {
                fixed4 output = fixed4(0.0, 0.0, 0.0, 0.0);
                for (uint i = 0; i < _Length; ++i)
                {
                    float x = 1.0 - input.texcoord.x;
                    float y = ((1.0 - input.texcoord.y) * 2.0) - 1.0;
                    float pos = ((float)i) / _Length;
                    float width = ((float)1) / _Length;
                    float level = _Levels[i];
                    if ((x > pos) && (x < (pos + width)))
                    {
                        if (((y > 0) && (y < level))
                        ||  ((y < 0) && (y > level)))
                        {
                            output = fixed4(1.0, 1.0, 1.0, 1.0);
                        }
                    }
                }
                return output;
            }
            ENDCG
        }
    }
}
