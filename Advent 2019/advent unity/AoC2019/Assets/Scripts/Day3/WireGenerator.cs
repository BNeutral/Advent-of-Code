using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WireGenerator : MonoBehaviour
{
    [Tooltip("Color to assign to the wire pieces on creation")]
    public Color WireColor;

    //"Prefab to use for laying spool"
    private Transform SpoolPrefab;
    //"Prefab to use for laying wire"
    public Transform WirePiecePrefab;
    //Id of the wiregenerator
    private int id;
    //Array detailing how to lay the wire
    private string[] Route;
    //Wire laid out so far
    private List<Transform> pieces;
    //For storing the last piece place
    private Vector2 position;

    private float delay = 0f; 

    private static Quaternion Vertical =  Quaternion.Euler(90,-90,90);
    private static Quaternion Horizontal = Quaternion.Euler(0,-90,90);
    private static Dictionary<char, Vector2> directions = new Dictionary<char, Vector2>{
        {'U', Vector2.up},
        {'D', Vector2.down},
        {'L', Vector2.left},
        {'R', Vector2.right}
    };

    /**
     * Initializes the component
     * insutrctions is string that looks like "U23,R45,D22,R23"etc
     */
    public void Initialize(string instructions, int id, Transform SpoolPrefab, Transform WirePiecePrefab)
    {
        this.SpoolPrefab = SpoolPrefab;
        this.WirePiecePrefab = WirePiecePrefab;
        pieces = new List<Transform>();
        Route = instructions.Split(',');
        this.id = id;
        StartCoroutine("LayAllWire");
        position = Vector2.zero;
        WireColor = id == 1 ? Color.grey : Color.yellow;
    }

    /**
     * Lays down the wire according to the input received
     */
    private IEnumerator LayAllWire()
    {
        foreach (string segment in Route)
        {
            Vector2 dir = directions[segment[0]];
            bool rotate = (dir == Vector2.right || dir == Vector2.left);
            int steps = int.Parse(segment.Substring(1));
            laySpool(position);
            layWirePiece(position+(dir*steps/2), steps-30, rotate);
            position += dir * steps;
            laySpool(position);
            yield return new WaitForSeconds(delay);
        }
    }


    private void layWirePiece(Vector3 position, float length = 1f, bool rotate = false)
    {
        position.z += id;
        Transform wire = Instantiate(WirePiecePrefab, position, rotate ? Horizontal : Vertical);
        wire.localScale = new Vector3(10, 1, length / 10);
        Material material = wire.gameObject.GetComponent<Renderer>().material;
        material.SetColor("_BaseColor", WireColor);
        Vector2 scaling = new Vector2(1f, length/100);
        material.SetTextureScale("_BumpMap", scaling);
        material.SetTextureScale("_BaseMap", scaling);
        pieces.Add(wire);
    }

    private void laySpool(Vector3 position)
    {
        position.z += id - 0.5f;
        Transform spool = Instantiate(SpoolPrefab, position, Vertical);
        Material material = spool.gameObject.GetComponent<Renderer>().material;
        material.SetColor("_BaseColor", WireColor);
        pieces.Add(spool);
    }

    private void OnDestroy()
    {
        foreach (Transform piece in pieces)
        {
            Destroy(piece);
        }
    }
}
