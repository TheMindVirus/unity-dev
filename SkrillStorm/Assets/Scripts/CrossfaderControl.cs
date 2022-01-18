using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CrossfaderControl : MonoBehaviour
{
    public AudioSource AudioSourceA;
    public AudioSource AudioSourceB;

    private RaycastHit hit;
    private Ray ray;
    private float distance;
    private float value;
    private float sensitivity;
    private bool hovering;
    private bool selected;
    private Vector3 origin;
    private UnityEngine.UI.Text HUD;
    private LineRenderer Line;

    // Start is called before the first frame update
    void Start()
    {
        hit = new RaycastHit();
        ray = new Ray();
        distance = 0.12f;
        value = 0.5f;
        sensitivity = 0.5f;
        origin = transform.position;
        HUD = GameObject.Find("/Player/HUD/Text").GetComponent<UnityEngine.UI.Text>();
        //Line = GameObject.Find("Line").GetComponent<LineRenderer>();
    }

    // Update is called once per frame
    void Update()
    {
        ray = Camera.main.ViewportPointToRay(new Vector3(0.5f, 0.5f, 0.0f));
        //Debug.DrawRay(ray.origin, Camera.main.transform.forward, Color.green);
        //Line.SetPosition(0, ray.origin);
        //Line.SetPosition(1, ray.direction);
        if (Physics.Raycast(ray, out hit))
        {
            //Debug.Log(hit.collider.transform.gameObject.name);
            if (!selected) { HUD.text = hit.collider.transform.gameObject.name; }
            if (hit.collider.transform.gameObject == transform.gameObject) { hovering = true; }
            else { hovering = false; }
        }
        else { HUD.text = "Spaceship"; } //Bug, Inside of Collider Not Detected
        if ((hovering) && (Input.GetMouseButton(0))) { selected = true; }
        else if (!Input.GetMouseButton(0)) { selected = false; }
        if (selected)
        {
            transform.gameObject.GetComponent<Renderer>().material.SetColor("_Color", Color.blue);
            value += (Input.GetAxis("Mouse X") * sensitivity);
            if (value > 1.0f) { value = 1.0f; }
            if (value < 0.0f) { value = 0.0f; }
            transform.position = new Vector3(origin.x + ((value - 0.5f) * distance), origin.y, origin.z);
            //SET_TRACK_VOLUMES//
            AudioSourceA.volume = 1.0f - ((Mathf.Clamp(value, 0.5f, 1.0f) - 0.5f) * 2.0f);
            AudioSourceB.volume = Mathf.Clamp(value, 0.0f, 0.5f) * 2.0f;
            /////////////////////
            HUD.text = transform.gameObject.name;
        }
        else if (hovering)
        {
            transform.gameObject.GetComponent<Renderer>().material.SetColor("_Color", Color.green);
        }
        else
        {
            transform.gameObject.GetComponent<Renderer>().material.SetColor("_Color", Color.red);
        }
    }
}
