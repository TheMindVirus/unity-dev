using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Unity.LEGO.Minifig;

public class Ghost : MonoBehaviour
{
    public GameObject Player = null;

    private float ViewX = 0.0f;
    private float ViewY = 0.0f;
    private float DirectionX = 0.0f;
    private float DirectionY = 0.0f;
    private bool KeyJump = false;

    public void SetViewX(float vx) { ViewX += vx; }
    public void SetViewY(float vy) { ViewY += vy; }
    public void SetDirectionX(float dx) { DirectionX = dx; }
    public void SetDirectionY(float dy) { DirectionY = dy; }
    public void SetKeyJump(float cz) { KeyJump = (cz > 0.0f); }

    void Update()
    {
        transform.parent.localPosition = Player.transform.localPosition;
        transform.parent.localRotation = Quaternion.Euler(transform.localRotation.x - ViewY,
                                                          transform.localRotation.y + ViewX,
                                                          transform.localRotation.z);
        Player.GetComponents<MinifigController>()[0].SetHorizontal(DirectionX);
        Player.GetComponents<MinifigController>()[0].SetVertical(-DirectionY);
        Player.GetComponents<MinifigController>()[0].SetOrbital((KeyJump) ? 1.0f : 0.0f);
    }
}
