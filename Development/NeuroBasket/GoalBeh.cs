#region Dependencies

using UnityEngine;
using System.Collections;
using System;

#endregion

public class GoalBehaviour : MonoBehaviour {

    #region Attributes

    private Vector3 defaultSize;
    private Vector3 maxSize;
    private Vector3 minSize;

    #endregion

    void Start()
    {
        defaultSize.x = transform.localScale.x;
        defaultSize.y = transform.localScale.y;
        defaultSize.z = transform.localScale.z;

        maxSize = new Vector3((defaultSize.x * 2), (defaultSize.y * 2), (defaultSize.z * 2));
        minSize = new Vector3((defaultSize.x / 2), (defaultSize.y / 2), (defaultSize.z / 2));

        //journeyLengthIncrease = Vector3.Distance(defaultSize, maxSize);
        //journeyLengthDecrease = Vector3.Distance(defaultSize, minSize);

    }

    void Update()
    {
        if (Input.GetKeyDown("f"))
        {
            float startTime = Time.time;
            float journeyLength = Vector3.Distance(transform.localScale, maxSize);
            StartCoroutine(ChangeSize(transform.localScale, maxSize, journeyLength, startTime, 1, 1.0F));
        }

        if (Input.GetKeyDown("g"))
        {
            float startTime = Time.time;
            float journeyLength = Vector3.Distance(transform.localScale, minSize);
            StartCoroutine(ChangeSize(transform.localScale, minSize, journeyLength, startTime, 1, 1.0F));
        }

        if (Input.GetKeyDown("h"))
        {
            float startTime = Time.time;
            float journeyLength = Vector3.Distance(transform.localScale, defaultSize);
            StartCoroutine(ChangeSize(transform.localScale, defaultSize, journeyLength, startTime, 1, 1.0F));
        }



    }

    void OnGUI()
    {
        //if (enter && !open)
        //{
        //    GUI.Label(new Rect(Screen.width / 2 - 75, Screen.height - 100, 150, 30), "Press 'F' to open");
        //}
        //if (enter && open)
        //{
        //    GUI.Label(new Rect(Screen.width / 2 - 75, Screen.height - 100, 150, 30), "Press 'G' to close");
        //}   

    }

    #region ChangeSize Animation

    IEnumerator ChangeSize(Vector3 InStartSize, Vector3 InTargetSize, float journeyLength, float startTime, float waitTime = 1, float speed = 0.001F)
    {
        bool LoopCondition = false;

        while (!LoopCondition)
        {
            float distCovered = (Time.time - startTime) * speed;
            float fracJourney = distCovered / journeyLength;
            transform.localScale = Vector3.Lerp(InStartSize, InTargetSize, fracJourney);
            //transform.position = Vector3.Lerp(InStartSize, InTargetSize, fracJourney);


            int traX = (int)(transform.localScale.x * 10000);   int traY = (int)(transform.localScale.y * 10000);   int traZ = (int)(transform.localScale.z * 10000);
            int inTrX = (int)(InTargetSize.x * 10000);          int inTrY = (int)(InTargetSize.y * 10000);          int inTrZ = (int)(InTargetSize.z * 10000);

            if (traX == inTrX && traY == inTrY && traZ == inTrZ)
            {
                LoopCondition = !LoopCondition;
            }

            yield return null;
    }
    yield return new WaitForSeconds(waitTime);
    }

    IEnumerator ChangePosition(Vector3 InStartPos, Vector3 InTargetPos, float journeyLength, float startTime, float waitTime = 1, float speed = 0.001F)
    {
        bool LoopCondition = false;

        while (!LoopCondition)
        {
            float distCovered = (Time.time - startTime) * speed;
            float fracJourney = distCovered / journeyLength;
            transform.position = Vector3.Lerp(InStartPos, InTargetPos, fracJourney);

            int traX = (int)(transform.position.x * 10000); int traY = (int)(transform.position.y * 10000); int traZ = (int)(transform.position.z * 10000);
            int inTrX = (int)(InTargetPos.x * 10000); int inTrY = (int)(InTargetPos.y * 10000); int inTrZ = (int)(InTargetPos.z * 10000);

            if (traX == inTrX && traY == inTrY && traZ == inTrZ)
            {
                LoopCondition = !LoopCondition;
            }

            yield return null;
        }
        yield return new WaitForSeconds(waitTime);
    }


    #endregion

}