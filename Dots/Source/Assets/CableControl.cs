using UnityEngine;

public class CableControl : MonoBehaviour
{
    public GameObject Cursor;
    public GameObject Cable;
    GameObject go;

    Ray ray;
    RaycastHit hit;
    Vector3 origin;
    Vector3 mouse;
    bool click;
    bool _lock;
    bool mode;
    float sag;

    void Start()
    {
        if (Cursor == null) { Cursor = GameObject.CreatePrimitive(PrimitiveType.Sphere); Cursor.name = "Cursor"; }
        DestroyImmediate(Cursor.GetComponent<Collider>());

        origin = new Vector3(0.0f, 0.0f, 0.0f);
        mouse = new Vector3(0.0f, 0.0f, 0.0f);
        click = false;
        _lock = false;
        mode = false;
        sag = 2.0f;

        //This utter nonsensical garbage is for disabling off-screen camera culling
        //Camera.main.cullingMatrix = Matrix4x4.Ortho(-99999, -99999, -99999, -99999, 0.001f, 99999)
        //                          * Matrix4x4.Translate(Vector3.forward * -99999 / 2.0f)
        //                          * Camera.main.worldToCameraMatrix;
        Camera.main.cullingMatrix = new Matrix4x4();
    }

    void Update()
    {
        mouse = new Vector3(Input.mousePosition.x / Screen.width,
                            Input.mousePosition.y / Screen.height, 1.0f);
        sag += Input.GetAxis("Mouse ScrollWheel");
        ray = Camera.main.ViewportPointToRay(mouse);
        if (Physics.Raycast(ray, out hit))
        {
            Cursor.transform.localPosition = hit.point;
            click = Input.GetMouseButton(0);
            if (_lock != click)
            {
                _lock = click;
                if (click == true)
                {
                    mode = !mode;
                    if (mode == true)
                    {
                        go = GameObject.Instantiate(Cable);
                        go.transform.position = origin;
                        go.GetComponent<Renderer>().material.SetVector("_Position1", hit.point);
                    }
                    Debug.Log(hit.point);
                }
            }
            if (mode == true)
            {
                go.GetComponent<Renderer>().material.SetVector("_Position2", hit.point);
                go.GetComponent<Renderer>().material.SetFloat("_Sag", sag);
            }
        }
    }
}
