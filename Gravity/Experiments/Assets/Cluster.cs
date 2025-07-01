using UnityEngine;
using System.Collections;
using System.Collections.Generic;

[ExecuteInEditMode]
public class Cluster : MonoBehaviour
{
    public List<GameObject> cluster;

    void Update()
    {
        cluster = new List<GameObject>();
        foreach (GameObject node in GameObject.FindObjectsOfType<GameObject>())
        {
            if (node.name == "Cluster") { cluster.Add(node); }
        }

        uint count = 0;
        Vector3 position = new Vector3(0.0f, 0.0f, 0.0f);
        Vector3 rotation = new Vector3(0.0f, 0.0f, 0.0f);
        foreach (var node in cluster)
        {
            if (node != this)
            {
                count += 1;
                position += node.transform.position;
                rotation += node.transform.rotation.eulerAngles;
            }
        }
        position /= count;
        rotation /= count;
        transform.position = position;
        transform.rotation = Quaternion.Euler(rotation.x, rotation.y, rotation.z);
    }
}
