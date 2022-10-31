using System.IO;
using UnityEngine;
using UnityEditor;

#if UNITY_EDITOR
public class builder
{
    static string output = "Assets/bundles";

    [MenuItem("Assets/Build AssetBundles")]
    static void BuildAllAssetBundles()
    {
        if (!Directory.Exists(output)) { Directory.CreateDirectory(output); }
        ////BuildPipeline.BuildAssetBundles(output, BuildAssetBundleOptions.None, BuildTarget.StandaloneWindows);
        BuildPipeline.BuildAssetBundles(output, BuildAssetBundleOptions.None, BuildTarget.WebGL);
        //BuildPipeline.BuildAssetBundles(output, BuildAssetBundleOptions.UncompressedAssetBundle, BuildTarget.WebGL);
        //BuildPipeline.BuildAssetBundles(output, BuildAssetBundleOptions.None, EditorUserBuildSettings.selectedStandaloneTarget);
        
        string[] files = Directory.GetFiles(output);
        foreach (string path in files)
        {
            if (Path.GetFileName(path) == "AssetBundles" || path.EndsWith(".manifest") || path.EndsWith(".meta")) { File.Delete(path); }
            else if (!Path.HasExtension(path))
            {
                string pathext = path + ".unity3d";
                if (File.Exists(pathext)) { File.Delete(pathext); }
                File.Move(path, pathext);
             }
        }
        Debug.Log("Build complete! AssetBundles can be found in the '" + output + "' folder.");
    }
}
#endif