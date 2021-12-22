using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Video;

public class BunkerScreen3 : MonoBehaviour
{
    public string filename = "YodaFullScreen.mp4";
    public AudioSource output = null;
    public List<VideoPlayer> Screens = new List<VideoPlayer>();
    private int SyncTarget = 0;
    
    void Start()
    {
        var filename = "YodaFullScreen.mp4";
        var path = Application.streamingAssetsPath + "/" + filename;

        Screen.sleepTimeout = SleepTimeout.NeverSleep;

        for (int i = 0; i < Screens.Count; ++i)
        {
            if (i == 0)
            {
                Screens[i].audioOutputMode = VideoAudioOutputMode.AudioSource;
                Screens[i].SetTargetAudioSource(0, output);
            }
            else
            {
                Screens[i].audioOutputMode = VideoAudioOutputMode.None;
                Screens[i].SetDirectAudioVolume(0, 0);
            }
        }

        //for (int i = 1; i < Screens.Count; ++i) { Screens[i].timeReference = VideoTimeReference.ExternalTime; }
        foreach (VideoPlayer screen in Screens) { screen.url = path; }
        //foreach (VideoPlayer screen in Screens) { screen.Prepare(); while (!screen.isPrepared) { } }
        foreach (VideoPlayer screen in Screens) { screen.Play(); }

        Invoke("Interval", 1.0f);
    }

    void Interval()
    {
        //for (int i = 1; i < Screens.Count; ++i) { Screens[i].time = Screens[0].time; }
        SyncTarget += 1;
        if (SyncTarget >= Screens.Count) { SyncTarget = 1; }
        Debug.Log("[SYNC]: " + SyncTarget.ToString());
        Screens[SyncTarget].time = Screens[0].time;
        //Screens[SyncTarget].externalReferenceTime = Screens[0].time;
        //Screens[SyncTarget].externalReferenceTime = Screens[0].clockTime;
        Invoke("Interval", 1.0f);
    }
}
