#define TEST
//#define LEAN

using System;
using UnityEngine;
#if TEST
using System.IO;
using System.Text;
#endif

public class loader : MonoBehaviour
{
    [Serializable]
    public class jsonwrap { public byte[] data; }
    public jsonwrap wrap(byte[] raw) { jsonwrap wrapper = new jsonwrap(); wrapper.data = raw; return wrapper; }

    public void load(string json)
    {
        AssetBundle bundle = AssetBundle.LoadFromMemory(JsonUtility.FromJson<jsonwrap>(json).data);
        if (bundle == null) { Debug.Log("AssetBundleReadErr"); return; }
        var assets = bundle.LoadAllAssets<GameObject>();
        if (assets == null) { Debug.Log("AssetBundleLoadErr"); bundle.Unload(true); return; }
        foreach (GameObject asset in assets)
        {
            GameObject prefab = GameObject.Instantiate(asset);
            prefab.name = asset.name;
        }
#if LEAN
        bundle.Unload(false);
#endif
    }
#if TEST
    void Start()
    {
        var src = new FileStream("Assets/bundles/1000truths.unity3d", FileMode.Open, FileAccess.Read);
        byte[] raw = new byte[src.Length];
        int n = src.Read(raw, 0, (int)src.Length);
        Debug.Log("srclen: " + src.Length.ToString() + " | ipolen: " + n.ToString() + " | dstlen: " + raw.Length.ToString());
        string json = JsonUtility.ToJson(wrap(raw));

        var dst = new FileStream("Assets/loader/sample.json", FileMode.Create, FileAccess.Write);
        dst.Write(Encoding.UTF8.GetBytes(json), 0, json.Length);
        dst.Close();

        byte[] memory = JsonUtility.FromJson<jsonwrap>(json).data;
        Debug.Log("strlen: " + json.Length.ToString() + " | memlen: " + memory.Length.ToString());
        for (int i = 0; i < memory.Length; ++i)
        {
            if (raw[i] != memory[i]) { Debug.Log("ERROR: Byte " + i.ToString()); }
        }
        src.Close();
        load(json);
    }
#endif
}
