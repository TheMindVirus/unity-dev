using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GhostDebug : MonoBehaviour
{
    void Update()
    {
        SendMessage("SetViewX", Input.GetAxis("Mouse X") * 5.0f);
        SendMessage("SetViewY", Input.GetAxis("Mouse Y") * 5.0f);

        Vector3 direction = new Vector3(0, 0, 0);
        if (Input.GetKey(KeyCode.W)) { direction += new Vector3( 0, -1,  0); }
        if (Input.GetKey(KeyCode.S)) { direction += new Vector3( 0,  1,  0); }
        if (Input.GetKey(KeyCode.A)) { direction += new Vector3(-1,  0,  0); }
        if (Input.GetKey(KeyCode.D)) { direction += new Vector3( 1,  0,  0); }

        SendMessage("SetDirectionX", direction.x * 1.0f);
        SendMessage("SetDirectionY", direction.y * 0.1f);

        SendMessage("SetKeyJump", Input.GetKey(KeyCode.Space) ? 1.0f : 0.0f);
    }
}
