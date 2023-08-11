using UnityEngine;
using System.Runtime.InteropServices;

public class CameraControl : MonoBehaviour
{
    [DllImport("__Internal")]
    static extern void anchor(string message);

    public Transform a0 = null;
    public Transform a1 = null;
    public Transform a2 = null;
    public Transform a3 = null;

    private Vector3 p0 = new Vector3(0, 0, 0);
    private Vector3 p1 = new Vector3(0, 0, 0);
    private Vector3 p2 = new Vector3(0, 0, 0);
    private Vector3 p3 = new Vector3(0, 0, 0);

    void Update()
    {
        transform.Rotate(-Input.GetAxis("Mouse Y"), Input.GetAxis("Mouse X"), 0.0f);
        p0 = Camera.main.WorldToScreenPoint(a0.position);
        p1 = Camera.main.WorldToScreenPoint(a1.position);
        p2 = Camera.main.WorldToScreenPoint(a2.position);
        p3 = Camera.main.WorldToScreenPoint(a3.position);
        anchor(p0.ToString() + ", " + p1.ToString() + ", " + p2.ToString() + ", " + p3.ToString());
    }
}
