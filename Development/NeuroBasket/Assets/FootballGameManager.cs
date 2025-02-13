﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FootballGameManager : MonoBehaviour {

    public GameObject respawnPrefab;
    public List<GameObject> ListOfRespwPositions;
    public List<GameObject> ListOfTargets;
    private float MIN_SPEED = 10.0F;
    private float MAX_SPEED = 14.0F;
    private float nextActionTime = 0.0f;
    public float period = 1f;
    int i = 0;
    public bool test;
    GameObject respawn; // only one respawn position and that is penalty position

    void Start()
    {
        ListOfTargets = new List<GameObject>();
        GameObject[] targets;
        targets = GameObject.FindGameObjectsWithTag("Target");
        respawn = GameObject.FindGameObjectWithTag("RespawnPosition");        

        foreach (GameObject curr in targets)
        {
            ListOfTargets.Add(curr);
        }

        StartCoroutine(generatingBall());
    }

    IEnumerator generatingBall()
    {
        Vector3 posIndex = respawn.transform.position;
        Quaternion rotationIndex = respawn.transform.rotation;
        respawnPrefab.tag = "Fot";

        while (i < 200)
        {
            test = false;
            float randomSpeed = Random.Range(MIN_SPEED, MAX_SPEED);
            yield return new WaitForSeconds(2);
            GameObject currGameObj = Instantiate(respawnPrefab, posIndex, rotationIndex);
            currGameObj.GetComponent<Rigidbody>().isKinematic = true;
            StartCoroutine(Move(currGameObj, ListOfTargets[Random.Range(0, ListOfTargets.Count)].gameObject.transform.position, randomSpeed));
            i++;
        }
        
    }


    //// Update is called once per frame
    //void Update ()
    //{ 

    //    if(Input.GetKeyDown("c"))
    //    {
    //        GameObject[] clearList;
    //        clearList = GameObject.FindGameObjectsWithTag("Fot");
    //        foreach (GameObject fot in clearList)
    //        {
    //            Destroy(fot);
    //        }
    //    }
    //    else if(Input.GetKeyDown("l"))
    //    {

    //    }
    //}

    IEnumerator Move(GameObject InGameO, Vector3 InTarget, float speed = 1.0F, float waitTime = 1)
    {
        bool LoopCondition = false;
        while (!LoopCondition)
        {
            float step = speed * Time.deltaTime;
            InGameO.transform.position = Vector3.MoveTowards(InGameO.transform.position, InTarget, step);

            int traX = (int)(InGameO.transform.position.x * 10000); int traY = (int)(InGameO.transform.position.y * 10000); int traZ = (int)(InGameO.transform.position.z * 10000);
            int inTrX = (int)(InTarget.x * 10000); int inTrY = (int)(InTarget.y * 10000); int inTrZ = (int)(InTarget.z * 10000);

            if (traX == inTrX && traY == inTrY && traZ == inTrZ)
            {
                LoopCondition = !LoopCondition;
            }
            
            yield return null;
        }
        yield return new WaitForSeconds(waitTime);
    }
    
}
