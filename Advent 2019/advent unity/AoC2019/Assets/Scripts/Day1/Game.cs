using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

public class Game : MonoBehaviour
{
    public TextAsset inputFile;
    public Transform rocketPrefab;
    public float unitsForMaxLoad;
    private List<int> loads;


    // Start is called before the first frame update
    void Start()
    {
        loads = new List<int>();
        int maxLoad = 0;
        using (StringReader reader = new StringReader(inputFile.text))
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
            rocket.GetComponent<Rocket>().Initialize(loads[x], scaleConversion);
            rocket.position = new Vector3( 0.5f + 1.5f * x,0,0);
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }

}
