using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Look : MonoBehaviour
{
    float sensitivity = 1.5f;
    Vector3 facing = new Vector3(0, 0, 0);

    void Update()
    {
        facing = new Vector3(transform.eulerAngles.x + (Input.GetAxis("Mouse Y") * sensitivity * -1.0f),
                             transform.eulerAngles.y + (Input.GetAxis("Mouse X") * sensitivity), 0);
        //BUG: Looking up and down causes strobe
        if ((facing.x < 180.0f) && (facing.x > 85.0f)) { facing.x = 85.0f; }
        else if ((facing.x > 180.0f) && (facing.x < 275.0f)) { facing.x = 275.0f; }
        transform.eulerAngles = facing;
    }
}