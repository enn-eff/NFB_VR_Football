using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScalingTargets : MonoBehaviour
{
    GameObject[] targets;
    public Vector3[] targetsInitialPosition { get; set; }
    public Vector3 toScale = new Vector3(0f, 0.001f,0.001f); 

    // Start is called before the first frame update
    void Start()
    {
        targets = GameObject.FindGameObjectsWithTag("Target");
        targetsInitialPosition = new Vector3[targets.Length];
        // saving initial positions for temporary uses.
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
            foreach (GameObject curr in targets)
            {
                // increasing scale target size
                curr.transform.localScale += toScale;
                
            }
            Debug.Log(targets[0].transform.localScale);
        }
        if (Input.GetKeyDown("p"))
        {
            for (int i =0; i < targets.Length;i++)
            {
                // decreasing scale targets size
                targets[i].transform.localScale -= toScale;
            }
            Debug.Log(targets[0].transform.localScale);
        }
        if (Input.GetKeyDown("i"))
        {
            for (int i = 0; i < targets.Length; i++)
            {
                // restoring targets default scaling
                targets[i].transform.localScale = targetsInitialPosition[i]; 
            }
            
        }

    }
}
