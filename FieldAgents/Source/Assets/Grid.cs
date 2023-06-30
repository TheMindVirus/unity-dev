using UnityEngine;
using System.Collections;

public class Grid : MonoBehaviour
{
    private IEnumerator coroutine;

    public Transform grid = null;
    public GameObject agent = null;

    void Start()
    {
        //Affector();
        //Test();
        //Traverse();
        //Traverse(true);
        //coroutine = Coroutine_Test();
        coroutine = Coroutine_Stagger(0.1f);
        StartCoroutine(coroutine);
    }

    void Affector()
    {
        foreach (Transform node in grid)
        {
            node.gameObject.AddComponent<Rigidbody>();
            node.gameObject.GetComponent<Rigidbody>().useGravity = false;
        }
    }

    void Test()
    {
        GameObject operativeA = GameObject.Instantiate(agent);
        operativeA.name = agent.name;
        operativeA.transform.parent = transform.Find("/Grid/Node_1_1_1");
        operativeA.transform.position = operativeA.transform.parent.position;
        operativeA.GetComponent<Target>().target = transform.Find("/Grid/Node_4_4_4");
        operativeA.SetActive(true);

        GameObject operativeB = GameObject.Instantiate(agent);
        operativeB.name = agent.name;
        operativeB.transform.parent = transform.Find("/Grid/Node_4_1_1");
        operativeB.transform.position = operativeB.transform.parent.position;
        operativeB.GetComponent<Target>().target = transform.Find("/Grid/Node_1_4_4");
        operativeB.SetActive(true);
    }

    void Traverse(bool break_early = false)
    {
        foreach (Transform node in grid)
        {
            foreach (Transform target in grid)
            {
                GameObject operative = GameObject.Instantiate(agent);
                operative.name = agent.name;
                operative.transform.parent = node;
                operative.transform.position = operative.transform.parent.position;
                operative.GetComponent<Target>().target = target;
                operative.SetActive(true);
            }   if (break_early) { break; }
        }
    }

    private IEnumerator Coroutine_Test(int n = 10, float t = 1.0f)
    {
        yield return false;
        for (var i = 0; i < n; ++i) { Debug.Log(i); yield return new WaitForSeconds(t); }
        yield return true;
    }

    private IEnumerator Coroutine_Stagger(float interval = 1.0f)
    {
        yield return false;
        foreach (Transform node in grid)
        {
            foreach (Transform target in grid)
            {
                GameObject operative = GameObject.Instantiate(agent);
                operative.name = agent.name;
                operative.transform.parent = node;
                operative.transform.position = operative.transform.parent.position;
                operative.GetComponent<Target>().target = target;
                operative.SetActive(true);
                yield return new WaitForSeconds(interval);
            }
        }
        yield return true;
    }
}