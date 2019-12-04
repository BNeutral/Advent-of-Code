using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Day3 : DayTemplate
{
    private List<Transform> WireGenerators;

    void Awake()
    {
        WireGenerators = new List<Transform>();
        using (StringReader reader = new StringReader(textInput))
        {
            string line = string.Empty;
            do
            {
                line = reader.ReadLine();
                if (line != null)
                {
                    //line.Split(",");
                    //loads.Add(mass);
                    //maxLoad = Mathf.Max(maxLoad, mass);
                }

            } while (line != null);
        }
    }

    void CallBack()
    {

    }
    public override void ResetScene()
    {
        foreach (Transform wire in WireGenerators)
        {
            Destroy(wire.gameObject);
        }
        Awake();
    }

    public override void RandomizeInput()
    {
        textInput = "";
        for (int x = 0; x < 5; x++)
        {
            textInput += Random.Range(30000, 120000).ToString();
            textInput += "\n";
        }
    }
}
