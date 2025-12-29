using UnityEngine;
using Unity.Collections;
using System.Collections;
using System.Collections.Generic;

public class AudioShader : MonoBehaviour //Behaviour //AudioRenderer
{
    public static bool Render(NativeArray<float> buffer) //new public static bool Render(NativeArray<float> buffer)
    {
        //Debug.Log("AudioShader Process");
        return true;
    }

    void Start() //new void Start()
    {
        Debug.Log("AudioShader Started");
    }

    void Stop() //new void Stop()
    {
        Debug.Log("AudioShader Stopped");
    }
}
