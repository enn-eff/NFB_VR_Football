using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScalingTargets : MonoBehaviour
{
    GameObject[] targets;
    public Vector3[] targetsInitialPosition { get; set; }

    //GameObject[] testt;
    //public List<GameObject> ListOfTargets;
    // Start is called before the first frame update
    void Start()
    {
        targets = GameObject.FindGameObjectsWithTag("Target");
        targetsInitialPosition = new Vector3[targets.Length];
        for (int i =0; i < targets.Length; i++)
        {
            targetsInitialPosition[i] = targets[i].transform.localScale;
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown("o"))
        {
            
            Debug.Log(targets);
            foreach (GameObject curr in targets)
            {
                curr.transform.localScale = new Vector3(0.05f, 0.05f, 0.05f);
            }
            //testt = GameObject.FindGameObjectsWithTag("Test");
            //testt[0].transform.localScale = new Vector3(0.5f,0.5f,0.5f);
        }
        if (Input.GetKeyDown("p"))
        {
            //foreach (GameObject curr in targets)
            //{
            //    curr.transform.localScale = targetsInitialPosition(curr);
            //}
            for (int i =0; i < targets.Length;i++)
            {
                targets[i].transform.localScale = targetsInitialPosition[i];
            }

        }
        
    }
}
