using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScalingTargets : MonoBehaviour
{
    GameObject[] targets;
    public Vector3[] targetsInitialPosition { get; set; }
    //public Vector3 toScale = 

    // Start is called before the first frame update
    void Start()
    {
        targets = GameObject.FindGameObjectsWithTag("Target");
        targetsInitialPosition = new Vector3[targets.Length];
        for (int i =0; i < targets.Length; i++)
        {
        // stroing initial scaling of all the targets.
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
                // scaling target size
                curr.transform.localScale = new Vector3(0.05f, 0.05f, 0.05f);
            }
        }
        if (Input.GetKeyDown("p"))
        {
            for (int i =0; i < targets.Length;i++)
            {
                // restoring targets default scaling
                targets[i].transform.localScale = targetsInitialPosition[i];
            }

        }
        
    }
}
