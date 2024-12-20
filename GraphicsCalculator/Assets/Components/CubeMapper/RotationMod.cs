using UnityEngine;

public class RotationMod : MonoBehaviour
{
    public Vector3 Rotation = new Vector3();
    public Vector3 Rotors_X = new Vector3();
    public Vector3 Rotors_Y = new Vector3();
    public Vector3 Rotors_Z = new Vector3();
    public Vector3 DirectionA = new Vector3();
    public Vector3 DirectionB = new Vector3();
    public Vector3 RotationA = new Vector3();
    public Vector3 RotationB = new Vector3();
    public Vector3 DebugReadout = new Vector3();
    public Quaternion DebugQuaternion = new Quaternion();

           bool UseANotB = false;
    public bool UseBNotA = false;
    public bool UseAngle = false;
    public bool UseHypot = false;
    public bool UseFixed = false;
    private bool UsePrev = false;
    private bool UseLock = false;

    Vector3 tmp = new Vector3();
    Vector3 rotation = new Vector3();
    //float multiplier = Mathf.Atan(Mathf.Sqrt(2.0f)) / Mathf.Atan(1);
    //multiplied by cubic sine of vector swapped angle at runtime specification
    Vector3 default_scale = new Vector3(360.0f, 360.0f, 360.0f);

    void Update() { Refresh(); }
    void Refresh() { Rotation.x += 0.001f; Rotation.x %= 1; OnValidate(); }

    void OnValidate()
    {
        transform.rotation = DebugQuaternion;
        rotation = VectorPhase(Rotation);
        tmp = new Vector3(transform.rotation.eulerAngles.x + rotation.x,
                          transform.rotation.eulerAngles.y + rotation.y,
                          transform.rotation.eulerAngles.z + rotation.z);
        if (UseAngle) { transform.rotation = Quaternion.Euler(tmp); }
    }

    //float Mathf_Tri(float x, float m) { return Mathf.PingPong(x, m); }
    //float Mathf_Tri(float x, float m) { return m - Mathf.Abs(Mathf.Repeat(x, (m * 2.0f)) - m); }

    Vector3 RotorMod(float phase)
    {
        Vector3 rotors = new Vector3();
        phase = Mathf.Repeat(phase, 1.0f) * 8.0f;
        rotors.z = (int)phase;
        rotors.y = Mathf.RoundToInt((rotors.z + 0.5f) / 2);
        rotors.x = Mathf.RoundToInt((rotors.z + 0.5f) / 2);
        rotors.y = rotors.y * ((rotors.z + 1) % 2);
        rotors.x = rotors.x * ((rotors.z + 0) % 2);
        return rotors;
    }

    float SinMod(float phase, float shift = Mathf.PI / 2.0f)
    {
        phase = Mathf.Repeat(phase, 1.0f);
        float i = phase * Mathf.PI * 2.0f;
        if (phase < 1.0f / 8.0f) { return  Mathf.Tan(i); }
        if (phase < 2.0f / 8.0f) { return  1.0f; }
        if (phase < 3.0f / 8.0f) { return  1.0f; }
        if (phase < 4.0f / 8.0f) { return  Mathf.Tan((2.0f * shift) - i); }
        if (phase < 5.0f / 8.0f) { return -Mathf.Tan(i - (2.0f * shift)); }
        if (phase < 6.0f / 8.0f) { return -1.0f; }
        if (phase < 7.0f / 8.0f) { return -1.0f; }
        if (phase < 8.0f / 8.0f) { return -Mathf.Tan((4.0f * shift) - i); }
        return 0.0f;
    }

    float CosMod(float phase, float shift = Mathf.PI / 2.0f)
    {
        phase = Mathf.Repeat(phase, 1.0f);
        float i = phase * Mathf.PI * 2.0f;
        if (phase < 1.0f / 8.0f) { return 1.0f; }
        if (phase < 2.0f / 8.0f) { return Mathf.Tan(shift - i); }
        if (phase < 3.0f / 8.0f) { return -Mathf.Tan(i - shift); }
        if (phase < 4.0f / 8.0f) { return -1.0f; }
        if (phase < 5.0f / 8.0f) { return -1.0f; }
        if (phase < 6.0f / 8.0f) { return -Mathf.Tan((3.0f * shift) - i); }
        if (phase < 7.0f / 8.0f) { return Mathf.Tan(i - (3.0f * shift)); }
        if (phase < 8.0f / 8.0f) { return 1.0f; }
        return 0.0f;
    }

