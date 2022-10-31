using UnityEngine;
using UnityEngine.AI;
using UnityEngine.Events;

public class MoveTo : MonoBehaviour
{
    public Transform goal;
    public UnityEvent objective;
    public UnityEvent reached;
    public NavMeshAgent agent;

    bool _reached = true;

    void Start()
    {
        objective.AddListener(Objective);
        reached.AddListener(Reached);
        agent = GetComponent<NavMeshAgent>();
        Move(goal.position);
    }

    void Move(Vector3 destination)
    {
        agent.destination = destination;
        objective.Invoke();
    }

    void Update() { Check(); }

    void Check()
    {
        if ((_reached == false) && (agent.remainingDistance == 0.0f)) { reached.Invoke(); }
    }

    void Objective()
    {
        _reached = false;
        Debug.Log("[INFO]: Objective: " + agent.destination.ToString());
        GetComponent<MeshRenderer>().material.DisableKeyword("_EMISSION");
    }

    void Reached()
    {
        _reached = true;
        Debug.Log("[INFO]: Reached");
        GetComponent<MeshRenderer>().material.EnableKeyword("_EMISSION");
    }
}
