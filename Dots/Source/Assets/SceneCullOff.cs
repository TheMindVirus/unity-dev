using UnityEngine; //Required for Matrix4x4
using UnityEditor;

#if UNITY_EDITOR

public class CustomSettings
{
    [MenuItem("Edit/SceneView Settings/Update Camera Settings")]
    static void UpdateCameraSettings()
    {
        SceneView.CameraSettings settings = new SceneView.CameraSettings();
        settings.accelerationEnabled = false;
        settings.speedMin = 1f;
        settings.speedMax = 10f;
        settings.speed = 5f;
        settings.easingEnabled = true;
        settings.easingDuration = 0.6f;
        settings.dynamicClip = false;
        settings.fieldOfView = 120f;
        settings.nearClip = 0.01f;
        settings.farClip = 1000f;
        settings.occlusionCulling = true;
        SceneView sceneView = SceneView.lastActiveSceneView;
        sceneView.cameraSettings = settings;
    }

    [MenuItem("Edit/SceneView Settings/Revert to Defaults")]
    static void RevertToDefaults()
    {
        //SceneView.CameraSettings settings = new SceneView.CameraSettings();
        SceneView sceneView = SceneView.lastActiveSceneView;
        //sceneView.cameraSettings = settings;
        sceneView.ResetCameraSettings();
    }

    [MenuItem("Edit/SceneView Settings/Default No Culling")]
    static void DefaultNoCulling()
    {
        SceneView.CameraSettings settings = new SceneView.CameraSettings();
        /*settings.accelerationEnabled = false;
        settings.speedMin = 1f;
        settings.speedMax = 10f;
        settings.speed = 5f;
        settings.easingEnabled = true;
        settings.easingDuration = 0.6f;
        settings.dynamicClip = false;
        settings.fieldOfView = 120f;
        settings.nearClip = 0.01f;
        settings.farClip = 1000f;
        settings.occlusionCulling = true;*/
        settings.dynamicClip = false; //This does nothing
        settings.occlusionCulling = false; //Neither does this
        SceneView sceneView = SceneView.lastActiveSceneView;
        sceneView.cameraSettings = settings;
        sceneView.camera.cullingMatrix = new Matrix4x4();
    }
}

#endif//UNITY_EDITOR