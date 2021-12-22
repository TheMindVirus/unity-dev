using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LiveInput : MonoBehaviour
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
        GetComponent<Renderer>().material.mainTexture = webcam;
        GetComponent<Renderer>().material.SetTextureScale("_MainTex", new Vector2(1.2f, 1.2f));
        GetComponent<Renderer>().material.SetTextureOffset("_MainTex", new Vector2(-0.3f, -0.1f));
        webcam.Play();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
