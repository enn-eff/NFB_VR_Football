using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Valve.VR;

public class HandAnimator : MonoBehaviour
{
    public SteamVR_Action_Single m_GrabAction = null;
    private Animator m_Animator = null;
    private SteamVR_Behaviour_Pose m_Pose = null;
    private GameObject rightHand;

    //private void Start()
    //{
    //    rightHand = GameObject.Find("Controller (left)");
    //    rightHand.transform.position = new Vector3(0,0,0);
    //}

    private void Awake()
    {
        m_Animator = GetComponent<Animator>();
        m_Pose = GetComponentInParent<SteamVR_Behaviour_Pose>();

        m_GrabAction[m_Pose.inputSource].onChange += Grab;
    }

    private void OnDestroy()
    {
        m_GrabAction[m_Pose.inputSource].onChange -= Grab;
    }

    private void OnColliderEnter (Collision other)
    {
        m_Animator.SetBool("Point", true);

        //Debug.Log("Triggered");
        //if (other.gameObject.tag.Equals("Fot"));
        //{
        //    Debug.Log("Hitting Football");
        //   // Destroy(gameObject);
        //}
    }

    private void OnTriggerExit(Collider other)
    {
        m_Animator.SetBool("Point", false);
    }

    private void Grab(SteamVR_Action_Single action, SteamVR_Input_Sources source, float axis, float delta)
    {
        m_Animator.SetFloat("GrabBlend", axis);
    }

    //void OnCollisionEnter(Collision collision)
    //{
    //    //Check for a match with the specified name on any GameObject that collides with your GameObject
    //    if (collision.gameObject.name == "Cube")
    //    {
    //        //If the GameObject's name matches the one you suggest, output this message in the console
    //        Debug.Log("Do something here");
    //    }

    //    //Check for a match with the specific tag on any GameObject that collides with your GameObject
    //    if (collision.gameObject.tag == "MyGameObjectTag")
    //    {
    //        //If the GameObject has the same tag as specified, output this message in the console
    //        Debug.Log("Do something else here");
    //    }
    //}
}
