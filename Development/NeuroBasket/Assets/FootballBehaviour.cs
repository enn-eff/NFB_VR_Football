//#region Dependecies

//using System.Collections;
//using System.Collections.Generic;
//using UnityEngine;
//using Valve.VR;

//#endregion

//public class FootballBehaviour : MonoBehaviour
//{

//    #region Attributes

//    private Valve.VR.EVRButtonId gripButton = Valve.VR.EVRButtonId.k_EButton_Grip;
//    private Valve.VR.EVRButtonId triggerButton = Valve.VR.EVRButtonId.k_EButton_SteamVR_Trigger;

//    private SteamVR_Controller.Device controller { get { return SteamVR_Controller.Input((int)trackedObj.index); } }
//    private SteamVR_TrackedObject trackedObj;

//    private GameObject pickup;

//    #endregion

//    void Start()
//    {
//        trackedObj = this.GetComponentInParent<SteamVR_TrackedObject>();
//    }

//    // Update is called once per frame
//    void Update()
//    {
//        if (controller.GetPressDown(Valve.VR.EVRButtonId.k_EButton_SteamVR_Trigger))
//        {
//            OnTriggerPressed();
//        }

//        if (controller.GetPressDown(Valve.VR.EVRButtonId.k_EButton_SteamVR_Touchpad))
//        {
//            OnTouchpadPressed();
//        }
//    }

//    void OnCollisionEnter(Collision collision)
//    {
//        //Check for a match with the specified name on any GameObject that collides with your GameObject
//        if (collision.gameObject.name == "Football")
//        {
//            pickup = collision.gameObject;
//            collision.gameObject.transform.GetComponent<Rigidbody>().isKinematic = true;
//            //collision.gameObject.transform.GetComponent<Rigidbody>().useGravity = false;
//            collision.gameObject.transform.parent = this.transform.parent;
//            collision.gameObject.transform.transform.Translate(new Vector3(0.15F, 0, 0));
//            //collision.gameObject.transform.transform.localScale = pickup.gameObject.transform.localScale;

//        }
//    }

//    private void OnTriggerPressed()
//    {
//        pickup.gameObject.transform.GetComponent<Rigidbody>().isKinematic = false;
//        pickup.gameObject.transform.parent = null;
//    }

//    private void OnTouchpadPressed()
//    {

//    }


//}