using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Physics : MonoBehaviour
{
    private float speed;
    private float accel;
    private float maxspeed;
    private float angle;
    private float angular;
    private float maxturn;

    void Start()
    {
        speed = 0.0f;
        accel = 0.05f; //0.01f;
        maxspeed = 120.0f; //10.0f;
        angle = 0.0f;
        angular = 0.05f;
        maxturn = 2.0f * Mathf.PI;
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.W)) { speed += accel; }
        else if (Input.GetKey(KeyCode.S)) { speed -= accel; }
        else { if (speed < -accel) { speed += accel; } else if (speed > accel) { speed -= accel; } else { speed = 0.0f; } }
        if (speed > maxspeed) { speed = maxspeed; }
        if (speed < -maxspeed) { speed = -maxspeed; }

        if (Input.GetKey(KeyCode.A)) { angle -= angular; }
        else if (Input.GetKey(KeyCode.D)) { angle += angular; }
        else { if (angle < -0.001f) { angle += angular; } else if (angle > 0.001f) { angle -= angular; } else { angle = 0.0f; } }
        if (angle > maxturn) { angle = maxturn; }
        if (angle < -maxturn) { angle = -maxturn; }
        //angle *= Mathf.Clamp(speed, -1.0f, 1.0f); //Mathf.Sin(Mathf.PI * Mathf.Abs(speed / maxspeed));
        float tmpfix = angle * Mathf.Clamp(speed, -1.0f, 1.0f);
        transform.Rotate(new Vector3(0.0f, tmpfix, 0.0f), Space.World);
        transform.Translate(Vector3.right * speed, Space.Self);
        transform.Find("Node-Quadra_dot_io/Inner-Node-Quadra_dot_io-8/ninefiftyfive").Rotate(new Vector3(0.0f, 0.0f, speed * Mathf.PI));
        transform.Find("Node-Quadra_dot_io/Inner-Node-Quadra_dot_io-3/twosixtythree").Rotate(new Vector3(0.0f, 0.0f, -speed * Mathf.PI));
    }
}
