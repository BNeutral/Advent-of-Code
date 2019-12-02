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

    /**
     * Decides which input to give to the Day
     */
    protected string getText()
    {
        if (DayMenu.CustomInputPath != null && DayMenu.CustomInputPath.Length > 0 && DayMenu.CustomInputPathScene != null && SceneManager.GetActiveScene().name == DayMenu.CustomInputPathScene)
        {
            return File.ReadAllText(DayMenu.CustomInputPath);
        }
        else return inputFile.text;
    }
}
