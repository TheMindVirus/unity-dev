using UnityEngine;
using Unity.Collections;
using System.Collections;
using System.Collections.Generic;

public class AudioFilter : MonoBehaviour //Behaviour //AudioLowPassFilter
{
    private bool running = false;
    private float phase = 0.0f;
    private float gain = 0.75f;
    private float inc = 0.001f;

    public void OnAudioFilterRead(float[] data, int channels) //new public void OnAudioFilterRead(float[] data, int channels)
    {
        if (!running) { return; }
        //Debug.Log("AudioFilter Process");
        //Debug.Log(data); //Continues Processing after Player Preview is Stopped
        //Debug.Log(channels); //2ch Stereo despite being in 7.1 Surround mode with 8ch
        for (var i = 0; i < data.Length; ++i) //i += channels);
        {
            //Audio Shading Process for Creative Labs Sound Blaster 16
            //AWE EAX SBX THX DSP ASP Processing Filter Inner Loop
            //data[i] = data[i]; //contains no interleaved data
            //data[i] *= 0.0f; //mutes the incoming stream
            //data[i] = Mathf.Sin(phase) * gain; phase += inc; //overlays a sine wave instead of mixing it
            data[i] += Mathf.Sin(phase) * gain; phase += inc; //varies in frequency tremendously
        }
    }

    void Start() //new void Start()
    {
        Debug.Log("AudioFilter Started");
        running = true;
    }

    void Stop() //new void Stop()
    {
        Debug.Log("AudioFilter Stopped");
        running = false;
    }

    //void Awake() { Start(); } //new void Awake() { Start(); }
    void OnApplicationQuit() { Stop(); } //new void OnApplicationQuit() { Stop(); }
}
