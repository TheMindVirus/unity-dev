using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightingControl : MonoBehaviour
{
    List<GameObject> Lights = new List<GameObject>();

    void Start()
    {
        foreach (Transform child in transform)
        {
            if (child.name.Contains("Light"))
            {
                Lights.Add(child.gameObject);
            }
        }
        foreach (GameObject go in Lights)
        {
            go.GetComponent<Renderer>().material.EnableKeyword("_EMISSION");
        }
    }

    void SetLights(string data)
    {
        string[] raw = data.Split(',');
        float[] values = new float[raw.Length];
        for (int i = 0; i < raw.Length; ++i) { float.TryParse(raw[i].Replace(" ", ""), out values[i]); }
        int index = 0;
        foreach (GameObject go in Lights)
        {
            int channel = 0;
            int level = 0;
            int.TryParse(go.name.Substring(3, 1), out channel);
            int.TryParse(go.name.Substring(5), out level);
            go.GetComponent<Renderer>().material.SetVector("_EmissionColor", new Vector4(0.0f, values[index], 0.0f, 0.5f));
            ++index;
        }
    }
/*
    void Update()
    {
        float intensity = Mathf.Sin((Time.time % (60.0f / 127.0f)) * Mathf.PI * 2.0f);
        string data = "";
        foreach (GameObject go in Lights)
        {
            data += intensity.ToString() + ", ";
        }
        SetLights(data);
    }
*/
}