    float HypMod(float phase, float shift = Mathf.PI / 2.0f)
    {
        phase = Mathf.Repeat(phase, 1.0f);
        float i = phase * Mathf.PI * 2.0f;
        if (phase < 1.0f / 8.0f) { return  1.0f - (1.0f / Mathf.Cos(i - (0.0f * shift))); }
        if (phase < 2.0f / 8.0f) { return  1.0f - (1.0f / Mathf.Cos((1.0f * shift) - i)); }
        if (phase < 3.0f / 8.0f) { return -1.0f + (1.0f / Mathf.Cos(i - (1.0f * shift))); }
        if (phase < 4.0f / 8.0f) { return -1.0f + (1.0f / Mathf.Cos((2.0f * shift) - i)); }
        if (phase < 5.0f / 8.0f) { return  1.0f - (1.0f / Mathf.Cos(i - (2.0f * shift))); }
        if (phase < 6.0f / 8.0f) { return  1.0f - (1.0f / Mathf.Cos((3.0f * shift) - i)); }
        if (phase < 7.0f / 8.0f) { return -1.0f + (1.0f / Mathf.Cos(i - (3.0f * shift))); }
        if (phase < 8.0f / 8.0f) { return -1.0f + (1.0f / Mathf.Cos((4.0f * shift) - i)); }
        return 0.0f;
    }

    Vector3 Rotate(Vector3 c, Vector3 r)
    {
        Vector3 n = new Vector3();

        Vector3 mx = new Vector3();
        Vector3 my = new Vector3();
        Vector3 mz = new Vector3();

        mx.x = Mathf.Cos(r.x) * Mathf.Cos(r.z);
        mx.y = (-Mathf.Cos(r.y) * Mathf.Sin(r.z)) + (Mathf.Sin(r.y) * Mathf.Sin(r.x) * Mathf.Cos(r.z));
        mx.z = (Mathf.Sin(r.y) * Mathf.Sin(r.z)) + (Mathf.Cos(r.y) * Mathf.Sin(r.x) * Mathf.Cos(r.z));

        my.x = Mathf.Cos(r.x) * Mathf.Sin(r.z);
        my.y = (Mathf.Cos(r.y) * Mathf.Cos(r.z)) + (Mathf.Sin(r.y) * Mathf.Sin(r.x) * Mathf.Sin(r.z));
        my.z = (-Mathf.Sin(r.y) * Mathf.Cos(r.z)) + (Mathf.Cos(r.y) * Mathf.Sin(r.x) * Mathf.Sin(r.z));

        mz.x = -Mathf.Sin(r.x);
        mz.y = Mathf.Sin(r.y) * Mathf.Cos(r.x);
        mz.z = Mathf.Cos(r.y) * Mathf.Cos(r.x);

        n.x = (mx.x * c.x) + (mx.y * c.y) + (mx.z * c.z);
        n.y = (my.x * c.x) + (my.y * c.y) + (my.z * c.z);
        n.z = (mz.x * c.x) + (mz.y * c.y) + (mz.z * c.z);
    
        return n;
    }

    Vector3 RotateMod(Vector3 c, Vector3 r)
    {
        Vector3 n = new Vector3();

        Vector3 mx = new Vector3();
        Vector3 my = new Vector3();
        Vector3 mz = new Vector3();

        mx.x = CosMod(r.x) * CosMod(r.z);
        mx.y = (-CosMod(r.y) * SinMod(r.z)) + (SinMod(r.y) * SinMod(r.x) * CosMod(r.z));
        mx.z = (SinMod(r.y) * SinMod(r.z)) + (CosMod(r.y) * SinMod(r.x) * CosMod(r.z));

        my.x = CosMod(r.x) * SinMod(r.z);
        my.y = (CosMod(r.y) * CosMod(r.z)) + (SinMod(r.y) * SinMod(r.x) * SinMod(r.z));
        my.z = (-SinMod(r.y) * CosMod(r.z)) + (CosMod(r.y) * SinMod(r.x) * SinMod(r.z));

        mz.x = -SinMod(r.x);
        mz.y = SinMod(r.y) * CosMod(r.x);
        mz.z = CosMod(r.y) * CosMod(r.x);

        n.x = (mx.x * c.x) + (mx.y * c.y) + (mx.z * c.z);
        n.y = (my.x * c.x) + (my.y * c.y) + (my.z * c.z);
        n.z = (mz.x * c.x) + (mz.y * c.y) + (mz.z * c.z);

        return n;
    }

