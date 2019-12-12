using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class Day3 : DayTemplate
{
    [Tooltip("Colores to use for wires")]
    public Color[] WireColors;
    [Tooltip("Prefab to use for laying spool")]
    public Transform SpoolPrefab;
    [Tooltip("Prefab to use for laying wire")]
    public Transform WirePiecePrefab;
    [Tooltip("Amount of wires to randomly generate")]
    public int RandomWireCount = 2;
    [Tooltip("Segments of wires to randomly generate")]
    public int RandomWireSegments = 200;

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
                    generator.Initialize(line, i, SpoolPrefab, WirePiecePrefab, WireColors[i]);
                    WireGenerators.Add(generator);
                    i += 1;
                }
            } while (line != null);
        }
        Camera.main.orthographicSize = 50;
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
        string letters = "UDLR";
        Dictionary<char, string> possibilities = new Dictionary<char, string>();
        possibilities['U'] = "LR";
        possibilities['D'] = "LR";
        possibilities['L'] = "UD";
        possibilities['R'] = "UD";
        char[] toTrim = { ',' };
        textInput = "";
        for (int y = 0; y < RandomWireCount; y++)
        {
            char dir = '?';
            for (int x = 0; x < 200; x++)
            {
                if (dir != '?')
                {
                    dir = possibilities[dir][Random.Range(0, 2)];
                }
                else dir = letters[Random.Range(0,4)];
                textInput += dir;
                textInput += Random.Range(100, 500).ToString();
                textInput += ",";
            }
            textInput = textInput.Trim(toTrim);
            textInput += "\n";
        }
        ResetScene();
    }
}
