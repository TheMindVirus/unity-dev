using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Control : MonoBehaviour
{
    public List<GameObject> bars = new List<GameObject>();
    public GameObject ambient;
    public Material skybox;
    public Material water;
    public Material glass;

    Color Chroma(string data)
    {
        float intensity = 0.0f;
        Color c = new Color(0.0f, 0.0f, 0.0f, 0.0f);
        string[] tokens = data.Split(',');
        for (int i = 0; i < 4; ++i) { float.TryParse(tokens[i], out intensity); c[i] = intensity; }
        return c;
    }

    Vector2 Vec2(string data)
    {
        float value = 0.0f;
        Vector2 v2 = new Vector2(0.0f, 0.0f);
        string[] tokens = data.Split(',');
        for (int i = 0; i < 2; ++i) { float.TryParse(tokens[i], out value); v2[i] = value; }
        return v2;
    }

    Vector3 Vec3(string data)
    {
        float value = 0.0f;
        Vector3 v3 = new Vector3(0.0f, 0.0f, 0.0f);
        string[] tokens = data.Split(',');
        for (int i = 0; i < 3; ++i) { float.TryParse(tokens[i], out value); v3[i] = value; }
        return v3;
    }

    Vector4 Vec4(string data)
    {
        float value = 0.0f;
        Vector4 v4 = new Vector4(0.0f, 0.0f, 0.0f, 0.0f);
        string[] tokens = data.Split(',');
        for (int i = 0; i < 4; ++i) { float.TryParse(tokens[i], out value); v4[i] = value; }
        return v4;
    }

    public void SetAmbientLight(string data) { ambient.GetComponent<Light>().color = Chroma(data); }
    public void SetAmbientIntensity(float value) { ambient.GetComponent<Light>().intensity = value; }
    public void SetAmbientAngle(string data) { ambient.transform.localRotation = Quaternion.Euler(Vec3(data)); }

    public void SetSkyboxSunSize(float value) { skybox.SetFloat("_SunSize", value); }
    public void SetSkyboxConvergence(float value) { skybox.SetFloat("_SunSizeConvergence", value); }
    public void SetSkyboxThickness(float value) { skybox.SetFloat("_AtmosphereThickness", value); }
    public void SetSkyboxExposure(float value) { skybox.SetFloat("_Exposure", value); }
    public void SetSkyboxSkyTint(string data) { skybox.SetVector("_SkyTint", Chroma(data)); }
    public void SetSkyboxGround(string data) { skybox.SetVector("_GroundColor", Chroma(data)); }

    public void SetWaterRefraction(string data) { water.SetVector("_RefractionColor", Chroma(data)); }
    public void SetWaterScale(float value) { water.SetFloat("_WaveScale", value); }
    public void SetWaterSpeed(string data) { water.SetVector("_WaveSpeed", Vec4(data)); }

    public void SetGlassAlbedo(string data) { glass.SetVector("_Color", Chroma(data)); }
    public void SetGlassMetallic(float value) { glass.SetFloat("_Metallic", value); }
    public void SetGlassSmoothness(float value) { glass.SetFloat("_Glossiness", value); }
    public void SetGlassEmission(string data) { Color c = Chroma(data); c *= c.a; glass.SetVector("_EmissionColor", c); }

    public void SetBarLevels(string data)
    {
        float level = 0.0f;
        string[] tokens = data.Split(',');
        for (int i = 0; i < 16; ++i)
        {
            float.TryParse(tokens[i], out level);
            bars[i].transform.localScale = new Vector3(10.0f, 200.0f * level, 10.0f);
        }
    }
}
