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
        audio.volume = 0.5f;
        audio.Play();
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(KeyCode.A))
        {
            audio.clip = Resources.Load<AudioClip>("AngryCrowdSoundEffect");
            audio.Play();
        }
        if (Input.GetKeyDown(KeyCode.D))
        {
            audio.clip = Resources.Load<AudioClip>("ApplauseCheerSound");
            audio.Play();
        }
        if (Input.GetKeyDown(KeyCode.S))
        {
            audio.clip = Resources.Load<AudioClip>("CrowdPanicEffects");
            audio.Play();
        }
        if (Input.GetKeyDown(KeyCode.Z))
        {
            audio.volume = audio.volume - 0.1f;
        }
        if (Input.GetKeyDown(KeyCode.X))
        {
            audio.volume = audio.volume + 0.1f;
        }
    }
}