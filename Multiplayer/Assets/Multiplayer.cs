using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Multiplayer : MonoBehaviour
{
    public GameObject template;

    void Start()
    {
        /*
        string ID = "[TEST]";
        SpawnPlayer(ID);
        GameObject player = GameObject.Find(ID);
        string JSON = "{\"alias\":\"" + ID + "\",\"position\":{\"x\":0.0,\"y\":0.0,\"z\":0.0},\"rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0}}";
        player.GetComponent<Player>().SetData(JSON);

        ID = "[TEST2]";
        SpawnPlayer(ID);
        player = GameObject.Find(ID);
        JSON = "{\"alias\":\"" + ID + "\",\"position\":{\"x\":0.0,\"y\":0.0,\"z\":0.0},\"rotation\":{\"x\":0.0,\"y\":0.0,\"z\":0.0}}";
        player.GetComponent<Player>().SetData(JSON);

        DespawnPlayer("[TEST]");
        */
    }

    public void SpawnPlayer(string ID)
    {
        if (GameObject.Find(ID) != null) { return; }
        GameObject player = GameObject.Instantiate(template);
        player.name = ID;
        player.SetActive(true);
    }

    public void DespawnPlayer(string ID)
    {
        GameObject player = GameObject.Find(ID);
        if ((player != null) && (player.GetComponent<Player>() != null)) { GameObject.Destroy(player); }
    }

    public void ListGameObjects()
    {
        List<GameObject> objects = new List<GameObject>();
        foreach (GameObject obj in Resources.FindObjectsOfTypeAll(typeof(GameObject)) as GameObject[])
        {
            Debug.Log(obj.name);
        }
    }
}