    float Radius(Vector3 direction)
    {
        return Mathf.Sqrt(Mathf.Sqrt(Mathf.Pow(direction.x, 2.0f)
                                   + Mathf.Pow(direction.y, 2.0f))
                                   + Mathf.Pow(direction.z, 2.0f));
    }

    float RadiusMod(Vector3 direction)
    {
        return Mathf.Sqrt(Mathf.Sqrt(Mathf.Pow(direction.x, 2.0f)
                                   + Mathf.Pow(direction.y, 2.0f))
                                   + Mathf.Pow(direction.z, 2.0f));
    }

    float InteriorAngle(float x, float y, float z)
    {
        float angle = (Mathf.Atan(x / y) / Mathf.PI) * 180.0f;
        //if (z < 0) { angle = -angle; }
        if ((x >= 0) && (y >= 0)) { angle = angle + ((z >= 0.0f) ?   0.0f :   0.0f); }
        if ((x >= 0) && (y <  0)) { angle = angle + ((z >= 0.0f) ? 180.0f : 180.0f); }
        if ((x <  0) && (y <  0)) { angle = angle + ((z >= 0.0f) ? 180.0f : 180.0f); }
        if ((x <  0) && (y >= 0)) { angle = angle + ((z >= 0.0f) ? 360.0f : 360.0f); }
        if (angle.ToString() == float.NaN.ToString()) { angle = 0.0f; }
        if (angle == 360.0f) { angle = 0.0f; }
        DebugReadout.x = x;
        DebugReadout.y = y;
        DebugReadout.z = angle;
        return angle;
    }

    Vector3 InteriorAngles(Vector3 c) //!!! might be buggy
    {
        Vector3 n = new Vector3();
        n.x = InteriorAngle( c.z,  c.y, -c.x);
        n.y = InteriorAngle( c.z, -c.x,  c.y);
        n.z = InteriorAngle(-c.x,  c.y,  c.z);
        return n;
    }

    float InteriorAngleMod(float x, float y, float z)
    {
        float angle = (Mathf.Atan(x / y) / Mathf.PI) * 180.0f;
        //if (z < 0) { angle = -angle; }
        if ((x >= 0) && (y >= 0)) { angle = angle + ((z >= 0.0f) ?   0.0f :   0.0f); }
        if ((x >= 0) && (y <  0)) { angle = angle + ((z >= 0.0f) ? 180.0f : 180.0f); }
        if ((x <  0) && (y <  0)) { angle = angle + ((z >= 0.0f) ? 180.0f : 180.0f); }
        if ((x <  0) && (y >= 0)) { angle = angle + ((z >= 0.0f) ? 360.0f : 360.0f); }
        if (angle.ToString() == float.NaN.ToString()) { angle = 0.0f; }
        if (angle == 360.0f) { angle = 0.0f; }
        DebugReadout.x = x;
        DebugReadout.y = y;
        DebugReadout.z = angle;
        return angle;
    }

    Vector3 InteriorAnglesMod(Vector3 c) //!!! might also be buggy
    {
        Vector3 n = new Vector3();
        n.x = InteriorAngleMod( c.z,  c.y, -c.x);
        n.y = 0.0f; //InteriorAngleMod( c.z, -c.x,  c.y);
        n.z = InteriorAngleMod(-c.x,  c.y,  c.z);
        return n;
    }

