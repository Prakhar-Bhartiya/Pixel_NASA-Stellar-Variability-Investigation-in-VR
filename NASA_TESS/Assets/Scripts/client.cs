using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;
using UnityEngine.UI;


public class client : MonoBehaviour
{
    [SerializeField] TextMeshProUGUI textOut;
    [SerializeField] RawImage imgOut;
    public string url_text;
    public string url_img;
    public void GetData() => StartCoroutine(GetData_corroutine(url_text));

    IEnumerator GetData_corroutine(string MediaUrl) 
    {
        textOut.text = "Loading ........";
        using(UnityWebRequest request = UnityWebRequest.Get(MediaUrl))
        {
            yield return request.SendWebRequest();
            if(request.isNetworkError || request.isHttpError)
            {
                textOut.text = request.error;
            }
            else
            {
                //Succecss 
                textOut.text = request.downloadHandler.text;
            }
        }

    }


    public void GetImage() => StartCoroutine(DownloadImage(url_img));

    IEnumerator DownloadImage(string MediaUrl)
    {
        textOut.text = "Loading ........";
        UnityWebRequest request = UnityWebRequestTexture.GetTexture(MediaUrl);
        yield return request.SendWebRequest();
        if (request.isNetworkError || request.isHttpError)
        {
            textOut.text = request.error;
        }
        else
        {
            textOut.text = "";
            imgOut.texture = ((DownloadHandlerTexture)request.downloadHandler).texture;
        }
    }

}
