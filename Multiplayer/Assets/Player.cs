using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class PlayerData
{
    public string alias = "<PlayerName>";
    public Vector3 position = new Vector3(0.0f, 0.0f, 0.0f);
    public Vector3 rotation = new Vector3(0.0f, 0.0f, 0.0f);
}

public class Player : MonoBehaviour
{
    private PlayerData data = new PlayerData();
    private Rect label = new Rect(0.0f, 0.0f, 100.0f, 30.0f);
    private Vector3 point = new Vector3(0.0f, 0.0f, 0.0f);
    private Vector3 offset = new Vector3(0.0f, 0.1f, 0.0f);

    void OnGUI()
    {
        point = Camera.main.WorldToScreenPoint(transform.position + offset);
        label.x = point.x - (label.width / 2.0f);
        label.y = Screen.height - point.y - label.height;
        var style = GUI.skin.GetStyle("Label");
        style.alignment = TextAnchor.UpperCenter;
        if (point.z > 0.0f) { GUI.Label(label, data.alias, style); }
    }

    public string GetData() { return JsonUtility.ToJson(data); }
    public void SetData(string JSON)
    {
        //JsonUtility.FromJsonOverwrite(JSON, this);
        data = JsonUtility.FromJson<PlayerData>(JSON);
        transform.position = data.position;
        transform.eulerAngles = data.rotation;
    }
}
