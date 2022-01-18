using System.IO;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class AudioControl : MonoBehaviour
{
    public AudioSource AudioSourceA;
    public AudioSource AudioSourceB;
    public AudioSource AudioSourceC;
    public string TrackA;
    public string TrackB;
    public string TrackC;

    void Start()
    {
        StartCoroutine(GetAudioClip(AudioSourceA, TrackA, AudioType.MPEG));
        StartCoroutine(GetAudioClip(AudioSourceB, TrackB, AudioType.MPEG));
        StartCoroutine(GetAudioClip(AudioSourceC, TrackC, AudioType.MPEG));
    }

    IEnumerator GetAudioClip(AudioSource deck, string track, AudioType type)
    {
        string url = Path.Combine(Application.streamingAssetsPath, track);
        Debug.Log("Loading " + url);
        using (UnityWebRequest www = UnityWebRequestMultimedia.GetAudioClip(url, type))
        {
            yield return www.SendWebRequest();
            if (www.result == UnityWebRequest.Result.ConnectionError) { Debug.Log(www.error); }
            else { deck.clip = DownloadHandlerAudioClip.GetContent(www); deck.Play(); }
        }
    }
}
