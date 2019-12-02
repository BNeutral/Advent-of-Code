using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuCallbacks : MonoBehaviour
{
    public string url;

    public void OpenURL()
    {
        Application.OpenURL(url);
    }

    public void SwitchScene(string sceneName)
    {
        SceneManager.LoadScene(sceneName);
    }

}
