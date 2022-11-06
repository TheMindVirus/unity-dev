using UnityEngine;

public class CutsceneControl : MonoBehaviour
{
    public AudioSource audio1 = null;
    public GameObject camera1 = null;
    public GameObject camera2 = null;
    public GameObject camera3 = null;
    public GameObject camera4 = null;
    public GameObject chicken = null;
    public GameObject glass = null;
    Vector3 mouse = new Vector3(0.0f, 0.0f, 0.0f);
    Vector3 drift = new Vector3(0.0f, 0.0f, 0.0f);
    Vector3 shake = new Vector3(0.0f, 0.0f, 0.0f);
    int state = 0;
    float speed = 0.03f; //0.01f; //much slower in build than in player

    void Update()
    {
        if ((state == 0)  && (audio1.time <=  11.0f)) { state = 1;  camera1.transform.localPosition = new Vector3(0.5449762f, 0.2578068f, 0.7255772f); } //state = 9; audio1.time = 230.0f; }
        if ((state == 1)  && (audio1.time <=  11.0f)) { state = 1;  camera1.transform.Translate(0.0f, 0.0f, speed, Space.World); }
        if ((state == 1)  && (audio1.time >   11.0f)) { state = 2;  camera1.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = true; }
        if ((state == 2)  && (audio1.time >   44.0f)) { state = 3;  camera1.transform.localPosition = new Vector3(0.5449762f, 0.2578068f, 0.7255772f); camera2.GetComponent<Camera>().enabled = false; camera1.GetComponent<Camera>().enabled = false; camera1.GetComponent<Camera>().enabled = true; }
        if ((state == 3)  && (audio1.time <=  77.0f)) { state = 3;  camera1.transform.Translate(0.0f, 0.0f, speed, Space.World); }
        if ((state == 3)  && (audio1.time >   77.0f)) { state = 4;  camera1.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = true; }
        if ((state == 4)  && (audio1.time >   99.0f)) { state = 5;  camera1.transform.localPosition = new Vector3(0.5449762f, 0.2578068f, 0.7255772f); camera2.GetComponent<Camera>().enabled = false; camera1.GetComponent<Camera>().enabled = false; camera1.GetComponent<Camera>().enabled = true; }
        if ((state == 5)  && (audio1.time <= 121.0f)) { state = 5;  camera1.transform.Translate(0.0f, 0.0f, speed, Space.World); }
        if ((state == 5)  && (audio1.time >  121.0f)) { state = 6;  camera1.GetComponent<Camera>().enabled = false; camera3.GetComponent<Camera>().enabled = false; camera3.GetComponent<Camera>().enabled = true; }
        if ((state == 6)  && (audio1.time >  165.0f)) { state = 7;  camera3.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = true; }
        if ((state == 7)  && (audio1.time >  187.0f)) { state = 8;  camera1.transform.localPosition = new Vector3(0.5449762f, 0.2578068f, 0.7255772f); camera3.GetComponent<Camera>().enabled = false; camera1.GetComponent<Camera>().enabled = false; camera1.GetComponent<Camera>().enabled = true; }
        if ((state == 8)  && (audio1.time <= 207.0f)) { state = 8;  camera1.transform.Translate(0.0f, 0.0f, speed, Space.World); }
        if ((state == 8)  && (audio1.time >  207.0f)) { state = 9;  camera1.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = false; camera2.GetComponent<Camera>().enabled = true; }
        if ((state == 9)  && (audio1.time >  218.0f)) { state = 10; camera2.GetComponent<Camera>().enabled = false; camera3.GetComponent<Camera>().enabled = false; camera3.GetComponent<Camera>().enabled = true; }
        if ((state == 10) && (audio1.time >  234.0f)) { state = 11; camera3.GetComponent<Camera>().enabled = false; camera4.GetComponent<Camera>().enabled = false; camera4.GetComponent<Camera>().enabled = true; chicken.transform.localPosition = new Vector3(0.0f, 0.0f, 0.0f); }
        if ((state == 11) && (audio1.time >  239.0f)) { state = 11; if (chicken.transform.localPosition.y < 1.9f) { chicken.transform.localPosition = new Vector3(0.0f, chicken.transform.localPosition.y + speed, 0.0f); } else { glass.GetComponent<Renderer>().enabled = true; } }

        if ((state == 6) || (state == 10))
        {
            mouse = new Vector3(Input.GetAxis("Mouse Y"), Input.GetAxis("Mouse X"), 0.0f);
            drift = new Vector3(drift.x + mouse.x, drift.y + mouse.y, drift.z);
            shake = new Vector3(Random.Range(0.0f, 1.0f), Random.Range(0.0f, 1.0f), Random.Range(0.0f, 1.0f));
            camera3.transform.parent.localRotation = Quaternion.Euler(drift + shake);
        }
    }
}