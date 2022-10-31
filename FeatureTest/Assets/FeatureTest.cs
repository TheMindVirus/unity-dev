using UnityEngine;

using Unity.Collections;
using Unity.Burst;
using Unity.Jobs;

//using UnityEngine.Experimental.Rendering; //Only available in Experimental Build
//using UnityEngine.NVIDIAModule; //Only available as Built-in Package in later versions
using Unity.Barracuda;

#if UNITY_EDITOR
using UnityEditor.Scripting.Python;
#endif

public class FeatureTest : MonoBehaviour
{
/*
    [TASK]: AI -> NavMesh
    [TASK]: Events -> UnityEvent
    [DONE]: See MoveTo and Window->AI->Navigation

    [TASK]: Burst -> BurstCompile
    [TASK]: Jobs -> Schedule
    [DONE]: See Task and Jobs->Burst->Open Inspector...

    [TASK]: NVIDIA -> DLSSContext
    [TASK]: Barracuda -> Tensor
    [FAIL]: Packages in Corrupt State

    [TASK]: ML Agents -> Runtime
    [TASK]: PolyBrush -> Runtime
    [TASK]: ProBuilder -> Runtime
    [FAIL]: Broken Gross Overcomplication Fluff on top of built-in and external tools

    [TASK]: Other -> AssetBundles Script Packing and Loading
    [????]: Not Tested - Requires Tabletop Simulator Modding Extensions
*/

    void Start()
    {
        ProfileNonBurst();
        ProfileBurst();
        AcceleratorStart();
    }

    void ProfileNonBurst()
    {
        float delta = Time.realtimeSinceStartup;

        var inputTest = new float[10];
        var outputTest = new float[1];
        for (int i = 0; i < inputTest.Length; ++i) { inputTest[i] = 1.0f * i; }
        NonBurst(inputTest, out outputTest);

        delta = Time.realtimeSinceStartup - delta;
        Debug.Log("[TIME]: NonBurst(): " + delta.ToString());
    }

    void ProfileBurst()
    {
        float delta = Time.realtimeSinceStartup;

        var inputData = new NativeArray<float>(10, Allocator.Persistent);
        var outputData = new NativeArray<float>(1, Allocator.Persistent);
        for (int i = 0; i < inputData.Length; ++i) { inputData[i] = 1.0f * i; }

        var task = new Task { Input = inputData, Output = outputData };
        task.Schedule().Complete();
        inputData.Dispose();
        outputData.Dispose();

        delta = Time.realtimeSinceStartup - delta;
        Debug.Log("[TIME]: Burst(): " + delta.ToString());
    }

    void NonBurst(float[] Input, out float[] Output)
    {
        float result = 0.0f;
        for (int i = 0; i < Input.Length; ++i) { result += Input[i]; }
        Output = new float[1] { result };
    }

    [BurstCompile(CompileSynchronously = true)]
    private struct Task : IJob
    {
        [ReadOnly]
        public NativeArray<float> Input;

        [WriteOnly]
        public NativeArray<float> Output;

        public void Execute()
        {
            float result = 0.0f;
            for (int i = 0; i < Input.Length; ++i) { result += Input[i]; }
            Output[0] = result;
        }
    }

    void AcceleratorStart()
    {
        //DLSSContext dlss = new NVIDIA.DLSSContext(); //This package has missing contents
        LoadOnyxModel("ssd_mobilenet_v1_12-int8.onyx");
#if UNITY_EDITOR
        Debug.Log("[INFO]: PythonRunner: " + PythonRunner.IsInitialized.ToString());
        PythonRunner.RunString(@"import UnityEngine; UnityEngine.Debug.Log('hello world')");
        PythonRunner.RunFile(Application.streamingAssetsPath + "/Python/" + "new_python_script.py");
#else
        Debug.Log("[WARN]: PythonRunner: Disabled - No UnityEditor Detected");
#endif
    }

    void LoadOnyxModel(string filename)
    {
        try
        {
            var model = Unity.Barracuda.ModelLoader.Load(Application.streamingAssetsPath + "/Onyx/" + filename);
            var engine = Unity.Barracuda.WorkerFactory.CreateWorker(model, WorkerFactory.Device.GPU);
            var input = new Tensor(1, 1, 1, 10);
            var output = engine.Execute(input).PeekOutput();
        }
        catch { Debug.Log("[ONYX]: Failed to load " + filename.ToString()); }
    }
}
