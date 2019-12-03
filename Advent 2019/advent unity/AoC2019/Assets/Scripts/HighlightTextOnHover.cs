using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.UI;

[RequireComponent(typeof(Text))]
public class HighlightTextOnHover : MonoBehaviour, IPointerEnterHandler, IPointerExitHandler
{
    public Color highlightColor = new Color(0.15f, 0.5f, 1f); 
    private Color defaultColor;
    private Text buttonText;

    public void Awake()
    {
        buttonText = GetComponent<Text>();
        defaultColor = buttonText.color;
    }

    public void OnPointerEnter(PointerEventData eventData)
    {
        buttonText.color = highlightColor;
    }

        public void OnPointerExit(PointerEventData eventData)
    {
        buttonText.color = defaultColor;
    }
}