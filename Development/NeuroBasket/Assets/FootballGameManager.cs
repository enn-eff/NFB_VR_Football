using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FootballGameManager : MonoBehaviour {

    public GameObject respawnPrefab;
    public List<GameObject> ListOfRespwPositions;
    public List<GameObject> ListOfTargets;
    private float MIN_SPEED = 13.0F;
    private float MAX_SPEED = 26.0F;


    void Start()
    {
        ListOfRespwPositions = new List<GameObject>();
        ListOfTargets = new List<GameObject>();
        
        GameObject[] respawns;
        respawns = GameObject.FindGameObjectsWithTag("RespawnPosition");
        GameObject[] targets;
        targets = GameObject.FindGameObjectsWithTag("Target");

        foreach (GameObject curr in respawns)
        {
            ListOfRespwPositions.Add(curr);
        }
        foreach (GameObject curr in targets)
        {
            ListOfTargets.Add(curr);
        }

    }

    // Update is called once per frame
    void Update ()
    { 
        if (Input.GetKeyDown("r"))
        {
            int randPosIndex = Random.Range(0, ListOfRespwPositions.Count);
            int randTargetIndex = Random.Range(0, ListOfTargets.Count);
            float randomSpeed = Random.Range(MIN_SPEED, MAX_SPEED);
            Debug.Log("Speed = " + randomSpeed);
            respawnPrefab.tag = "Fot";
            GameObject currGameObj = Instantiate(respawnPrefab, ListOfRespwPositions[randPosIndex].transform.position, ListOfRespwPositions[randPosIndex].transform.rotation);
            StartCoroutine(Move(currGameObj, ListOfTargets[randTargetIndex].gameObject.transform.position, randomSpeed));
        }
        else if(Input.GetKeyDown("c"))
        {
            GameObject[] clearList;
            clearList = GameObject.FindGameObjectsWithTag("Fot");
            foreach (GameObject fot in clearList)
            {
                Destroy(fot);
            }
        }
        else if(Input.GetKeyDown("l"))
        {

        }
    }

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
