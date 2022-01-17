using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MorePhysics : MonoBehaviour
{
    private bool held;
    private Cloth bbox;
    private Rigidbody body;
    private Vector3 cursor;
    private float mousespeed;
    private float hysteresis;

    void Start()
    {
        held = false;
        bbox = GetComponent<Cloth>();
        body = GetComponent<Rigidbody>();
        mousespeed = 20.0f;
        hysteresis = 1000.0f;
    }
 
    void Update()
    {
        if (held == true)
        {
            cursor = new Vector3(transform.position.x + (Input.GetAxis("Mouse X") * -mousespeed),
                                 transform.position.y + (Input.GetAxis("Mouse Y") * mousespeed),
                                 transform.position.z + (Input.GetAxis("Mouse ScrollWheel") * -mousespeed * 10.0f));
            transform.position = new Vector3(transform.position.x + ((cursor.x - transform.position.x) / hysteresis),
                                             transform.position.y + ((cursor.y - transform.position.y) / hysteresis),
                                             transform.position.z + ((cursor.z - transform.position.z) / hysteresis));
        }
    }

    void OnMouseDown() { held = true; bbox.useGravity = false; body.useGravity = false; Debug.Log(name); }
    void OnMouseUp() { held = false; bbox.useGravity = false; body.useGravity = true; }
}