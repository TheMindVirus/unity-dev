using UnityEngine;
//using UnityEditor;
using System.Collections;
using System.Collections.Generic;

[ExecuteInEditMode]
public class NewBehaviourScript : MonoBehaviour
{
    //public GameObject parent1;
    //public GameObject parent2;
    public List<GameObject> parents;

    // Awake is called before the first frame update
    void Awake()
    {
        //parent1 = GameObject.Find("Parent1");
        //parent2 = GameObject.Find("Parent2");

        parents.Add(GameObject.Find("Parent1"));
        parents.Add(GameObject.Find("Parent2"));
    }

    // Update is called once per frame in the editor
    void Update()
    {
        //transform.position = new Vector3(0.0f, 0.0f, 0.0f);
        //transform.rotation.eulerAngles = new Vector3(0.0f, 0.0f, 0.0f);

        //transform.position += (parent1.transform.position + parent2.transform.position) / 2;
        //transform.rotation.eulerAngles = (parent1.transform.rotation.eulerAngles + parent2.transform.rotation.eulerAngles) / 2;

        uint count = 0;
        Vector3 position = new Vector3(0.0f, 0.0f, 0.0f);
        Vector3 rotation = new Vector3(0.0f, 0.0f, 0.0f);
        foreach (var parent in parents)
        {
            count += 1;
            position += parent.transform.position;
            rotation += parent.transform.rotation.eulerAngles;
        }
        position /= count;
        rotation /= count;
        transform.position = position;
        //transform.rotation.eulerAngles = rotation;
        //transform.rotation = Quaternion.Euler(rotation.xyz);
        transform.rotation = Quaternion.Euler(rotation.x, rotation.y, rotation.z);
    }
}
