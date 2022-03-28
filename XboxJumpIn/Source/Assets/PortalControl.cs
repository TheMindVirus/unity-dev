using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using UnityEngine;

public class PortalControl : MonoBehaviour
{
    public string zone = "zone";

    [DllImport("__Internal")]
    private static extern void TriggerZone(string zone);

    void OnTriggerEnter()
    {
        Debug.Log("Player Entered " + zone + "!");
        TriggerZone(zone);
    }
}
