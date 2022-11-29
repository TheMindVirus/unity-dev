Shader "Custom/Cable"
{
    Properties
    {
        [HDR] _Emission("Emission", Color) = (1.0, 1.0, 1.0, 1.0)
        _Position1("Position 1", Vector) = (-0.5, -0.5, -0.5, 1.0)
        _Position2("Position 2", Vector) = (0.5, 0.5, 0.5, 1.0)
        _Rotation("Rotation", Vector) = (0.0, 0.0, 0.0, 0.0)
        _Scale("Scale", Float) = 100.0
        _Size("Size", Float) = 1.0
        _Sag("Sag", Float) = 1.0
    }
    SubShader
    {
        Tags { "Queue" = "Transparent" "RenderType" = "Opaque" "Occlude" = "Ignored" } //Ignored
        Blend SrcAlpha OneMinusSrcAlpha
        Cull Off
        //Occlude Off //Ignored, Breaks
        ZWrite Off

        Pass
        {
            Name "Dot"
            Tags { "Occlude" = "Off" }
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 0
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 1
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 2
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 3
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 4
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 5
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 6
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 7
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 8
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 9
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 10
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 11
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 12
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 13
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 14
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 15
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 16
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 17
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 18
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 19
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 20
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 21
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 22
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 23
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 24
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 25
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 26
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 27
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 28
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 29
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 30
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 31
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 32
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 33
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 34
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 35
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 36
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 37
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 38
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 39
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 40
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 41
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 42
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 43
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 44
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 45
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 46
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 47
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 48
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 49
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 50
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 51
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 52
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 53
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 54
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 55
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 56
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 57
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 58
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 59
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 60
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 61
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 62
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 63
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 64
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 65
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 66
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 67
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 68
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 69
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 70
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 71
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 72
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 73
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 74
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 75
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 76
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 77
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 78
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 79
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 80
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 81
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 82
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 83
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 84
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 85
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 86
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 87
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 88
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 89
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 90
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 91
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 92
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 93
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 94
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 95
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 96
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 97
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 98
            #include "CableInclude.cginc"
            ENDCG
        }
        Pass
        {
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB 100
            #define CABLE_INCLUDE_POSITION 99
            #include "CableInclude.cginc"
            ENDCG
        }
    }
}
