using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class ExportingDataToCSV : MonoBehaviour
{
    void createCSV()
    {
        string path = Application.dataPath + "/TestingCSVExport.csv";
        if (!File.Exists(path))
        {
            Debug.Log(!File.Exists(path));
            File.WriteAllText(path, "Demo");
        }
    }
    // Start is called before the first frame update
    void Start()
    {
        createCSV();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
