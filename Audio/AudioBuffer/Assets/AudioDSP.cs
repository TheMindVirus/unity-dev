using UnityEngine;

public class AudioDSP : MonoBehaviour
{
    public float freq1 = 441.0f;
    public float freq2 = 441.0f;
    public float gain1 = 1.0f;
    public float gain2 = 1.0f;
    public float fm1x2 = -1.0f;

    float[] left = new float[2048];
    float[] right = new float[2048];

    float[] sine1 = new float[44100];
    float[] sine2 = new float[44100];

    int i = 0;
    int il = 0;
    int ir = 0;

    float pos1 = 0.0f;
    float pos2 = 0.0f;

    void Start()
    {
        for (i = 0; i < 44100; ++i)
        {
            var phase = ((float)i / 44100.0f) * 2.0f * Mathf.PI;
            sine1[i] = Mathf.Sin(phase);
            sine2[i] = Mathf.Sin(phase);
        }
    }

    float Compand(float a)
    {
        if (a >= 0.0f) { return 1.0f - (0.5f * a); }
        else { return 1.0f - (-0.5f * a); }
    }

    float Mix(float a, float b)
    {
        return (a * Compand(b)) + (b * Compand(a));
    }

    void OnAudioFilterRead(float[] data, int channels)
    {
        il = 0;
        ir = 0;
        if (freq1 < 0.0f) { freq1 = 0.0f; }
        if (freq2 < 0.0f) { freq2 = 0.0f; }
        for (i = 0; i < 2048; i += 2)
        {
            left[il] = data[i + 0];
            right[ir] = data[i + 1];

            data[i + 0] = left[il];
            data[i + 1] = right[ir];

            //data[i + 0] = Mathf.Sin((pos1 / 44100.0f) * 2.0f * Mathf.PI);
            //data[i + 1] = Mathf.Sin((pos1 / 44100.0f) * 2.0f * Mathf.PI);

            //data[i + 0] += (sine1[(int)pos1] * gain1);
            //data[i + 1] += (sine1[(int)pos1] * gain1);

            //data[i + 0] += (sine2[(int)pos2] * gain2);
            //data[i + 1] += (sine2[(int)pos2] * gain2);

            var level1 = (sine1[(int)pos1] * gain1);
            var level2 = (sine2[(int)pos2] * gain2);
            var cross = (level1 * level2) * fm1x2;

            data[i + 0] = Mix(data[i + 0], level1);
            data[i + 1] = Mix(data[i + 1], level1);

            data[i + 0] = Mix(data[i + 0], level2);
            data[i + 1] = Mix(data[i + 1], level2);

            data[i + 0] = Mix(data[i + 0], cross);
            data[i + 1] = Mix(data[i + 1], cross);

            //data[i + 0] = 0.0f;
            //data[i + 1] = 0.0f;

            il += 1;
            ir += 1;

            pos1 += freq1;
            pos2 += freq2;

            if (pos1 >= 44100.0f) { pos1 = 0.0f; }
            if (pos2 >= 44100.0f) { pos2 = 0.0f; }
        }
    }
}
