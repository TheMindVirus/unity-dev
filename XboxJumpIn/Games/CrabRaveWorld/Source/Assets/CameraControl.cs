using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraControl : MonoBehaviour
{
    float speed = 0.1f;
    float sensitivity = 1.5f;
    float deadzone = 0.1f;
    float floor = 10.0f;
    Vector3 facing = new Vector3(0, 0, 0);
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

        Vector2 rightStick = new Vector2(Input.GetAxis("Right Stick X"), Input.GetAxis("Right Stick Y"));
        rightStick = new Vector2((Mathf.Abs(rightStick.x) > deadzone) ? rightStick.x * sensitivity : 0.0f,
                                 (Mathf.Abs(rightStick.y) > deadzone) ? rightStick.y * sensitivity : 0.0f);
        facing = new Vector3(rightStick.y, rightStick.x, 0);
        //BUG: Looking up and down causes strobe
        if ((facing.x < 180.0f) && (facing.x > 85.0f)) { facing.x = 85.0f; }
        else if ((facing.x > 180.0f) && (facing.x < 275.0f)) { facing.x = 275.0f; }
        transform.eulerAngles += facing;

        if (Input.GetKey(KeyCode.W)) { direction += new Vector3( 0,  0,  1); }
        if (Input.GetKey(KeyCode.S)) { direction += new Vector3( 0,  0, -1); }
        if (Input.GetKey(KeyCode.A)) { direction += new Vector3(-1,  0,  0); }
        if (Input.GetKey(KeyCode.D)) { direction += new Vector3( 1,  0,  0); }
        direction = direction * speed;
        transform.Translate(direction);

        direction = new Vector3(Input.GetAxis("Left Stick X"), 0, Input.GetAxis("Left Stick Y")) * speed;
        transform.Translate(direction);

        newpos = transform.position;
        if (newpos.y < floor) { newpos.y = floor; }
        transform.position = newpos;
    }
}