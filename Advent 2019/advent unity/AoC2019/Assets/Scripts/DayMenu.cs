using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

/**
 * The script for handling the generic menu shown on the top left of each day
 */
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
    [Tooltip("If the scene allows randomization of the input")]
    public bool allowRandomization = true;
    private bool acceptInput = true;

    public KeyCode menuKey = KeyCode.Q;
    public KeyCode resetKey = KeyCode.W;
    public KeyCode loadKey = KeyCode.E;
    public KeyCode randomizeKey = KeyCode.R;
    public KeyCode hideKey = KeyCode.T;

    private Vector3 FirstTouch;   //First touch position
    private Vector3 LastTouch;   //Last touch position
    private float dragDistance;  //minimum distance for a swipe to be registered

    public void Update()
    {
        if (acceptInput)
        {
            if (Input.GetKeyDown(menuKey))
            {
                BackToMenu();
            }
            else if (Input.GetKeyDown(resetKey))
            {
                ResetScene();
            }
            else if (Input.GetKeyDown(loadKey))
            {
                LoadCustomInput();
            }
            else if (Input.GetKeyDown(hideKey))
            {
                FlipHiding();
            }
            else if (Input.GetKeyDown(randomizeKey))
            {
                RandomizeInput();
            }
        }
        CheckSideSwipeForHiding();
    }

    /**
     * Switches back to the menu scene
     */
    public void BackToMenu()
    {
        SwitchScene(MenuSceneName);
    }

    /**
     * Handles the result of using the file browser
     */
    public void LoadCustomInput()
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

    /**
     * Changes to a different scene
     */
    public void SwitchScene(string sceneName)
    {
        SceneManager.LoadScene(sceneName);
    }

    /**
     * Resets the scene
     */
    public void ResetScene()
    {
        DayTemplateOwner.GetComponent<DayTemplate>().ResetScene();
    }

    /**
     * Randomizes the input data of the scene
     */
    public void RandomizeInput()
    {
        if (allowRandomization)
        {
            DayTemplateOwner.GetComponent<DayTemplate>().RandomizeInput();
            DayTemplateOwner.GetComponent<DayTemplate>().ResetScene();
        }
    }

    void Start()
    {
        string text = DayTemplateOwner.GetComponent<DayTemplate>().textInput;
        if (text != "") CustomInputText.text = text;
        dragDistance = Screen.height * 15 / 100; //dragDistance is 15% height of the screen
    }

    /**
     * Code from https://forum.unity.com/threads/simple-swipe-and-tap-mobile-input.376160/
     * Checks if a horizontal swipe motion happened to hide/show the menu
     */
    void CheckSideSwipeForHiding()
    {
        if (Input.touchCount == 1) // user is touching the screen with a single touch
        {
            Debug.Log("onetouch");
            Touch touch = Input.GetTouch(0); // get the touch
            if (touch.phase == TouchPhase.Began) //check for the first touch
            {
                FirstTouch = touch.position;
                LastTouch = touch.position;
            }
            else if (touch.phase == TouchPhase.Moved) // update the last position based on where they moved
                LastTouch = touch.position;
            else if (touch.phase == TouchPhase.Ended) //check if the finger is removed from the screen
            {
                Debug.Log("neded");
                LastTouch = touch.position;
                if (Mathf.Abs(LastTouch.x - FirstTouch.x) > dragDistance)
                {
                    if ((LastTouch.x > FirstTouch.x))  //Right swipe
                        Instructions.SetActive(true);
                    else
                        Instructions.SetActive(false);
                }
            }
        }
    }
}