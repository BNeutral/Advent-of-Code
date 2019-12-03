using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class Day1 : DayTemplate
{
    [Tooltip("Text file to use as input if provided at runtime")]
    public static string inputFilePath;
    [Tooltip("Prefab for rockets. Should have a Rocket component.")]
    public Transform rocketPrefab;
    [Tooltip("How many unity length units for the biggest ship?")]
    public float unitsForMaxLoad;
    private List<int> loads;
    private List<Transform> rockets;
    private int rocketsReady;

    void Awake()
    {
        rockets = new List<Transform>();
        loads = new List<int>();
        int maxLoad = 0;
        using (StringReader reader = new StringReader(getText()))
        {
            string line = string.Empty;
            do
            {
                line = reader.ReadLine();
                if (line != null)
                {
                    int mass = int.Parse(line);
                    loads.Add(mass);
                    maxLoad = Mathf.Max(maxLoad, mass);
                }

            } while (line != null);
        }
        float scaleConversion = unitsForMaxLoad / maxLoad;
        for (int x = 0; x < loads.Count; ++x)
        {
            Transform rocket = Instantiate(rocketPrefab, new Vector3(0.5f + 1.5f * x, 0, 0), Quaternion.identity);
            Rocket component = rocket.GetComponent<Rocket>();
            component.Initialize(loads[x], scaleConversion);
            component.callback = CallBack;
            rockets.Add(rocket);
        }
    }

    void CallBack()
    {
        rocketsReady += 1;
        if (rocketsReady >= rockets.Count)
        {
            foreach (Transform rocket in rockets){
                rocket.GetComponent<Rocket>().launch();
            }
        }
    }
    public override void ResetScene()
    {
        foreach(Transform rocket in rockets)
        {
            Destroy(rocket.gameObject);
        }
        Awake();
    }

    public override void RandomizeInput()
    {
        textInput = "";

        for (int x = 0; x < rockets.Count; x++)
        {
            textInput += Random.Range(30000, 120000).ToString();
            textInput += "\n";
        }
    }
}
