using UnityEngine;

public class Movement : MonoBehaviour
{
    GameObject axis;
    GameObject player;
    Vector3 root;
    Vector3 motion;
    float gravity;
    float altitude;

    void Start()
    {
        axis = GameObject.Find("Axis");
        player = GameObject.Find("Player");
        root = new Vector3(0.0f, 0.0f, 0.0f);
        motion = new Vector3(0.0f, 0.0f, 0.0f);
        gravity = -9.81f;
        altitude = 4.0f;
    }

    void Update()
    {
        root = new Vector3(0.0f, 0.0f, 0.0f);
        motion = new Vector3(0.0f, 0.0f, 0.0f);
        if (Input.GetKey("w")) { motion.x += 1.0f; }
        if (Input.GetKey("s")) { motion.x += -1.0f; }
        if (Input.GetKey("w") && Input.GetKey("s")) { motion.x = 0.0f; }
        if (!Input.GetKey("w") && !Input.GetKey("s")) { motion.x = 0.0f; }
        if (Input.GetKey("a")) { motion.z += 1.0f; }
        if (Input.GetKey("d")) { motion.z += -1.0f; }
        if (Input.GetKey("a") && Input.GetKey("d")) { motion.z = 0.0f; }
        if (!Input.GetKey("a") && !Input.GetKey("d")) { motion.z = 0.0f; }
        if (Input.GetKey("space")) { altitude = 5.0f; }
        if (!Input.GetKey("space")) { altitude = 4.0f; }
        //motion.y = normalise(motion.x, motion.z); //LookAt
        root.y = altitude;
        player.transform.localPosition = root;
        transform.Rotate(motion);
    }
}
