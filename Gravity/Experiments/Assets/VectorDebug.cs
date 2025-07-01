using UnityEngine;

public class VectorDebug : MonoBehaviour
{
    public Transform ground;
    public Vector3 gravity;
    public Rigidbody body;
    public LineRenderer line;

    public Vector3 angle = Vector3.zero;

    public Vector3 orient = new Vector3(0.0f, 45.0f, 0.0f);
    public Vector3 origin = new Vector3(0.0f, 5.0f, 0.0f);
    public Vector3 zero = Vector3.zero;

    public Vector3 debug = Vector3.zero;

    Vector3 Gravity(Vector3 pos, Vector3 gnd, float acc = 9.81f)
    {
        Vector3 vec = gnd - pos;
        float radius = Mathf.Sqrt((vec.x * vec.x) + (vec.y * vec.y) + (vec.z * vec.z));
        return new Vector3((vec.x / radius) * acc, (vec.y / radius) * acc, (vec.z / radius) * acc);
    }

    Vector3 Rotor(Vector3 pos, Vector3 rot, Vector3 piv)
    {
        Vector3 mov = pos - piv;
        Vector3 _m0 = new Vector3(0.0f, 0.0f, 0.0f);
        Vector3 _m1 = new Vector3(0.0f, 0.0f, 0.0f);;
        Vector3 _m2 = new Vector3(0.0f, 0.0f, 0.0f);;
        _m0.x = Mathf.Cos(rot.x) * Mathf.Cos(rot.z);
        _m0.y = (-1.0f * Mathf.Cos(rot.y) * Mathf.Sin(rot.z)) + (Mathf.Sin(rot.y) * Mathf.Sin(rot.x) * Mathf.Cos(rot.z));
        _m0.z = (Mathf.Sin(rot.y) * Mathf.Sin(rot.z)) + (Mathf.Cos(rot.y) * Mathf.Sin(rot.x) * Mathf.Cos(rot.z));
        _m1.x = Mathf.Cos(rot.x) * Mathf.Sin(rot.z);
        _m1.y = (Mathf.Cos(rot.y) * Mathf.Cos(rot.z)) + (Mathf.Sin(rot.y) * Mathf.Sin(rot.x) * Mathf.Sin(rot.z));
        _m1.z = (-1.0f * Mathf.Sin(rot.y) * Mathf.Cos(rot.z)) + (Mathf.Cos(rot.y) * Mathf.Sin(rot.x) * Mathf.Sin(rot.z));
        _m2.x = (-1.0f * Mathf.Sin(rot.x));
        _m2.y = Mathf.Sin(rot.y) * Mathf.Cos(rot.x);
        _m2.z = Mathf.Cos(rot.y) * Mathf.Cos(rot.x);
        Vector3 res = new Vector3((mov.x * _m0.x) + (mov.y * _m0.y) + (mov.z * _m0.z),
                                  (mov.x * _m1.x) + (mov.y * _m1.y) + (mov.z * _m1.z),
                                  (mov.x * _m2.x) + (mov.y * _m2.y) + (mov.z * _m2.z));
      return res + piv;
    }

    void Start()
    {
        ground = GameObject.Find("Sphere").transform;
        body = this.gameObject.GetComponent<Rigidbody>();
        line = this.gameObject.GetComponent<LineRenderer>();
        orient = new Vector3(0.0f, 45.0f, 0.0f);
        origin = new Vector3(0.0f, 5.0f, 0.0f);
    }

    void Update()
    {
        transform.LookAt(ground);
        transform.Rotate(new Vector3(-90.0f, 0.0f, 0.0f));
        //transform.Translate(gravity * Time.deltaTime);

        Vector3 move = new Vector3((Input.GetKey("d") ? 1 : 0) - (Input.GetKey("a") ? 1 : 0), 0, (Input.GetKey("w") ? 1 : 0) - (Input.GetKey("s") ? 1 : 0));
        move = Vector3.ClampMagnitude(move, 1.0f); // Optional: prevents faster diagonal movement
        if (move == Vector3.zero) { body.velocity = new Vector3(0.0f, 0.0f, 0.0f); body.ResetInertiaTensor(); }

        gravity = Gravity(transform.position, ground.position);
        body.AddForce(gravity);

        //body.AddRelativeForce(transform.forward + move);
        //body.AddForce(transform.position + (Vector3.RotateTowards(move, transform.forward, 1.0f)));
        //body.AddForce(transform.position + (Quaternion.AngleAxis(0.0f, transform.forward) * move));

        //line.SetPosition(0, transform.position);
        //line.SetPosition(1, gravity);
        //line.SetPosition(1, transform.position + (Vector3.RotateTowards(move, transform.forward, 1.0f)));

        angle = transform.rotation.eulerAngles;
        //angle = new Vector3(Vector3.Angle(transform.rotation.eulerAngles, Vector3.forward),
        //                    Vector3.Angle(transform.rotation.eulerAngles, Vector3.up),
        //                    Vector3.Angle(transform.rotation.eulerAngles, Vector3.right));

        orient = (angle / 180.0f) * Mathf.PI;
        orient = new Vector3(orient.y, orient.x, orient.z); debug = orient;
        //if ((orient.x > Mathf.PI * 1.0f) && (orient.x < Mathf.PI * 1.5f)) { move.z = -move.z; }
        if (transform.position.y <= ground.position.y) { move.z = -move.z; }
        if (transform.position.z >= ground.position.z) { move.x = -move.x; }
        orient = origin + Rotor(move, orient, zero);
        origin = transform.position;
        line.SetPosition(0, origin);
        line.SetPosition(1, orient);

        body.AddForce(orient);
    }
}
