using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraControl : MonoBehaviour
{
    void Update()
    {
        transform.Rotate(new Vector3(Input.GetAxis("Mouse Y"), 0.0f, 0.0f), Space.Self);
        transform.Rotate(new Vector3(0.0f, Input.GetAxis("Mouse X"), 0.0f), Space.World);
        transform.Rotate(new Vector3(Input.GetAxis("Right Stick X") * 2.0f, 0.0f, 0.0f), Space.Self);
        transform.Rotate(new Vector3(0.0f, Input.GetAxis("Right Stick Y") * 2.0f, 0.0f), Space.World);
        transform.Translate(new Vector3(Input.GetAxis("Keyboard X"), 0.0f, Input.GetAxis("Keyboard Y")), Space.Self);
        transform.Translate(new Vector3(Input.GetAxis("Left Stick X"), 0.0f, Input.GetAxis("Left Stick Y")), Space.Self);
    }
}