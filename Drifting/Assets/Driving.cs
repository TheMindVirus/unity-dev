using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Driving : MonoBehaviour
{
    private Rigidbody bbox;

    private GameObject FL;
    private GameObject FR;
    private GameObject RL;
    private GameObject RR;

    private float speed = 0.0f;
    private float steering = 0.0f;

    // Start is called before the first frame update
    void Start()
    {
        speed = 100.0f;
        steering = 15.0f;
        bbox = GetComponent<Rigidbody>();
        FL = transform.Find("WheelFrontLeft").gameObject;
        FR = transform.Find("WheelFrontRight").gameObject;
        RL = transform.Find("WheelRearLeft").gameObject;
        RR = transform.Find("WheelRearRight").gameObject;
    }

    // Update is called once per frame
    void Update()
    {
        Debug.Log(bbox.velocity.x + ", " + bbox.angularVelocity.y);
        if (Mathf.Abs(bbox.velocity.x) < (speed * 100.0f)) { bbox.AddRelativeForce(new Vector3(-speed * bbox.mass, 0.0f, 0.0f), ForceMode.Force); }
        if (Mathf.Abs(bbox.angularVelocity.y) < (steering / 10.0f)) { bbox.AddRelativeTorque(new Vector3(0.0f, bbox.mass * steering * (speed / 100.0f), 0.0f), ForceMode.Impulse); }
        FL.transform.localRotation = Quaternion.Euler(FL.transform.localRotation.x - (bbox.velocity.x * 30.0f), -90.0f + steering, FL.transform.localRotation.z);
        FR.transform.localRotation = Quaternion.Euler(FR.transform.localRotation.x + (bbox.velocity.x * 30.0f),  90.0f + steering, FR.transform.localRotation.z);
        RL.transform.localRotation = Quaternion.Euler(RL.transform.localRotation.x - (bbox.velocity.x * 30.0f), -90.0f + RL.transform.localRotation.y, RL.transform.localRotation.z);
        RR.transform.localRotation = Quaternion.Euler(RR.transform.localRotation.x + (bbox.velocity.x * 30.0f),  90.0f + RR.transform.localRotation.y, RR.transform.localRotation.z);
    }
}
