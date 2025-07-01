using UnityEngine;

public class Gravity : MonoBehaviour
{
    public Transform ground;
    public Vector3 gravity;
    public Rigidbody body;

    void Start()
    {
        ground = GameObject.Find("Sphere").transform;
        body = this.gameObject.GetComponent<Rigidbody>();
    }

    void Update()
    {
        transform.LookAt(ground);
        transform.Rotate(new Vector3(-90.0f, 0.0f, 0.0f));
        //transform.Translate(gravity * Time.deltaTime);

        Vector3 move = new Vector3((Input.GetKey("d") ? 1 : 0) - (Input.GetKey("a") ? 1 : 0), 0, (Input.GetKey("w") ? 1 : 0) - (Input.GetKey("s") ? 1 : 0));
        move = Vector3.ClampMagnitude(move, 1.0f); // Optional: prevents faster diagonal movement
        if (move == Vector3.zero) { body.velocity = new Vector3(0.0f, 0.0f, 0.0f); body.ResetInertiaTensor(); }

        gravity = Vector3.ClampMagnitude(ground.position - transform.position, 9.81f);
        body.AddRelativeForce(move + transform.forward);
        body.AddForce(gravity);
    }
}
