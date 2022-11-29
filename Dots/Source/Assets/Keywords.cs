using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;

#if UNITY_EDITOR

[ExecuteInEditMode]
public class Keywords : MonoBehaviour
{
    private bool _cullState = true;

    void Awake()
    {
        if (Shader.IsKeywordEnabled("Occlude")) { Debug.Log("KEYWORD"); }
        else { Debug.Log("NO KEYWORD"); }
    }

    void Update()
    {
        var shader = GetComponent<MeshRenderer>().sharedMaterial.shader;
        if (shader != null)
        {
            var tag = shader.FindPassTagValue(0, new ShaderTagId("Occlude")); //Forced Pass Index 0
            if (tag != null) { Debug.Log(tag.name); }
            else { Debug.Log("NO KEYWORD"); }

            // Pass { Tags { "Occlude" = "Off" } //<-- THIS APPEARED. NOT FROM SUBSHADER.

            if (tag.name == "Off")
            {
                _cullState = false;
            }
        }
        //SceneView sceneView = SceneView.lastActiveSceneView;
        //sceneView.camera.onPreRender = OnPreRender;
        //sceneView.camera.onPostRender = OnPostRender;
        Camera.onPreRender = _OnPreRender;
        Camera.onPostRender = _OnPostRender;
    }

    private Matrix4x4 _cullMatrixPrev;

    //Shader Pass Pre and Post Events Required : Shader.OnPrePass(int) Shader.OnPostPass(int)
    void _OnPreRender(Camera cam)
    {
        //Debug.Log("PreRender");
        _cullMatrixPrev = cam.cullingMatrix;
        if (_cullState == false) { cam.cullingMatrix = new Matrix4x4(); } //!!!No Undo, Editor Reload
    }

    void _OnPostRender(Camera cam)
    {
        //Debug.Log("PostRender");
        cam.cullingMatrix = _cullMatrixPrev;
        //Unity Will Cheekily try to rewrite this as GetComponent<Camera>() which is incorrect.
    }
}

#endif//UNITY_EDITOR