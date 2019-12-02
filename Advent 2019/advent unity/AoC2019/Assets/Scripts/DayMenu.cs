using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEditor;

[RequireComponent(typeof(CanvasGroup))]
public class DayMenu : MonoBehaviour
{
    private CanvasGroup CanvasGroup;
    [Tooltip("Name of the scene to return to.")]
    public string MenuSceneName;
    [Tooltip("Object that contains a GameTemplate component")]
    public GameObject inputOwner;
    public static string CustomInputPath;
    public static string CustomInputPathScene;

    private void Start()
    {
        CanvasGroup = GetComponent<CanvasGroup>();
    }

    public void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape)) {
            SwitchScene(MenuSceneName);
        }
        else if (Input.GetKeyDown(KeyCode.R))
        {
            ResetScene();
        }
        else if(Input.GetKeyDown(KeyCode.L))
        {
            CustomInputPath = EditorUtility.OpenFilePanel("What input file?", "", "txt");
            CustomInputPathScene = SceneManager.GetActiveScene().name;
            ResetScene();
        }
        else if(Input.GetKeyDown(KeyCode.H))
        {
            FlipHiding();
        }
    }

    /**
     * Hides or unhides the group canvas that should be parent to the game object that owns this
     */
    public void FlipHiding()
    {
        CanvasGroup.alpha = CanvasGroup.alpha == 0f ? 1f : 0f;
        return;
    }

    public void SwitchScene(string sceneName)
    {
        SceneManager.LoadScene(sceneName);
    }


    public void ResetScene()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().name);
    }

}
