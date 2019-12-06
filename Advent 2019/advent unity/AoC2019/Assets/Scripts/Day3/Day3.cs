using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Day3 : DayTemplate
{
    [Tooltip("Prefab to use for laying spool")]
    public Transform SpoolPrefab;
    [Tooltip("Prefab to use for laying wire")]
    public Transform WirePiecePrefab;

    private List<WireGenerator> WireGenerators;

    new void Awake()
    {
        base.Awake();
        WireGenerators = new List<WireGenerator>();
        using (StringReader reader = new StringReader(textInput))
        {
            string line = string.Empty;
            int i = 0;
            do
            {
                line = reader.ReadLine();
                Debug.Log(line);
                if (line != null)
                {
                    WireGenerator generator = gameObject.AddComponent(typeof(WireGenerator)) as WireGenerator;
                    generator.Initialize(line, i, SpoolPrefab, WirePiecePrefab);
                    WireGenerators.Add(generator);
                    i += 1;
                }
            } while (line != null);
        }
    }

    /**
     * Callback function for WireGenerators to call after putting down a piece of wire
     */
    void LayWireCallback(int x, int y, int id)
    {

    }

    public override void ResetScene()
    {
        foreach (WireGenerator wire in WireGenerators)
        {
            Destroy(wire);
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
