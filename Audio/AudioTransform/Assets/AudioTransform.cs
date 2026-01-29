using UnityEngine;

[ExecuteInEditMode]
public class AudioTransform : MonoBehaviour
{
    public float Translation = 0.0f;
    public float Rotation = 360.0f;
    public float Scale = 1.0f;

    void OnAudioFilterRead(float[] data, int channels)
    {
        for (var i = 0; i < data.Length; ++i)
        {
            data[i] *= Scale;
            data[i] *= Mathf.Cos((Rotation * Mathf.PI) / 180.0f);
            data[i] += Translation;
        }
    }
}
