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

    // Start is called before the first frame update
    void Start()
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
            Transform rocket = Instantiate(rocketPrefab);
            Rocket component = rocket.GetComponent<Rocket>();
            component.Initialize(loads[x], scaleConversion);
            component.callback = CallBack;
            rocket.position = new Vector3( 0.5f + 1.5f * x,0,0);
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

}
