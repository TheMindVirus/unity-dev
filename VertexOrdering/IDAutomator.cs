using UnityEngine;
using System.Collections;
using System.Collections.Generic;

public class IDAutomator : MonoBehaviour
{
    private float _delta = 0;
    private int _id = 0;

    void Update()
    {
        _delta += Time.deltaTime;
        if (_delta > 0.2)
        {
            _id += 1;
            if (_id >= 24) { _id = 0; }
            Debug.Log("TICK");
            GetComponent<Renderer>().sharedMaterial.SetFloat("_ID", _id);
            _delta = 0;
        }
    }
}
