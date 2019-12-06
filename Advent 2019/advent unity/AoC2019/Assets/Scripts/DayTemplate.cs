using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;

/**
 * Only really for the inputFile atm
 */
public abstract class DayTemplate : MonoBehaviour
{
    [Tooltip("Text file to use as input")]
    [SerializeField]
    private TextAsset inputFile = null;
    [Tooltip("If not null, use this string instead of the default input file.")]
    [HideInInspector]
    public string textInput;

    protected void Awake()
    {
        if (textInput == "") {
            textInput = inputFile.text.Trim();
        }        
    }

    /**
     * Resets the scene back to the starting state more or less
     */
    public abstract void ResetScene();

    /**
     * Randomizes the input of the scene
     */
    public abstract void RandomizeInput();

}
