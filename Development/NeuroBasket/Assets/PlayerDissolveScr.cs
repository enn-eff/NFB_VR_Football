﻿#region Dependencies

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

#endregion

public class PlayerDissolveScr : MonoBehaviour
{
    private Material DissolveMaterial;
    private Material DefaultMaterial;



    void Start ()
    {
        //UI_Manager.OnDissolveOpponentsPressed += UI_Manager_OnDissolveOpponentsPressed;
        //UI_Manager.OnResolveOpponentsPressed += UI_Manager_OnResolveOpponentsPressed;

        DefaultMaterial = gameObject.GetComponent<Renderer>().material;
        DissolveMaterial = Resources.Load("Diss2Mat") as Material;
        //Debug.Log(DissolveMaterial);
    }

    void Update ()
    {
        if (Input.GetKeyDown(KeyCode.Q))  //Trigger the dissolve animation
        {
            gameObject.GetComponent<Renderer>().material = DissolveMaterial;
            StartCoroutine(DissolveMaterialOverTime(DissolveMaterial, 0, 1, 3, Time.time));

        }
        else if (Input.GetKeyDown(KeyCode.W)) //Trigger the fade in animation
        {
            StartCoroutine(DissolveMaterialOverTime(DissolveMaterial, 1, 0, 3, Time.time, 1F, 1F, true));
        }
    }

    #region UI Button Actions

    private void UI_Manager_OnResolveOpponentsPressed()
    {
        StartCoroutine(DissolveMaterialOverTime(DissolveMaterial, 1, 0, 1, Time.time, 1F, 1F, true));
    }

    private void UI_Manager_OnDissolveOpponentsPressed()
    {
        gameObject.GetComponent<Renderer>().material = DissolveMaterial;
        StartCoroutine(DissolveMaterialOverTime(DissolveMaterial, 0, 1, 1, Time.time));
    }

    #endregion

    #region Fade Effect

    IEnumerator DissolveMaterialOverTime(Material inMaterial, float StartValue, float TargetValue, float journeyLength, float startTime, float waitTime = 1, float speed = 1.0F, bool SetBackToDefaultMaterial = false)
    {
        bool LoopCondition = false;

        while (!LoopCondition)
        {
            float distCovered = (Time.time - startTime) * speed;
            float fracJourney = distCovered / journeyLength;
            inMaterial.SetFloat("_Level", Mathf.Lerp(StartValue, TargetValue, fracJourney));
            

            int actualVal = (int)(inMaterial.GetFloat("_Level") * 100);
            int targetVal = (int)(TargetValue * 100);

            if (actualVal == targetVal)
            {
                LoopCondition = !LoopCondition;
            }

            yield return null;
        }

        if(SetBackToDefaultMaterial)
        {
            gameObject.GetComponent<Renderer>().material = DefaultMaterial;
        }

        yield return new WaitForSeconds(waitTime);
    }

    #endregion

}
