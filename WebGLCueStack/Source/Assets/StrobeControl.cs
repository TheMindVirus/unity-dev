using UnityEngine;

public class StrobeControl : MonoBehaviour
{
    public GameObject Backlight = null;
    public GameObject Rokon = null;
    public GameObject Glass = null;
    public GameObject Frame = null;
    public GameObject Backdrop = null;
    public AudioSource audio1 = null;
    float intensity = 0.0f;
    float secondary = 0.0f;
    void Update()
    {
        intensity = Mathf.Sin(audio1.time * 10.0f) * 10.0f;
        secondary = 1.0f - (intensity / 10.0f);
        Backlight.GetComponent<Light>().intensity = intensity;
        Rokon.GetComponent<Renderer>().material.SetColor("_EmissionColor", new Color(1.0f, secondary, secondary, 1.0f));
        Glass.GetComponent<Renderer>().material.SetColor("_EmissionColor", new Color(1.0f, secondary, secondary, 1.0f));
        Frame.GetComponent<Renderer>().material.SetColor("_Color", new Color(intensity, 0.0f, 0.0f, 1.0f));
        Backdrop.GetComponent<Renderer>().material.SetColor("_Color", new Color(intensity, 0.0f, 0.0f, 1.0f));
    }
}
