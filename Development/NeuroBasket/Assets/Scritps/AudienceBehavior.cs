using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AudienceBehavior : MonoBehaviour
{
    AudioSource audio;
    // Start is called before the first frame update
    void Start()
    {
        audio = GetComponent<AudioSource>();
        audio.clip = Resources.Load<AudioClip>("ApplauseCheerSound");
        audio.Play();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
