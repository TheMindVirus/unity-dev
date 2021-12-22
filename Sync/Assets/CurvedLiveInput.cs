using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CurvedLiveInput : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        WebCamDevice[] devices = WebCamTexture.devices;
        for (var i = 0; i < devices.Length; i++)
        {
            Debug.Log(devices[i].name);
        }

        WebCamTexture webcam = new WebCamTexture("Game Capture HD60 S");
        GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        GetComponent<Renderer>().material.SetTextureScale("_EmissionMap", new Vector2(1.0f, 1.0f));
        GetComponent<Renderer>().material.SetTextureOffset("_EmissionMap", new Vector2(0.0f, 0.0f));
        webcam.Play();
    }

    // Update is called once per frame
    void Update()
    {

    }
}
