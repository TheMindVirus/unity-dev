using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Laser : MonoBehaviour
{
    void OnCollisionEnter(UnityEngine.Collision collision)
    {
        Deform.Slice(this.transform, collision.transform);
    }
}
