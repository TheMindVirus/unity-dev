using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Example : MonoBehaviour
{
    public CharacterController controller;
    public Vector3 playerVelocity;
    public bool groundedPlayer;
    public float playerSpeed = 2.0f;
    public float jumpHeight = 1.0f;
    public float gravityValue = -9.81f;

    public Transform player;
    public Transform ground;
    public Vector3 gravity;

    private void Start()
    {
        //controller = gameObject.AddComponent<CharacterController>();
        controller = this.gameObject.GetComponent<CharacterController>();
        player = this.transform;
    }

    void Update()
    {
        player = this.transform;
        groundedPlayer = controller.isGrounded;
        if (groundedPlayer && playerVelocity.y < 0)
        {
            playerVelocity.x = 0f;
            playerVelocity.y = 0f;
            playerVelocity.z = 0f;
        }
        else if (!groundedPlayer)
        {
            //playerVelocity.x = 0f;
            //playerVelocity.y = 0f;
            //playerVelocity.z = 0f;
        }

        // Horizontal input
        //Vector3 move = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
        Vector3 move = new Vector3((Input.GetKey("d") ? 1 : 0) - (Input.GetKey("a") ? 1 : 0), 0, (Input.GetKey("w") ? 1 : 0) - (Input.GetKey("s") ? 1 : 0));
        move = Vector3.ClampMagnitude(move, 1f); // Optional: prevents faster diagonal movement

        if (move != Vector3.zero)
        {
            //transform.forward = move;
        }

        // Jump
        //if (Input.GetButtonDown("Jump") && groundedPlayer)
        if (Input.GetKey("space") && groundedPlayer)
        {
            playerVelocity.y = Mathf.Sqrt(jumpHeight * -2.0f * gravityValue);
        }

        // Apply gravity
        //playerVelocity.y += gravityValue * Time.deltaTime;
        if (ground)
        {
            //gravity = (ground.position - player.position) * Time.deltaTime;
            gravity = Vector3.ClampMagnitude(ground.position - player.position, gravityValue) * Time.deltaTime;
            playerVelocity += gravity;
        }
        else if (!ground && !groundedPlayer)
        {
            playerVelocity.y += gravityValue * Time.deltaTime;
        }

        // Combine horizontal and vertical movement
        //Vector3 finalMove = (move * playerSpeed) + (playerVelocity.y * Vector3.up);
        Vector3 finalMove = (move * playerSpeed) + (playerVelocity.y * player.up);
        controller.Move(finalMove * Time.deltaTime);

        // LookAt ground
        //var player = this.transform;
        //var ground = controller.ground;
        //if (ground)
        if (groundedPlayer && ground)
        {
            player.LookAt(ground);
            player.Rotate(new Vector3(-90f, 0f, 0f));
        }
    }

    void OnControllerColliderHit(ControllerColliderHit hit)
    {
        ground = hit.gameObject.transform;
    }

    void OnCollisionEnter(Collision hit)
    {
        //ground = hit.gameObject.transform;
        //player = this.transform;
        //player.LookAt(ground);
        //player.Rotate(new Vector3(-90f, 0f, 0f));
    }
}
