using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class rotate : MonoBehaviour
{
    public GameObject Camera;
    public GameObject Door;
    bool Triggered = false;
    int State = 0;
    float CameraRotation = 0.0f;
    float CameraRotationTarget = 45.0f;
    float DoorRotation = 1.0f;
    float DoorRotationTarget = 45.0f;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if ((Input.GetKeyDown(KeyCode.Space)) && (!Triggered))
        {
            Triggered = true;
            Debug.Log("Triggering Sequence...");
        }
        if (Triggered)
        {
            if (State == 0)
            {
                CameraRotation += 1.0f;
                Camera.transform.Rotate(new Vector3(0.0f, -0.1f * CameraRotation, 0.0f));
                if (CameraRotation >= (CameraRotationTarget / (0.5f * Mathf.PI))) { State = 1; }
            }
            if (State == 1)
            {
                DoorRotation += 1.0f;
                Door.transform.Rotate(new Vector3(-0.1f * DoorRotation, 0.0f, 0.0f));
                if (DoorRotation >= (DoorRotationTarget / (0.5f * Mathf.PI))) { State = 2; }
            }
        }
    }
}
