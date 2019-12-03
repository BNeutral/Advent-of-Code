using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuCallbacks : MonoBehaviour
{
    public string url;
    public GameObject loadingImage;

    public void OpenURL()
    {
        Application.OpenURL(url);
    }

    public void SwitchScene(string sceneName)
    {
        loadingImage.SetActive(true);
        SceneManager.LoadScene(sceneName);
    }

}
