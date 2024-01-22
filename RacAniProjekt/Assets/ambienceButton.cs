using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ambienceButton : MonoBehaviour
{
    public void ChangeSkybox(Material ski)
    {
        RenderSettings.skybox = ski;
    }

    public void ChangeMat(Material mat)
    {
        foreach (GameObject obj in GameObject.FindGameObjectsWithTag("Floor"))
        {
            obj.GetComponent<MeshRenderer>().material = mat;
        }
    }

    public void ChangeParticles()
    {
        var emission = GameObject.Find("Particles").GetComponent<ParticleSystem>().emission;
        emission.rateOverTime = GameObject.Find("Weather intensity").GetComponent<Slider>().value;
    }
}
