using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;

[ExecuteInEditMode]
public class GreasePencil : MonoBehaviour
{
    public bool toggle = false;
    public float size = 1.0f;
    public float distance = 30.0f;
    public Material material = null;
    public GameObject _collider = null;

    private bool _toggle;
    private Event _event;
    private Vector3 _mouse;
    private Vector3 _point;
    private GameObject _brush;
    
    void OnValidate() { if (!toggle && _toggle) { _toggle = false; } }

    void OnEnable()
    {
        _toggle = false;
        _event = new Event();
        _mouse = new Vector3(0.0f, 0.0f, 0.0f);
        _point = new Vector3(0.0f, 0.0f, 0.0f);
        _brush = null;
        SceneView.duringSceneGui += OnScene;
    }

    void OnScene(SceneView scene)
    {
        _event = Event.current;
        _mouse = _event.mousePosition;

        if ((_event.type == EventType.MouseDown && _event.isMouse && _event.button == 0) && (toggle && !_toggle))
        {
            _toggle = true;
            Debug.Log("Press");
            GUIUtility.hotControl = 0;
        }
        else if ((_event.type == EventType.MouseUp && _event.isMouse && _event.button == 0) && (toggle && _toggle))
        {
            _toggle = false;
            Debug.Log("Release");
        }
        if (_event.type == EventType.KeyDown && _event.keyCode == KeyCode.Escape)
        {
            _toggle = false;
            Debug.Log("Emergency Release");
        }
        if (_toggle)
        {
            //_point = scene.camera.ScreenToWorldPoint(new Vector3(_mouse.x, Screen.height - _mouse.y - 40.0f, scene.camera.nearClipPlane + distance));
            Ray ray = scene.camera.ScreenPointToRay(new Vector3(_mouse.x, Screen.height - _mouse.y, scene.camera.nearClipPlane));
            RaycastHit hit = new RaycastHit();
            if (Physics.Raycast(ray, out hit))
            {
                if ((_collider == null) || ((_collider != null) /* && (hit.collider.gameObject == _collider)*/))
                {
                    _point = hit.point;
                    Debug.Log(_point);
                    _brush = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                    _brush.transform.position = _point;
                    _brush.transform.parent = this.transform;
                    _brush.transform.localScale = new Vector3(size, size, size);
                    _brush.transform.localPosition = new Vector3(_brush.transform.localPosition.x, 0.0f, _brush.transform.localPosition.z);
                    if (material != null) { _brush.GetComponent<MeshRenderer>().sharedMaterial = material; }
                }
            }
        }
    }
}
