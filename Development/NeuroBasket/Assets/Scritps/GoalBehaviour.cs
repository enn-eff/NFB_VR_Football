#region Dependencies

using UnityEngine;
using System.Collections;
using System;

#endregion

public class GoalBehaviour : MonoBehaviour {

    #region Attributes

    private Vector3 defaultSize;
    private Vector3 defaultPosition;

    #endregion

    void Start()
    {
        defaultSize.x = transform.localScale.x;
        defaultSize.y = transform.localScale.y;
        defaultSize.z = transform.localScale.z;

        defaultPosition.x = transform.position.x;
        defaultPosition.y = transform.position.y;
        defaultPosition.z = transform.position.z;
    }

    void Update()
    {
        if (Input.GetKeyDown("f"))
        {
            Vector3 newSize = new Vector3((transform.localScale.x * 1.25F), (transform.localScale.y * 1.25F), (transform.localScale.z * 1.25F));
            float startTime = Time.time;
            float journeyLength = Vector3.Distance(transform.localScale, newSize);
            Vector3 newPos = new Vector3((transform.position.x + journeyLength), (transform.position.y + journeyLength), (transform.position.z));
            StartCoroutine(ChangeSize(transform.localScale, newSize, transform.position, newPos, journeyLength, startTime));
        }

        if (Input.GetKeyDown("g"))
        {
            Vector3 newSize = new Vector3((transform.localScale.x * 0.75F), (transform.localScale.y * 0.75F), (transform.localScale.z * 0.75F));
            float startTime = Time.time;
            float journeyLength = Vector3.Distance(transform.localScale, newSize);
            Vector3 newPos = new Vector3((transform.position.x - journeyLength), (transform.position.y - journeyLength), (transform.position.z - 0));
            StartCoroutine(ChangeSize(transform.localScale, newSize, transform.position, newPos, journeyLength, startTime));
        }

        if (Input.GetKeyDown("h"))
        {
            float startTime = Time.time;
            float journeyLength = Vector3.Distance(transform.localScale, defaultSize);
            StartCoroutine(ChangeSize(transform.localScale, defaultSize, transform.position, defaultPosition, journeyLength, startTime));
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

    IEnumerator ChangeSize(Vector3 InStartSize, Vector3 InTargetSize, Vector3 InStartPosition, Vector3 InTargetPosition, float journeyLength, float startTime, float waitTime = 1, float speed = 1.0F)
    {
        bool LoopCondition = false;
        while (!LoopCondition)
        {
            float distCovered = (Time.time - startTime) * speed;
            float fracJourney = distCovered / journeyLength;
            transform.localScale = Vector3.Lerp(InStartSize, InTargetSize, fracJourney);
            transform.position = Vector3.Lerp(InStartPosition, InTargetPosition, fracJourney);

            float precision = 1000.0F;
            int traX = (int)(transform.localScale.x * precision);   int traY = (int)(transform.localScale.y * precision);   int traZ = (int)(transform.localScale.z * precision);
            int inTrX = (int)(InTargetSize.x * precision);          int inTrY = (int)(InTargetSize.y * precision);          int inTrZ = (int)(InTargetSize.z * precision);

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