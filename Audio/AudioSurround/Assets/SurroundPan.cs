using UnityEngine;

public class SurroundPan : MonoBehaviour
{
    public Vector2 Pan;

    public Vector2 Forward;
    public Vector2 Middle;
    public Vector2 Backward;
    public Vector2 Lateral;

    public AudioSource FrontLeft;
    public AudioSource FrontRight;
    public AudioSource Center;
    public AudioSource Subwoofer;
    public AudioSource RearLeft;
    public AudioSource RearRight;
    public AudioSource SideLeft;
    public AudioSource SideRight;

    private int I = 0; //1; //Include Middle in Forward and Backward
    private int J = 1; //0; //Mystery Parameter for Panning Crossover
    private AudioListener Listener;
    private AudioLowPassFilter SurroundFX;

    void Start()
    {
        FrontLeft = GameObject.Find("Front Left").GetComponent<AudioSource>();
        FrontRight = GameObject.Find("Front Right").GetComponent<AudioSource>();
        Center = GameObject.Find("Center").GetComponent<AudioSource>();
        Subwoofer = GameObject.Find("Subwoofer").GetComponent<AudioSource>();
        RearLeft = GameObject.Find("Rear Left").GetComponent<AudioSource>();
        RearRight = GameObject.Find("Rear Right").GetComponent<AudioSource>();
        SideLeft = GameObject.Find("Side Left").GetComponent<AudioSource>();
        SideRight = GameObject.Find("Side Right").GetComponent<AudioSource>();
        Listener = GameObject.Find("Main Camera").GetComponent<AudioListener>();
        SurroundFX = GameObject.Find("Main Camera").GetComponent<AudioLowPassFilter>();
    }

    void Refresh()
    {
        FrontLeft.volume  = Mathf.Min(Mathf.Max((0 - (Pan.x * 2)) * (J + (Pan.y + I)),      0), 1);
        FrontRight.volume = Mathf.Min(Mathf.Max((0 + (Pan.x * 2)) * (J + (Pan.y + I)),      0), 1);
        Center.volume     = Mathf.Min(Mathf.Max((1 - Mathf.Abs(Pan.x)) * (0 + (Pan.y + 1)), 0), 1);
        Subwoofer.volume  = Mathf.Min(Mathf.Max((1 - Mathf.Abs(Pan.x)) * (2 - (Pan.y + 1)), 0), 1);
        RearLeft.volume   = Mathf.Min(Mathf.Max((0 - (Pan.x * 2)) * (J - (Pan.y + I)),      0), 1);
        RearRight.volume  = Mathf.Min(Mathf.Max((0 + (Pan.x * 2)) * (J - (Pan.y + I)),      0), 1);
        SideLeft.volume   = Mathf.Min(Mathf.Max((0 - (Pan.x * 2)) * (1 - Mathf.Abs(Pan.y)), 0), 1);
        SideRight.volume  = Mathf.Min(Mathf.Max((0 + (Pan.x * 2)) * (1 - Mathf.Abs(Pan.y)), 0), 1);
        Forward.x  =  FrontLeft.volume;
        Forward.y  = FrontRight.volume;
        Middle.x   =     Center.volume;
        Middle.y   =  Subwoofer.volume;
        Backward.x =   RearLeft.volume;
        Backward.y =  RearRight.volume;
        Lateral.x  =   SideLeft.volume;
        Lateral.y  =  SideRight.volume;
        SurroundFX.cutoffFrequency = 1000 + ((1 + Pan.y) * 10000);
    }

    void Update() { Refresh(); }
}
