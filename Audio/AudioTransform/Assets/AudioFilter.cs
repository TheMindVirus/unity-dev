using UnityEngine;

[ExecuteInEditMode]
public class AudioFilter : MonoBehaviour
{
    public int Mode;
    public string ModeName;

    public float Phase = 0.5f;
    public float Gain = -1.0f;
    public float Q = 0.05f;
    public float Curve = 5.0f;
    public float Bandwidth = 2.0f;

    public Material Visualiser;
    public Material EQ;

    public uint VisOffset;
    public uint EQOffset;

    int N;
    float[] input;
    float[] output;

    float[] real;
    float[] imag;
    float[] eq;

    float[] vis = new float[1000];
    float[] eqo = new float[1000];

    void Start()
    {
        float[] x = { -6.0f, -5.0f, -4.0f, -3.0f, -2.0f, -1.0f, 0.0f, 1.0f, 2.0f, 3.0f, 4.0f, 5.0f, 6.0f };
        float[] r = { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };
        float[] c = { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };
        float[] y = { 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f, 0.0f };
        int n = x.Length;
        string str = "";
        for (var i = 0; i < n; ++i)
        {
            for (var j = 0; j < n; ++j)
            {
                r[i] += x[j] * Mathf.Cos((2.0f * Mathf.PI * j * i) / n);
                c[i] += x[j] * -Mathf.Sin((2.0f * Mathf.PI * j * i) / n);
            }
        }
        for (var i = 0; i < n; ++i)
        {
            for (var j = 0; j < n; ++j)
            {
                y[i] += (1.0f / n) * ((r[j] * Mathf.Cos((2.0f * Mathf.PI * j * i) / n)) - (c[j] * Mathf.Sin((2.0f * Mathf.PI * j * i) / n)));
            }
        }
        for (var i = 0; i < n; ++i)
        {
            str += y[i].ToString() + ", ";
        }
        Debug.Log(str);
    }

    void Update()
    {
        if (Mode == 0) { ModeName = "Fourier"; }
        else { ModeName = "Unknown"; }

        eq = new float[N];
        for (var i = 0; i < N; ++i)
        {
            float x = ((float)i) / N;
            x += -Phase;
            eq[i] = Mathf.Pow(Curve, -Mathf.Pow(Mathf.Abs(x), Bandwidth) / Q);
            eq[i] *= Gain;
        }

        for (var i = 0; i < 1000; ++i)
        {
            vis[i] = output[(i + VisOffset) % vis.Length];
            eqo[i] = eq[(i + EQOffset) % eq.Length];
        }

        Visualiser.SetInt("_Length", vis.Length);
        Visualiser.SetFloatArray("_Levels", vis);
        EQ.SetInt("_Length", eqo.Length);
        EQ.SetFloatArray("_Levels", eqo);
    }

    void OnAudioFilterRead(float[] data, int channels)
    {
        N = data.Length / channels;
        input = new float[N];
        output = new float[N];
        real = new float[N];
        imag = new float[N];
        
        uint i = 0;
        uint j = 0;
        uint k = 0;

        for (k = 0; k < channels; ++k)
        {
            //Deinterleave Channel
            for (i = 0; i < N; ++i)
            {
                input[i] = data[(i * channels) + k];
            }

            //Forward Transform
            if (Mode == 0)
            {
                for (i = 0; i < N; ++i)
                {
                    for (j = 0; j < N; ++j)
                    {
                        real[i] += data[j] * Mathf.Cos((2.0f * Mathf.PI * j * i) / N);
                        imag[i] += data[j] * -Mathf.Sin((2.0f * Mathf.PI * j * i) / N);
                    }
                }
            }
        
            //Apply Gauss
            if (eq != null)
            {
                for (i = 0; i < N; ++i)
                {
                    real[i] += eq[i];
                    imag[i] += eq[i];
                }
            }
        
            //Inverse Transform
            if (Mode == 0)
            {
                for (i = 0; i < N; ++i)
                {
                    for (j = 0; j < N; ++j)
                    {
                        output[i] += (1.0f / N) * ((real[j] * Mathf.Cos((2.0f * Mathf.PI * j * i) / N)) - (imag[j] * Mathf.Sin((2.0f * Mathf.PI * j * i) / N)));
                        data[i] = output[i];
                    }
                }
            }

            //Reinterleave Channel
            for (i = 0; i < N; ++i)
            {
                data[(i * channels) + k] = output[i];
            }
        }
    }
}
