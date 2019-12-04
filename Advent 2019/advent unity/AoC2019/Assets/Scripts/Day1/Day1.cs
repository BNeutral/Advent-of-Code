using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class Day1 : DayTemplate
{
    [Tooltip("Prefab for rockets. Should have a Rocket component.")]
    public Transform RocketPrefab;
    [Tooltip("How many unity length units for the biggest ship?")]
    public float UnitsForMaxLoad;
    private List<int> Loads;
    private List<Transform> Rockets;
    private int RocketsReady;

    void Awake()
    {
        base.Awake();
        Rockets = new List<Transform>();
        Loads = new List<int>();
        int maxLoad = 0;
        using (StringReader reader = new StringReader(textInput))
        {
            string line = string.Empty;
            do
            {
                line = reader.ReadLine();
                if (line != null)
                {
                    int mass = int.Parse(line);
                    Loads.Add(mass);
                    maxLoad = Mathf.Max(maxLoad, mass);
                }

            } while (line != null);
        }
        float scaleConversion = UnitsForMaxLoad / maxLoad;
        for (int x = 0; x < Loads.Count; ++x)
        {
            Transform rocket = Instantiate(RocketPrefab, new Vector3(0.5f + 1.5f * x, 0, 0), Quaternion.identity);
            Rocket component = rocket.GetComponent<Rocket>();
            component.Initialize(Loads[x], scaleConversion);
            component.callback = CallBack;
            Rockets.Add(rocket);
        }
    }

    void CallBack()
    {
        RocketsReady += 1;
        if (RocketsReady >= Rockets.Count)
        {
            foreach (Transform rocket in Rockets){
                rocket.GetComponent<Rocket>().launch();
            }
        }
    }
    public override void ResetScene()
    {
        foreach(Transform rocket in Rockets)
        {
            Destroy(rocket.gameObject);
        }
        Awake();
    }

    public override void RandomizeInput()
    {
        textInput = "";

        for (int x = 0; x < Rockets.Count; x++)
        {
            textInput += Random.Range(30000, 120000).ToString();
            textInput += "\n";
        }
    }
}
