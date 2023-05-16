using System.Collections;
using UnityEngine;
using Unity.LEGO.Minifig;

namespace Unity.LEGO.Behaviours
{
    public class MinifigInputManager : MonoBehaviour
    {
        protected MinifigController m_MinifigController;

        protected virtual void Awake()
        {
            m_MinifigController = GetComponent<MinifigController>();
        }

        IEnumerator DoUpdateInput(bool enabled)
        {
            yield return new WaitForEndOfFrame();
        }
    }
}
