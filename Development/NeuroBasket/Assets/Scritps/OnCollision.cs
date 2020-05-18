using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class OnCollision : MonoBehaviour
{


    private void Start()
    {
        Debug.Log("<color=red>Message: </color> ntered ");
        
    }

    private void OnCollisionEnter(Collision collisionInfo)
    {
        Debug.Log(collisionInfo.gameObject.name);
        Debug.Log(collisionInfo.gameObject.tag);

        if (collisionInfo.gameObject.name == "Controller_(right)" )
        {
            Debug.Log("<color=red>Message: </color> We are hitting the controller");
            Debug.Log(collisionInfo.gameObject.tag);
            //Destroy(collisionInfo.gameObject);
        }

    }
}
