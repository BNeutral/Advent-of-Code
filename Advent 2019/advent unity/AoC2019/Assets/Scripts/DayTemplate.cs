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
    public TextAsset inputFile;
    [Tooltip("If not null, use this string instead of the default input file.")]
    public string textInput;

    /**
     * Decides which input to give to the Day
     */
    protected string getText()
    {
        if (textInput != "") return textInput;
        else return inputFile.text;
    }

    /**
     * Resets the scene back to the starting state more or less
     */
    public abstract void ResetScene();

}
