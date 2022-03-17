using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraControl : MonoBehaviour
{
    float accel = 0.001f;
    float maxspeed = 0.2f;
    float sensitivity = 1.5f;
    float floor = 10.0f;
    Vector3 facing = new Vector3(0, 0, 0);
    Vector3 speed = new Vector3(0, 0, 0);
    Vector3 direction = new Vector3(0, 0, 0);
    Vector3 newpos = new Vector3(0, 0, 0);

    void Start()
    {
        //Use with Web Pointer Lock API
    }

    void Update()
    {
        facing = new Vector3(transform.eulerAngles.x + (Input.GetAxis("Mouse Y") * sensitivity * -1.0f),
                             transform.eulerAngles.y + (Input.GetAxis("Mouse X") * sensitivity), 0);
        //BUG: Looking up and down causes strobe
        if ((facing.x < 180.0f) && (facing.x > 85.0f)) { facing.x = 85.0f; }
        else if ((facing.x > 180.0f) && (facing.x < 275.0f)) { facing.x = 275.0f; }
        transform.eulerAngles = facing;

        speed -= direction;
        if (Input.GetKey(KeyCode.W)) { direction += new Vector3( 0,  0,  accel); }
        if (Input.GetKey(KeyCode.S)) { direction += new Vector3( 0,  0, -accel); }
        if (Input.GetKey(KeyCode.A)) { direction += new Vector3(-accel,  0,  0); }
        if (Input.GetKey(KeyCode.D)) { direction += new Vector3( accel,  0,  0); }
        speed += direction;

        if (speed.x > maxspeed) { speed.x = maxspeed; }
        if (speed.x < -maxspeed) { speed.x = -maxspeed; }
        if (speed.z > maxspeed) { speed.z = maxspeed; }
        if (speed.z < -maxspeed) { speed.z = -maxspeed; }

        transform.Translate(speed);
        newpos = transform.position;
        if (newpos.y < floor) { newpos.y = floor; }
        transform.position = newpos;
    }
}