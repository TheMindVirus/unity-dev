Shader "FX/Water"
{
    Properties
    {
	_WaveScale ("Wave Scale", Range (0.02, 0.15)) = 0.063
	_WaveSpeed ("Wave Speed", Vector) = (19, 9, -16, -7)
	_ReflectionDistortion ("Reflection Distortion", Range (0, 1.5)) = 0.44
	_RefractionDistortion ("Refraction Distortion", Range (0, 1.5)) = 0.40
	_RefractionColor ("Refraction Color", COLOR) = (0.34, 0.85, 0.92, 1)
	_HorizonColor ("Horizon Color", COLOR) = (0.172, 0.463, 0.435, 1)
	[NoScaleOffset] _Fresnel ("Fresnel", 2D) = "gray" {}
	[NoScaleOffset] _NormalMap ("Normal Map", 2D) = "bump" {}
	[NoScaleOffset] _ReflectionColor ("Reflection Color", 2D) = "" {}
	[HideInInspector] _ReflectionMap ("Internal Reflection", 2D) = "" {}
	[HideInInspector] _RefractionMap ("Internal Refraction", 2D) = "" {}
    }
    Subshader
    {
	Tags
        {
            "WaterMode"="Refractive"
            "RenderType"="Opaque"
        }
        Blend SrcAlpha OneMinusSrcAlpha
	Pass
        {
            CGPROGRAM
            #pragma vertex vertex_shader
            #pragma fragment fragment_shader
            #pragma multi_compile_fog
            #pragma multi_compile WATER_REFRACTIVE WATER_REFLECTIVE WATER_SIMPLE

            #if defined (WATER_REFLECTIVE) || defined (WATER_REFRACTIVE)
            #define HAS_REFLECTION 1
            #endif

            #if defined (WATER_REFRACTIVE)
            #define HAS_REFRACTION 1
            #endif

            #include "UnityCG.cginc"

            uniform float4 _WaveScaleDynamic;
            uniform float4 _WaveOffsetDynamic;

            #if HAS_REFLECTION
            uniform float _ReflectionDistortion;
            #endif

            #if HAS_REFRACTION
            uniform float _RefractionDistortion;
            #endif

            struct appdata
            {
	        float4 vertex : POSITION;
	        float3 normal : NORMAL;
            };

            struct v2f
            {
	        float4 pos : SV_POSITION;

	        #if defined(HAS_REFLECTION) || defined(HAS_REFRACTION)
		float4 ref : TEXCOORD0;
		float2 bumpuv0 : TEXCOORD1;
		float2 bumpuv1 : TEXCOORD2;
		float3 viewDir : TEXCOORD3;
	        #else
		float2 bumpuv0 : TEXCOORD0;
		float2 bumpuv1 : TEXCOORD1;
		float3 viewDir : TEXCOORD2;
	        #endif

	        UNITY_FOG_COORDS(4)
            };

            v2f vertex_shader(appdata v)
            {
	        v2f o;
	        o.pos = UnityObjectToClipPos(v.vertex);

	        float4 temp;
	        float4 wpos = mul(unity_ObjectToWorld, v.vertex);
	        temp.xyzw = wpos.xzxz * _WaveScaleDynamic + _WaveOffsetDynamic;
	        o.bumpuv0 = temp.xy;
	        o.bumpuv1 = temp.wz;
	        o.viewDir.xzy = WorldSpaceViewDir(v.vertex);

	        #if defined(HAS_REFLECTION) || defined(HAS_REFRACTION)
	        o.ref = ComputeNonStereoScreenPos(o.pos);
	        #endif

	        UNITY_TRANSFER_FOG(o, o.pos);
	        return o;
            }

            #if defined (WATER_REFLECTIVE) || defined (WATER_REFRACTIVE)
            sampler2D _ReflectionMap;
            #endif

            #if defined (WATER_REFLECTIVE) || defined (WATER_SIMPLE)
            sampler2D _ReflectionColor;
            #endif

            #if defined (WATER_REFRACTIVE)
            sampler2D _Fresnel;
            sampler2D _RefractionMap;
            uniform float4 _RefractionColor;
            #endif

            #if defined (WATER_SIMPLE)
            uniform float4 _HorizonColor;
            #endif

            sampler2D _NormalMap;

            half4 fragment_shader(v2f i) : SV_Target
            {
	        i.viewDir = normalize(i.viewDir);
	        half3 bump1 = UnpackNormal(tex2D(_NormalMap, i.bumpuv0)).rgb;
	        half3 bump2 = UnpackNormal(tex2D(_NormalMap, i.bumpuv1)).rgb;
	        half3 bump = (bump1 + bump2) * 0.5;
	        half fresnel = dot(i.viewDir, bump);

	        #if HAS_REFLECTION
	        float4 uv1 = i.ref; uv1.xy += bump * _ReflectionDistortion;
	        half4 reflection = tex2Dproj(_ReflectionMap, UNITY_PROJ_COORD(uv1));
	        #endif

	        #if HAS_REFRACTION
	        float4 uv2 = i.ref; uv2.xy -= bump * _RefractionDistortion;
	        half4 refraction = tex2Dproj(_RefractionMap, UNITY_PROJ_COORD(uv2)) * _RefractionColor;
	        #endif

	        half4 color;

	        #if defined(WATER_REFRACTIVE)
	        half sample = UNITY_SAMPLE_1CHANNEL(_Fresnel, float2(fresnel, fresnel));
	        color = lerp(refraction, reflection, sample);
	        #endif

	        #if defined(WATER_REFLECTIVE)
	        half4 water = tex2D(_ReflectionColor, float2(fresnel, fresnel));
	        color.rgb = lerp(water.rgb, reflection.rgb, water.a);
	        color.a = reflection.a * water.a;
	        #endif
	
	        #if defined(WATER_SIMPLE)
	        half4 water = tex2D(_ReflectionColor, float2(fresnel, fresnel));
	        color.rgb = lerp(water.rgb, _HorizonColor.rgb, water.a);
	        color.a = _HorizonColor.a;
	        #endif

	        UNITY_APPLY_FOG(i.fogCoord, color);
	        return color;
            }
        ENDCG
	}
    }
}