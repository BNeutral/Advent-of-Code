using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rocket : MonoBehaviour
{
    private Transform root;
    private Transform fuelTransform;
    private Transform loadTranform;   
    private int mass;
    private int fuel;
    private bool liftoff;
    public float velocity;
    public float liftoffDelay;
    

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        if (Time.realtimeSinceStartup > liftoffDelay)
        {
            float newY = root.localPosition.y + velocity * Time.deltaTime;
            root.localPosition = new Vector3(root.localPosition.x, newY, root.localPosition.z);
        }
    }

    /**
     * Initializes the object. Assumes it's being attached to a rocket prefab
     */
    public void Initialize(int mass, float scaleConversion)
    {
        this.mass = mass;
        StartCoroutine("Refuel",scaleConversion);
    }

    /**
     * Performs the secuential fuel loading
     */
    private IEnumerator Refuel(float scaleConversion)
    {
        root = this.GetComponentInParent<Transform>();
        fuelTransform = root.GetChild(0);
        loadTranform = root.GetChild(1);
        loadTranform.localScale = new Vector3(1, mass * scaleConversion, 1);
        fuel = 0;
        int nextFuel = CalculateFuel(mass);
        yield return new WaitForSeconds(5f);
        while (nextFuel > 0)
        {
            fuel += nextFuel;
            AdjustScales(fuel, scaleConversion);
            nextFuel = CalculateFuel(nextFuel);
            yield return new WaitForSeconds(0.5f);
        }
    }

    /**
     * Adjust the scaling based on new fuel data
     */
    private void AdjustScales(int fuel, float scaleConversion)
    {
        this.fuelTransform.localScale = new Vector3(1, fuel * scaleConversion, 1);
        this.loadTranform.localPosition = new Vector3(0, fuel * scaleConversion, 0);
    }

    /**
     * Given a mass calculates the fuel needed to lift it
     */
    private int CalculateFuel(int mass)
    {
        return (mass / 3 - 2);
    }

}
