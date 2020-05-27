using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OnCollisionBitte : MonoBehaviour
{


    private void Start()
    {
        Debug.Log("<color=red>Message: </color> ntered ");
        
    }

    private void OnTriggerEnter(Collider collisionInfo)
    {
        Debug.Log("We were here.");
        Debug.Log(collisionInfo.gameObject.name);
        Debug.Log(collisionInfo.gameObject.tag);

        if (collisionInfo.gameObject.tag == "Fot" )
        {
            Debug.Log("<color=red>Message: </color> We are hitting the controller");
            Debug.Log(collisionInfo.gameObject.tag);
            //Destroy(collisionInfo.gameObject);
        }

    }
}
