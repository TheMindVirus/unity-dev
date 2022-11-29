def pass_template(n = 100, i = 1):
    return """
        Pass
        {{
            CGPROGRAM
            #define CABLE_INCLUDE_MAX_NUMB {}
            #define CABLE_INCLUDE_POSITION {}
            #include "CableInclude.cginc"
            ENDCG
        }}""".format(n, i)

N = 100
newdata = ""
for i in range(0, N):
    newdata += pass_template(N, i)

with open("PassTemplate.txt", "w") as file:
    file.write(newdata)

print("Done!")
