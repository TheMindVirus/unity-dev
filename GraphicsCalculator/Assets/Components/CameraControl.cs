using UnityEngine;
using UnityEngine.InputSystem;
using System.Collections;
using System.Collections.Generic;

public class CameraControl : MonoBehaviour
{
    float speed = 0.1f;
    float sensitivity = 0.15f;
    float floor = 1.0f;
    float deadzone = 0.1f;
    Vector3 direction = new Vector3(0, 0, 0);
    Vector3 newpos = new Vector3(0, 0, 0);
    Vector2 rightStick = new Vector2(0, 0);
    Vector2 leftStick = new Vector2(0, 0);

    void Update()
    {
        var mouse = Mouse.current;
        if (mouse != null)
        {
            transform.Rotate(new Vector3(mouse.delta.y.ReadValue() * -sensitivity, 0, 0), Space.Self);
            transform.Rotate(new Vector3(0, mouse.delta.x.ReadValue() * sensitivity, 0), Space.World);
        }

        var keyboard = Keyboard.current;
        if (keyboard != null)
        {
            if (keyboard.wKey.isPressed) { direction += new Vector3( 0,  0,  1); }
            if (keyboard.sKey.isPressed) { direction += new Vector3( 0,  0, -1); }
            if (keyboard.aKey.isPressed) { direction += new Vector3(-1,  0,  0); }
            if (keyboard.dKey.isPressed) { direction += new Vector3( 1,  0,  0); }
        }

        var gamepad = Gamepad.current;
        if (gamepad != null)
        {
            rightStick = gamepad.rightStick.ReadValue();
            rightStick = new Vector2((Mathf.Abs(rightStick.x) > deadzone) ? rightStick.x * sensitivity : 0.0f,
                                     (Mathf.Abs(rightStick.y) > deadzone) ? rightStick.y * sensitivity : 0.0f);
            transform.Rotate(new Vector3(-1.0f * rightStick.y, 0, 0), Space.Self);
            transform.Rotate(new Vector3(0, rightStick.x, 0), Space.World);
            leftStick = gamepad.leftStick.ReadValue();
            leftStick = new Vector2((Mathf.Abs(leftStick.x) > deadzone) ? leftStick.x * sensitivity : 0.0f,
                                    (Mathf.Abs(leftStick.y) > deadzone) ? leftStick.y * sensitivity : 0.0f);
            direction += new Vector3(leftStick.x, 0, -1.0f * leftStick.y);
        }

        direction = direction * speed;
        transform.Translate(new Vector3(direction.x, 0, 0), Space.Self);
        transform.Translate(new Vector3(0, 0, direction.z), Space.Self);
        newpos = transform.position;
        if (newpos.y < floor) { newpos.y = floor; }
        transform.position = newpos;
    }
}