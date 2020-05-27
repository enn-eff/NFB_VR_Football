using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AudienceBehavior : MonoBehaviour
{
    AudioSource audio;
    //float IncVolume = 0.8f;
    //float DecVolume = 0.8f;
    //float VolumeRate = 0.1f;
    // Start is called before the first frame update
    void Start()
    {
        audio = GetComponent<AudioSource>();
        audio.clip = Resources.Load<AudioClip>("ApplauseCheerSound");
        audio.Play();
    }

    //private void Update()
    //{
    //    if (Input.GetKeyDown(KeyCode.W))
    //    {
    //        IncVolume = IncVolume + (VolumeRate * Time.deltaTime);
    //        //audio.enabled = !GetComponent<AudioSource>().enabled;
    //        audio.volume = IncVolume;
    //    }
    //    if (Input.GetKeyDown(KeyCode.Q))
    //    {
    //        DecVolume = DecVolume - (VolumeRate * Time.deltaTime);
    //        audio.volume = DecVolume;
    //    }
    //}
}
