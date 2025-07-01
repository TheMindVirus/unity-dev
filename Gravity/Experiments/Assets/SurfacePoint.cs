using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SurfacePoint : MonoBehaviour
{
    public Vector3 ground;
    public Vector3 gravity;
    public Vector3 move;
    public Vector3 normal;
    public Rigidbody body;
    public LineRenderer line;

    void Start()
    {
        body = GetComponent<Rigidbody>();
        line = GetComponent<LineRenderer>();
    }

    void Update()
    {
        move = new Vector3((Input.GetKey("d") ? 1 : 0) - (Input.GetKey("a") ? 1 : 0), 0, (Input.GetKey("w") ? 1 : 0) - (Input.GetKey("s") ? 1 : 0));
        move = Vector3.ClampMagnitude(move, 1.0f); // Optional: prevents faster diagonal movement

        if (move == Vector3.zero) { body.velocity = new Vector3(0.0f, 0.0f, 0.0f); body.ResetInertiaTensor(); }
        gravity = Vector3.ClampMagnitude(ground - transform.position, 9.81f);

        normal = gravity; //transform.up
        move = Vector3.ProjectOnPlane(move, normal);

        body.AddForce(move);
        body.AddForce(gravity);

        line.SetPosition(0, transform.position);
        line.SetPosition(1, transform.position + move);
    }

    void OnCollisionStay(Collision hit)
    {
        Vector3 average = Vector3.zero;
        for (int i = 0; i < hit.contactCount; ++i)
        {
            Vector3 contact = hit.GetContact(i).point;
            average += contact;
        }
        average /= hit.contactCount;
        ground = average;
    }
}
