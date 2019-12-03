using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class DayMenu : MonoBehaviour
{
    [Tooltip("UI element that shows the instructions and can be disabled.")]
    public GameObject Instructions;
    [Tooltip("UI element for setting the custom input.")]
    public GameObject Modal;
    [Tooltip("UI element with the actual custom input text.")]
    public InputField CustomInputText;
    [Tooltip("Name of the scene to return to.")]
    public string MenuSceneName = "Menu";
    [Tooltip("Object that contains a GameTemplate component")]
    public GameObject DayTemplateOwner;
    private bool acceptInput = true;

    public void Update()
    {
        if (acceptInput)
        {
            if (Input.GetKeyDown(KeyCode.Escape))
            {
                SwitchScene(MenuSceneName);
            }
            else if (Input.GetKeyDown(KeyCode.R))
            {
                ResetScene();
            }
            else if (Input.GetKeyDown(KeyCode.L))
            {
                LoadCustomInput();
            }
            else if (Input.GetKeyDown(KeyCode.H))
            {
                FlipHiding();
            }
        }
    }

    /**
     * Handles the result of using the file browser
     */
    private void LoadCustomInput()
    {
        acceptInput = false;
        Modal.SetActive(true);        
    }

    /**
     * Function to call from the modal when the buttons are pressed
     */
    public void ReturnFromModal(bool applyChanges)
    {
        Modal.SetActive(false);
        acceptInput = true;
        if (applyChanges)
        {
            DayTemplateOwner.GetComponent<DayTemplate>().textInput = CustomInputText.text;
            DayTemplateOwner.GetComponent<DayTemplate>().ResetScene();
        }
        
    }

    /**
     * Hides or unhides the group canvas that should be parent to the game object that owns this
     */
    public void FlipHiding()
    {
        if (Instructions.activeSelf) Instructions.SetActive(false);
        else Instructions.SetActive(true);
    }

    public void SwitchScene(string sceneName)
    {
        SceneManager.LoadScene(sceneName);
    }


    public void ResetScene()
    {
        DayTemplateOwner.GetComponent<DayTemplate>().ResetScene();
    }

}
