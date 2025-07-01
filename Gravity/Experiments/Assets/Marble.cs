using UnityEngine;

public class Marble: MonoBehaviour
{
    public Transform ground;
    public Vector3 gravity;
    public Rigidbody body;

    Vector3 ClampMagnitude(Vector3 vec, float max)
    {
        float rd1 = Mathf.Sqrt((vec.x * vec.x) + (vec.y * vec.y) + (vec.z * vec.z));
        Vector3 res = new Vector3((vec.x / rd1) * max, (vec.y / rd1) * max, (vec.z / rd1) * max);
        //float rd2 = Mathf.Sqrt((res.x * res.x) + (res.y * res.y) + (res.z * res.z));
        //Debug.Log(res.ToString() + " | " + rd1.ToString() + " | " + rd2.ToString());
        //return res;
        //return (rd1 < rd2) ? vec : res;
        return (rd1 < max) ? vec : res;
    }

    Vector3 Normalise(Vector3 vec)
    {
        float radius = Mathf.Sqrt((vec.x * vec.x) + (vec.y * vec.y) + (vec.z * vec.z));
        return new Vector3(vec.x / radius, vec.y / radius, vec.z / radius);
    }

    void Start()
    {
        ground = GameObject.Find("Ground").transform;
        body = this.gameObject.GetComponent<Rigidbody>();

        Vector3 test = new Vector3(1.0f, 2.0f, 3.0f);
        Vector3 control = Vector3.ClampMagnitude(test, 9.81f);
        Vector3 result = ClampMagnitude(test, 9.81f);
        Debug.Log(test.ToString() + " | " + control.ToString() + " | " + result.ToString());
    }

    void Update()
    {
        Vector3 move = new Vector3((Input.GetKey("d") ? 1 : 0) - (Input.GetKey("a") ? 1 : 0), 0, (Input.GetKey("w") ? 1 : 0) - (Input.GetKey("s") ? 1 : 0));
        move = Vector3.ClampMagnitude(move, 1.0f); // Optional: prevents faster diagonal movement
        if (move == Vector3.zero) { body.velocity = new Vector3(0.0f, 0.0f, 0.0f); body.ResetInertiaTensor(); }

        gravity = Vector3.ClampMagnitude(ground.position - transform.position, 9.81f);
        //body.AddRelativeForce(move + transform.forward);
        body.AddForce(move + transform.up);
        body.AddForce(gravity);
    }
}
