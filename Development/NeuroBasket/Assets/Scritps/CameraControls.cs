using UnityEngine;
using System.Collections;

public class CameraControls : MonoBehaviour
{
    public GameObject player;
    private Vector3 offset;

    public float xDelta = 0.25f;
    public float zDelta = 0.25f;

    private Vector3 mouseOrigin;        // Position of cursor when mouse dragging starts
    private bool isRotating = false;    // Is the camera being rotated?

    public float turnSpeed = 4.0f;      // Speed of camera turning when mouse moves in along an axis

    public bool ghostMode = false;      //IsKinematic:true = ghostMode, IsKinematic:false = !ghostMode
    public int displayForFrames = 120;  //Display ghost mode message for 120 frames, ~2 seconds

    void Start()
    {
        gameObject.GetComponent<Rigidbody>().isKinematic = ghostMode;
    }
   
    void Update()
    {
        //Comment this back in order to get camera controls back
        ////Change camera controls based on input
        if (Input.GetKeyDown("1"))
        {
            ghostMode = !ghostMode;
            displayForFrames = 120;
        }
        displayForFrames--;
        gameObject.GetComponent<Rigidbody>().isKinematic = ghostMode;


        //Moving forward, left and right
        float xAxisValue = Input.GetAxis("Horizontal") * xDelta * 0.2f;
        float zAxisValue = Input.GetAxis("Vertical") * zDelta * 0.2f;
        if (Camera.current != null)
        {
            this.transform.Translate(new Vector3(xAxisValue, 0.0f, zAxisValue));

        }



        if (Input.GetMouseButtonDown(0))
        {
            // Get mouse origin
            mouseOrigin = Input.mousePosition;
            isRotating = true;
        }

        if (!Input.GetMouseButton(0)) isRotating = false;

        if (isRotating)
        {
            Vector3 pos = (this.GetComponent<Camera>()).ScreenToViewportPoint(Input.mousePosition - mouseOrigin);

            this.gameObject.transform.RotateAround(transform.position, transform.right, -pos.y * turnSpeed);
            this.gameObject.transform.RotateAround(transform.position, Vector3.up, pos.x * turnSpeed);

            //player.transform.RotateAround(transform.position, transform.right, -pos.y * turnSpeed);
            //player.transform.RotateAround(transform.position, Vector3.up, pos.x * turnSpeed);
        }
    }

    void OnGUI()
    {
        if (!ghostMode && displayForFrames > 0)
        {
            GUI.Label(new Rect(Screen.width / 2 - 75, Screen.height - 100, 150, 30), "Player Mode");
        }
        else if (ghostMode && displayForFrames > 0)
        {
            GUI.Label(new Rect(Screen.width / 2 - 75, Screen.height - 100, 150, 30), "Ghost Mode");
        }

    }

}