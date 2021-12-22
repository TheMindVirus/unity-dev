using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BunkerScreen2 : MonoBehaviour
{
    public GameObject Screen1;
    public GameObject Screen2;
    public GameObject Screen3;
    public GameObject Screen4;
    public GameObject Screen5;
    public GameObject Screen6;
    public GameObject Screen7;
    public GameObject Screen8;
    public GameObject Screen9;

    // Start is called before the first frame update
    void Start()
    {
        WebCamDevice[] devices = WebCamTexture.devices;
        for (var i = 0; i < devices.Length; i++)
        {
            Debug.Log(devices[i].name);
        }

        WebCamTexture webcam = new WebCamTexture("Game Capture HD60 S");

        Screen1.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen1.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen1.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(0.0f, 0.0f));

        Screen2.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen2.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen2.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-1.0f, 0.0f));

        Screen3.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen3.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen3.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-2.0f, 0.0f));

        Screen4.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen4.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen4.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-3.0f, 0.0f));

        Screen5.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen5.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen5.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-4.0f, 0.0f));

        Screen6.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen6.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen6.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-5.0f, 0.0f));

        Screen7.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen7.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen7.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-6.0f, 0.0f));

        Screen8.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen8.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen8.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-7.0f, 0.0f));

        Screen9.GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        Screen9.GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(9.0f, 1.0f));
        Screen9.GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-8.0f, 0.0f));

        webcam.Play();
    }

    // Update is called once per frame
    void Update()
    {

    }
}
