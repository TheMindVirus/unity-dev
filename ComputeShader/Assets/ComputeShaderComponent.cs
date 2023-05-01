using UnityEngine;
using System;

public class ComputeShaderComponent : MonoBehaviour
{
    public ComputeShader cs = null;
    public ComputeBuffer cb = null;
    public int CSMain = -1;

    void Start()
    {
        if (SystemInfo.supportsComputeShaders == true) { Debug.Log("[INFO]: Compute Shaders: Supported"); }
        else { Debug.Log("[INFO]: Compute Shaders: Not Supported"); }
        //cs = new ComputeShader("NewComputeShader.compute");
        cs = Resources.Load<ComputeShader>("NewComputeShader"); //Assets/Resources
        Debug.Log(cs);
        CSMain = cs.FindKernel("CSMain");
        cb = new ComputeBuffer(4, sizeof(float), ComputeBufferType.Structured, ComputeBufferMode.Immutable); //Raw+Dynamic should be default but have been wrecked internally on purpose
        cs.SetBuffer(CSMain, "Result", cb);
        cs.Dispatch(CSMain, 1, 1, 1);
        float[] raw = new float[4];
        cb.GetData(raw);
        Debug.Log("[" + raw[0].ToString("F") + ", " + raw[1].ToString("F") + ", " + raw[2].ToString("F") + ", " + raw[3].ToString("F") + "]");
        Color result = new Color(raw[0], raw[1], raw[2], raw[3]);
        GetComponent<MeshRenderer>().sharedMaterial.SetColor("_Color", result);
        cb.Release();
    }
}
