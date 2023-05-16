using UnityEngine;

public class RandomControl : MonoBehaviour
{
    public AudioSource sound = null;

    void OnTriggerEnter()
    {
        Debug.Log(Random.Range(0.0f, 100.0f));
        transform.position = new Vector3(Random.Range(150.0f, 250.0f), 1.5f, Random.Range(-25.0f, -69.0f));
        if (sound != null) { sound.Play(); }
    }
}
