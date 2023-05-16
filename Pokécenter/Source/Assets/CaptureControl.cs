using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class CaptureControl : MonoBehaviour
{
    public Material output = null;
    int captureWidth = 1280;
    int captureHeight = 720;
    float captureFPS = 59.94f;
    int captureSelect = 0;

    public void Start() { SelectDevice(captureSelect); }

    public void SelectDevice(int selected = 0) // = 1)
    {
        captureSelect = selected;
        WebCamDevice[] devices = WebCamTexture.devices;
        Debug.Log("[INFO]: Selected: " + selected.ToString() + ": " + devices[selected].name);

        WebCamTexture webcam = new WebCamTexture(devices[selected].name);
        output.SetTexture("_EmissionMap", webcam);
        output.SetTextureScale("_EmissionMap", new Vector2(1.0f, 1.0f));
        output.SetTextureOffset("_EmissionMap", new Vector2(0.0f, 0.0f));
        webcam.wrapMode = TextureWrapMode.Repeat;
        webcam.filterMode = FilterMode.Point;
        webcam.requestedWidth = captureWidth;
        webcam.requestedHeight = captureHeight;
        webcam.requestedFPS = captureFPS;
        webcam.Play();
    }

    public void CaptureWidth(int width = 1280) { captureWidth = width; SelectDevice(captureSelect); }
    public void CaptureHeight(int height = 720) { captureHeight = height; SelectDevice(captureSelect); }
    public void CaptureFPS(float fps = 59.94f) { captureFPS = fps; SelectDevice(captureSelect); }
}