    Vector3 VectorPhase(Vector3 angle) //, Vector3 scale, Vector3 order)
    {
        Vector3 scaled = new Vector3(angle.x, angle.y, angle.z);
        //angle.xyz *= default_scale.xyz;

        scaled.x = Mathf.Repeat(scaled.x * default_scale.x, default_scale.x);
        scaled.y = Mathf.Repeat(scaled.y * default_scale.y, default_scale.y);
        scaled.z = Mathf.Repeat(scaled.z * default_scale.z, default_scale.z);

        //Debug.Log(Mathf.Sqrt(2.0f));
        //Debug.Log(multiplier);

        //incorrect value generated from temporary cache of the same variable: 1.414214 vs. 1.216347
        //the first one is correct for root 2, the second one is correct for temporary scaling

        //float rotor_z = Mathf.Abs(Mathf.Sin((2.0f * angle.y * Mathf.PI * 2.0f)));
        //float rotor_z = Mathf.Pow(Mathf.Abs(Mathf.Sin((2.0f * angle.y * Mathf.PI * 2.0f))), 10);

        //float A = 1; //opp - opposite varies between axial directions once rotated
        //float B = 1; //adj - adjacent is pretty much always 1 for a virtual radius

        //float shift = Mathf.PI / 2.0f;
        //float shift_a = shift * Rotors.x;
        //float shift_b = shift * Rotors.y;
        //float scale = angle.y * Mathf.PI * 2.0f;

        //opp follows a triangle wave
        //Rotors_Y.z = 1.0f - Mathf.Abs(1.0f / Mathf.Cos(shift_a - scale - shift_b));
        //A = Rotors_Y.z;

        //float multiplier = Mathf.Atan(Mathf.Sqrt(2.0f) / 1) / Mathf.Atan(1 / 1);
        //float multiplier = Mathf.Atan(Mathf.Sqrt(2.0f) / 1) / Mathf.Atan(A / B);
       
        //scaled.x = scaled.x * (1 + ((multiplier - 1) * Rotors.z));
        //scaled.x = scaled.x * Rotors.z;
        //scaled.y = scaled.y;
        //scaled.z = scaled.z;

        DirectionA = Rotate(Vector3.up, angle * Mathf.PI * 2.0f);
        RotationA = InteriorAngles(DirectionA);
        DirectionB = RotateMod(Vector3.up, angle);
        RotationB = InteriorAnglesMod(DirectionB);
        
        Rotors_X = RotorMod(angle.x); 
        Rotors_Y = RotorMod(angle.y);
        Rotors_Z = RotorMod(angle.z);

        if (!UseBNotA)
        {
            scaled.x = RotationA.x;
            scaled.y = RotationA.y;
            scaled.z = RotationA.z;
            UseANotB = true;
        }

        if (UseBNotA)
        {
            scaled.x = RotationB.x;
            scaled.y = RotationB.y;
            scaled.z = RotationB.z;
            UseANotB = false;
        }

        float hyp = 1.0f;
        if (!UseBNotA) { hyp = Radius(DirectionA); }
        if (UseBNotA) { hyp = RadiusMod(DirectionB); UseLock = false; }
        if ((!UseBNotA) && (!UseANotB) && (!UseLock)) { UseANotB = true; UseLock = true; }

        var Line = GetComponent<LineRenderer>();
        if (Line != null)
        {
            if ((!UseAngle) && (!UseBNotA)) { Line.SetPosition(1, DirectionA); }
            if ((!UseAngle) && (UseBNotA)) { Line.SetPosition(1, DirectionB); }
            if ((UseAngle) && (!UseHypot)) { Line.SetPosition(1, new Vector3(0.0f, 1.0f, 0.0f)); }
            if ((UseAngle) && (UseHypot)) { Line.SetPosition(1, new Vector3(0.0f, hyp, 0.0f)); UsePrev = true; }
            if ((!UseHypot) && (UsePrev)) { Line.SetPosition(1, new Vector3(0.0f, 1.0f, 0.0f)); UsePrev = false; }
        }
        if (UseFixed) { Rotation.x = 0.125f; Rotation.y = 0.125f; Rotation.z = 0.0f; }

        //scaled.x = Mathf.Repeat(RotationA.x * default_scale.x, default_scale.x);
        //scaled.y = Mathf.Repeat(RotationA.y * default_scale.y, default_scale.y);
        //scaled.z = Mathf.Repeat(RotationA.z * default_scale.z, default_scale.z);

        //scaled.x = Mathf.Repeat(RotationB.x * default_scale.x, default_scale.x);
        //scaled.y = Mathf.Repeat(RotationB.y * default_scale.y, default_scale.y);
        //scaled.z = Mathf.Repeat(RotationB.z * default_scale.z, default_scale.z);

        //!!! High Disk Usage By Unity Editor Console to an unmarked Temporary Location
        //Debug.Log(phase.ToString() + ", " + Rotors.x.ToString() + ", " + Rotors.y.ToString() + ", " + Rotors.z.ToString());

        return scaled;
    }
}
