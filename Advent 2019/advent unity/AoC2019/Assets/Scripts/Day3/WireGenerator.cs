using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WireGenerator : MonoBehaviour
{
    private string[] Route;

    /**
     * Initializes the component
     * insutrctions is string that looks like "U23,R45,D22,R23"etc
     */
    public void Initialize(string instructions)
    {
        Route = instructions.Split(',');
    }

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
