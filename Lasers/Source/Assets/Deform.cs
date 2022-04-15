using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Deform : MonoBehaviour
{
    private static Vector3 crux;
    private static Vector3 scalex;
    private static Vector3 center;
    private static Vector3 position;
    private static float distance;
    private static float width;
    private static Material mat;
    private static GameObject target;

    public static bool Slice(Transform slicer, Transform source)
    {
        crux = new Vector3(slicer.position.x, source.position.y, source.position.z);
        scalex = source.localScale;
        center = (Vector3.right * scalex.x) / 2.0f;
        position = source.position;
        distance = Vector3.Distance(source.position, crux);
        if (distance >= scalex.x / 2.0f) { return false; }

        mat = source.GetComponent<MeshRenderer>().material;
        Destroy(source.gameObject);
        Create(position - center, crux, scalex, mat);
        Create(position + center, crux, scalex, mat);
        return true;
    }

    public static void Create(Vector3 pos, Vector3 crux, Vector3 scalex, Material mat)
    {
        target = GameObject.CreatePrimitive(PrimitiveType.Cube); //!!!INCORRECT!!!
        target.transform.position = (crux + pos) / 2.0f;
        width = Vector3.Distance(crux, pos);
        target.transform.localScale = new Vector3(width, scalex.y, scalex.z);
        target.AddComponent<Rigidbody>().mass = 100.0f;
        target.GetComponent<MeshRenderer>().material = mat;
    }
}
