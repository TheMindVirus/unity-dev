using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DrumControl : MonoBehaviour
{
    public AudioSource AudioSourceC;

    private RaycastHit hit;
    private Ray ray;
    private bool toggle;
    private bool locked;
    private bool hovering;
    private bool selected;
    private Vector3 origin;
    private UnityEngine.UI.Text HUD;

    void Start()
    {
        hit = new RaycastHit();
        ray = new Ray();
        toggle = true;
        locked = false;
        origin = transform.position;
        HUD = GameObject.Find("/Player/HUD/Text").GetComponent<UnityEngine.UI.Text>();
    }

    void Update()
    {
        ray = Camera.main.ViewportPointToRay(new Vector3(0.5f, 0.5f, 0.0f));
        if (Physics.Raycast(ray, out hit))
        {
            if (hit.collider.transform.gameObject == transform.gameObject) { hovering = true; }
            else { hovering = false; }
        }
        if ((hovering) && (Input.GetMouseButton(0))) { selected = true; }
        else if (!Input.GetMouseButton(0)) { selected = false; }
        if (selected && !locked)
        {
            //SET_TRACK_VOLUMES//
            toggle = !toggle;
            locked = true;
            AudioSourceC.volume = (toggle) ? 1.0f : 0.0f;
            /////////////////////
        }
        else if (!selected) { locked = false; }
    }
}
