#region Dependencies
using UnityEngine;
using System.Collections;
#endregion

public class ColliderNotify : MonoBehaviour {

    #region Attributes

    public delegate void OnPlayerInside();
    public event OnPlayerInside PlayerInside;

    public delegate void OnPlayerOutside();
    public event OnPlayerOutside PlayerOutside;

    #endregion

    // Use this for initialization
    void Start ()
    {
	
	}
	
	// Update is called once per frame
	void Update ()
    {
	
	}

    //Activate the Main function when player is near the door
    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.tag == "Player")
        {
            PlayerInside();
        }
    }

    //Deactivate the Main function when player is away from door
    void OnTriggerExit(Collider other)
    {
        if (other.gameObject.tag == "Player")
        {
            PlayerOutside();
        }
    }
}
