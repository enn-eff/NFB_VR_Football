using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

public class CrowdManager : MonoBehaviour {


    #region Audio

    public AudioClip BackgroundCheers;
    public AudioClip AngryBoos;
    public AudioClip GoalCelebration;
    public AudioClip Panic;

    #endregion

    #region UI Attributes

    public Slider ControlSlider;
    public Text CurrentCutoffFrequency;

    public Button BackgroundCheersButton;
    public Button AngryBoosButton;
    public Button GoalCelebrationButton;
    public Button PanicButton;
    public Button MuteButton;
    public Button UnmuteButton;
    
    #endregion
    
    void Start ()
    {
        this.gameObject.GetComponent<AudioSource>().clip = BackgroundCheers;
        this.gameObject.GetComponent<AudioSource>().Play();
        CurrentCutoffFrequency.text = this.gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency.ToString();

        ControlSlider.onValueChanged.AddListener(delegate { OnSliderValueChanged(); });

        BackgroundCheersButton.onClick.AddListener(delegate { OnBackgroundCheersButtonPressed(); });
        AngryBoosButton.onClick.AddListener(delegate { OnAngryBoosButtonPressed(); });
        GoalCelebrationButton.onClick.AddListener(delegate { OnGoalCelebrationButtonPressed(); });
        PanicButton.onClick.AddListener(delegate { OnPanicButtonPressed(); });
        MuteButton.onClick.AddListener(delegate { MuteButtonClicked(); });
        UnmuteButton.onClick.AddListener(delegate { UnmuteButtonClicked(); });

    }

    void Update()
    {
        #region Keyboard Events

        if (Input.GetKeyDown("1"))
        {
            this.gameObject.GetComponent<AudioSource>().Stop();
            this.gameObject.GetComponent<AudioSource>().time = 2f;
            this.gameObject.GetComponent<AudioSource>().Play();


            this.gameObject.GetComponent<AudioSource>().PlayOneShot(AngryBoos);
        }
        else if (Input.GetKeyDown("2"))
        {
            this.gameObject.GetComponent<AudioSource>().PlayOneShot(GoalCelebration);
        }
        else if (Input.GetKeyDown("3"))
        {
            this.gameObject.GetComponent<AudioSource>().PlayOneShot(Panic);
        }
        else if (Input.GetKeyDown("`"))
        {
            if(gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency > 500)
            {
                this.gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency = 11000F;
                StartCoroutine(DampenSound(gameObject.GetComponent<AudioLowPassFilter>(), 11000F, 350F, (11000F - 300.0F), Time.time, 1F, 5000F));
            }
            else
            {
                StartCoroutine(DampenSound(gameObject.GetComponent<AudioLowPassFilter>(), 350F, 22000F, (22000F - 300.0F), Time.time, 1F, 5000F));
            }
        }

        #endregion
    }

    #region Slider Events

    private void OnSliderValueChanged()
    {
        CurrentCutoffFrequency.text = ControlSlider.value.ToString();
        gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency = ControlSlider.value;

    }

    #endregion

    #region Button Press Events

    private void OnBackgroundCheersButtonPressed()
    {
        this.gameObject.GetComponent<AudioSource>().Stop();
        this.gameObject.GetComponent<AudioSource>().time = 2f;
        this.gameObject.GetComponent<AudioSource>().Play();
    }

    private void OnAngryBoosButtonPressed()
    {
        this.gameObject.GetComponent<AudioSource>().PlayOneShot(AngryBoos);
    }

    private void OnGoalCelebrationButtonPressed()
    {
        this.gameObject.GetComponent<AudioSource>().PlayOneShot(GoalCelebration);
    }

    private void OnPanicButtonPressed()
    {
        this.gameObject.GetComponent<AudioSource>().PlayOneShot(Panic);
    }


    private void UnmuteButtonClicked()
    {
        if (gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency > 500)
        {
            this.gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency = 11000F;
            StartCoroutine(DampenSound(gameObject.GetComponent<AudioLowPassFilter>(), 11000F, 350F, (11000F - 300.0F), Time.time, 1F, 5000F));
        }
        else
        {
            StartCoroutine(DampenSound(gameObject.GetComponent<AudioLowPassFilter>(), 350F, 22000F, (22000F - 300.0F), Time.time, 1F, 5000F));
        }

    }

    private void MuteButtonClicked()
    {
        if (gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency > 500)
        {
            this.gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency = 11000F;
            StartCoroutine(DampenSound(gameObject.GetComponent<AudioLowPassFilter>(), 11000F, 350F, (11000F - 300.0F), Time.time, 1F, 5000F));
        }
        else
        {
            StartCoroutine(DampenSound(gameObject.GetComponent<AudioLowPassFilter>(), 350F, 22000F, (22000F - 300.0F), Time.time, 1F, 5000F));
        }
    }

    #endregion

    #region DampenSound Effect

    IEnumerator DampenSound(AudioLowPassFilter inAudioFilter, float StartValue, float TargetValue, float journeyLength, float startTime, float waitTime = 1, float speed = 1.0F)
    {
        bool LoopCondition = false;

        while (!LoopCondition)
        {
            float distCovered = (Time.time - startTime) * speed;
            float fracJourney = distCovered / journeyLength;
            inAudioFilter.cutoffFrequency = Mathf.Lerp(StartValue, TargetValue, fracJourney);
            ControlSlider.value = inAudioFilter.cutoffFrequency;
            CurrentCutoffFrequency.text = this.gameObject.GetComponent<AudioLowPassFilter>().cutoffFrequency.ToString();


            int actualVal = (int)(inAudioFilter.cutoffFrequency); 
            int targetVal = (int)(TargetValue);

            if (actualVal == targetVal)
            {
                LoopCondition = !LoopCondition;
            }

            yield return null;
        }
        yield return new WaitForSeconds(waitTime);
    }

    #endregion
}
