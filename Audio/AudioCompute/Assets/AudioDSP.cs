using UnityEditor;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;

//using System.Windows.Media.ShaderEffects;

[ExecuteInEditMode]
public class AudioDSP : MonoBehaviour
{
    public ComputeShader shader;
    ComputeBuffer samples;
    int bufferSize = 2048;
    int idx;

    string kernel = "main";
    string sizeName = "size";
    string dataName = "data";
    string channelsName = "channels";

    int m_channels = 0;
    float[] m_data = new float[2048];
    float[] m_dataOut = new float[2048];

    int accent;
    double startTick;
    double sampleRate;
    double nextTick;
    float amp;
    float phase;
    double bpm;
    float gain;
    int signatureHi;
    int signatureLo;

    int i = 0;
    int j = 0;

    bool busy = false;
    double time = 0.0;

    void Start()
    {
        accent = 4;
        startTick = AudioSettings.dspTime;
        sampleRate = AudioSettings.outputSampleRate;
        nextTick = startTick * sampleRate;
        amp = 0.0F;
        phase = 0.0F;
        bpm = 140.0F;
        gain = 0.5F;
        signatureHi = 4;
        signatureLo = 4;
        Debug.Log(sampleRate);
        Application.runInBackground = true;
    }

    void Update()
    {
        //DSP();
        time = Time.timeAsDouble;
        if (!busy) { StartCoroutine("DSP"); }
        /*for (j = 0; j < bufferSize; ++j)
        {
            m_dataOut[j] = m_data[j];
        }*/
        //m_dataOut = m_data;
    }

    void OnApplicationFocus()
    {
        Debug.Log("State Change");
    }

    void OnAudioFilterRead(float[] data, int channels)
    {
        //m_data = data;
        //data = m_dataOut;
        ///*
        busy = true;
        m_channels = channels;
        for (i = 0; i < bufferSize; ++i)
        {
            m_data[i] = data[i];
            data[i] = m_dataOut[i];
        }
        busy = false;
        //*/
        /*
        for (i = 0; i < bufferSize; ++i)
        {
            //data[i] *= Mathf.Sin((float)time * 15.0f); //wonky trance gate
            //data[i] *= Mathf.Sin(i); //transient high pass filter
            data[i] += data[i] * Mathf.Sin(i); //christmas sparkle filter
            //data[i] = data[i] - Mathf.Repeat(data[i], 0.5f); //bitcrushed white noise
        }
        */
        /*
        double samplesPerTick = sampleRate * 60.0F / bpm * 4.0F / signatureLo;
        double sample = AudioSettings.dspTime * sampleRate;
        int dataLen = data.Length / channels;

        int n = 0;
        while (n < dataLen)
        {
            float x = gain * amp * Mathf.Sin(phase);
            int i = 0;
            while (i < channels)
            {
                data[n * channels + i] += x;
                i++;
            }
            while (sample + n >= nextTick)
            {
                nextTick += samplesPerTick;
                amp = 1.0F;
                if (++accent > signatureHi)
                {
                    accent = 1;
                    amp *= 2.0F;
                }
                Debug.Log("Tick: " + accent + "/" + signatureHi);
            }
            phase += amp * 0.3F;
            amp *= 0.993F;
            n++;
        }
        */
    }

    void DSP()
    {
        /*
        for (j = 0; j < bufferSize; ++j)
        {
            m_dataOut[j] = m_data[j];
        }
        */
        ///*
        idx = shader.FindKernel(kernel);
        samples = new ComputeBuffer(bufferSize, 4, ComputeBufferType.Raw, ComputeBufferMode.SubUpdates);
        samples.SetData(m_data);
        shader.SetInt(sizeName, bufferSize);
        shader.SetInt(channelsName, m_channels);
        shader.SetBuffer(idx, dataName, samples);
        shader.Dispatch(idx, 1, 1, 1);
        samples.GetData(m_dataOut);
        samples.Release();
        //*/
    }
}
