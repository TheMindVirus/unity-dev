using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FlatScreen : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        foreach (var device in WebCamTexture.devices)
        {
            Debug.Log("Capture Card: " + device.name);
        }

	/*	foreach (var device in Microphone.devices)
        {
            Debug.Log("Sound Card: " + device);
        }
*/
		var webcam_selected = "Game Capture HD60 S"; //WebCamTexture.devices[0].name;
        WebCamTexture webcam = new WebCamTexture(webcam_selected);
        GetComponent<Renderer>().material.SetTexture("_EmissionMap", webcam);
        GetComponent<Renderer>().material.SetTextureScale("_EmissionMap", new Vector2(1.0f, 1.0f));
        GetComponent<Renderer>().material.SetTextureOffset("_EmissionMap", new Vector2(0.0f, 0.0f));
    /*    
		var microphone_selected = Microphone.devices[0]; //"Line (Elgato Sound Capture)"; //Microphone.devices[0];
		var sample_rate_min = 48000;
		var sample_rate = 48000;
		Microphone.GetDeviceCaps(microphone_selected, out sample_rate_min, out sample_rate);
		AudioSource microphone = GetComponent<AudioSource>();
		microphone.clip = Microphone.Start(microphone_selected, true, 10, 48000);
		microphone.loop = true;
		while (!(Microphone.GetPosition(null) > 0)) {}
*/
		webcam.Play();
		//microphone.Play();
		//Debug.Log("Capture Card: " + webcam_selected + " | Sound Card: " + microphone_selected);
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.F11))
        {
            if (Screen.fullScreen == false) { Screen.fullScreen = true; }
            else { Screen.fullScreen = false; }
        }
    }
}
