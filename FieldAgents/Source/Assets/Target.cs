using UnityEngine;

public class Target : MonoBehaviour
{
    public Transform target = null;
    public float speed = 0.01f;
    public float threshold = 1.0f;

    void Update()
    {
        transform.LookAt(target.position);
        transform.position = Vector3.MoveTowards(transform.position, target.position, speed);
        if (Vector3.Distance(transform.position, target.position) < threshold) { transform.position = target.position; }
        //add sphere colliders along trail at absolute position on grid
    }
}


