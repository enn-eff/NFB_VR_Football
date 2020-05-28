using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class OnCollisionBitte : MonoBehaviour
{
    public Text Score;
    private int defaultScore = 0;
    
    private void OnTriggerEnter(Collider collisionInfo)
    {
        if (collisionInfo.gameObject.tag == "Fot" )
        {

            Debug.Log("<color=red>Score: </color>" + Score.text);
            defaultScore = int.Parse(Score.text) + 1;
            Score.text = defaultScore.ToString();
            Debug.Log(collisionInfo.gameObject.tag);
            Destroy(collisionInfo.gameObject);
        }

    }
}
