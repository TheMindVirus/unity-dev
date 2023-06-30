using UnityEngine;

public class Pivot : MonoBehaviour
{
    void Update()
    {
        transform.Rotate(-Input.GetAxis("Mouse Y"), Input.GetAxis("Mouse X"), Input.GetAxis("Mouse ScrollWheel") * 100.0f, Space.World);
    }
}
