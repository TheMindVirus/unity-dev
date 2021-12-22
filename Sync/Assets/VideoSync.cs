using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Video;

public class VideoSync : MonoBehaviour
{
    VideoPlayer videoPlayer = null;
    public VideoPlayer masterVideoPlayer = null;

    void Start()
    {
        videoPlayer = this.GetComponent<VideoPlayer>();
        //videoPlayer.timeSource.Freerun = false;
        //videoPlayer.timeReference = VideoTimeReference.ExternalTime;
        //videoPlayer.timeSource = VideoTimeSource.AudioDSPTimeSource;
        //videoPlayer.timeSource = VideoTimeSource.GameTimeSource;
        videoPlayer.Play();
    }

    void Update()
    {
        //videoPlayer.externalReferenceTime = <external clock>;
        //videoPlayer.time = masterVideoPlayer.time;
    }
}
