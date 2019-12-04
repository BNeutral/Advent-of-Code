using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using System.Runtime.InteropServices;

public class MenuCallbacks : MonoBehaviour
{
    public string url;
    public GameObject loadingImage;

    // From https://va.lent.in/opening-links-in-a-unity-webgl-project/
    [DllImport("__Internal")]
    private static extern void openWindow(string url);
    public void OpenURL()
    {
        #if UNITY_WEBGL
                    openWindow(url);
        #else
            Application.OpenURL(url);
        #endif
    }
       
    public void SwitchScene(string sceneName)
    {
        loadingImage.SetActive(true);
        SceneManager.LoadScene(sceneName);
    }

}
