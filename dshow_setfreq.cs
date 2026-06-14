using System;
using System.Runtime.InteropServices;

class Program {
    [DllImport("ole32.dll")]
    static extern int CoCreateInstance(ref Guid rclsid, IntPtr pUnkOuter, int dwClsCtx, ref Guid riid, out IntPtr ppv);

    [DllImport("ole32.dll")]
    static extern int CoInitialize(IntPtr pvReserved);

    [DllImport("ole32.dll")]
    static extern void CoUninitialize();

    static Guid CLSID_SystemDeviceEnum = new Guid("860BB310-5D01-11D0-BD3B-00A0C911CE86");
    static Guid CLSID_VideoInputDeviceCategory = new Guid("8E14549A-DB91-43D6-957B-53597EB1ABDC");
    static Guid IID_ICreateDevEnum = new Guid("29840822-5B84-11D0-BD3B-00A0C911CE86");
    static Guid IID_IEnumMoniker = new Guid("55272A00-42CB-11CE-8135-00AA004BB851");
    static Guid IID_IMoniker = new Guid("0000000F-0000-0000-C000-000000000046");
    static Guid IID_IBaseFilter = new Guid("56A86895-0AD4-11CE-B03A-0020AF0BA770");
    static Guid IID_IAMVideoProcAmp = new Guid("C6E13370-36AC-11D2-B40E-006008798020");

    [ComImport, Guid("29840822-5B84-11D0-BD3B-00A0C911CE86")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface ICreateDevEnum {
        [PreserveSig] int CreateClassEnumerator(ref Guid clsidDeviceClass, out IEnumMoniker ppEnumMoniker, int dwFlags);
    }

    [ComImport, Guid("55272A00-42CB-11CE-8135-00AA004BB851")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IEnumMoniker {
        [PreserveSig] int Next(int celt, [MarshalAs(UnmanagedType.LPArray, SizeParamIndex=0)] IMoniker[] rgelt, out int pceltFetched);
        [PreserveSig] int Skip(int celt);
        [PreserveSig] int Reset();
        [PreserveSig] int Clone(out IEnumMoniker ppEnum);
    }

    [ComImport, Guid("0000000F-0000-0000-C000-000000000046")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IMoniker {
        [PreserveSig] int BindToObject(IntPtr pbc, IntPtr pmkToLeft, ref Guid riidResult, out IntPtr ppvResult);
        [PreserveSig] int BindToStorage(IntPtr pbc, IntPtr pmkToLeft, ref Guid riid, out IntPtr ppvObj);
    }

    [ComImport, Guid("C6E13370-36AC-11D2-B40E-006008798020")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    interface IAMVideoProcAmp {
        [PreserveSig] int GetRange(int Property, out int pMin, out int pMax, out int pSteppingDelta, out int pDefault, out int pCapsFlags);
        [PreserveSig] int Get(int Property, out int lValue, out int Flags);
        [PreserveSig] int Set(int Property, int lValue, int Flags);
    }

    static int Main(string[] args) {
        if (args.Length < 1) return 1;
        int freq = int.Parse(args[0]);

        CoInitialize(IntPtr.Zero);
        try {
            Guid clsid = CLSID_SystemDeviceEnum;
            Guid iid = IID_ICreateDevEnum;
            IntPtr devEnumPtr = IntPtr.Zero;
            int hr = CoCreateInstance(ref clsid, IntPtr.Zero, 1, ref iid, out devEnumPtr);
            if (hr != 0 || devEnumPtr == IntPtr.Zero) return 1;

            ICreateDevEnum devEnum = (ICreateDevEnum)Marshal.GetObjectForIUnknown(devEnumPtr);

            IEnumMoniker enumMon;
            hr = devEnum.CreateClassEnumerator(ref CLSID_VideoInputDeviceCategory, out enumMon, 0);
            if (hr != 0 || enumMon == null) return 1;

            IMoniker[] monikers = new IMoniker[1];
            int fetched;
            bool success = false;

            while (true) {
                hr = enumMon.Next(1, monikers, out fetched);
                if (hr != 0 || fetched == 0) break;

                IMoniker mon = monikers[0];
                try {
                    IntPtr filterPtr = IntPtr.Zero;
                    Guid filterIid = IID_IBaseFilter;
                    hr = mon.BindToObject(IntPtr.Zero, IntPtr.Zero, ref filterIid, out filterPtr);

                    if (hr == 0 && filterPtr != IntPtr.Zero) {
                        IntPtr ampPtr;
                        Guid ampIid = IID_IAMVideoProcAmp;
                        hr = Marshal.QueryInterface(filterPtr, ref ampIid, out ampPtr);

                        if (hr == 0 && ampPtr != IntPtr.Zero) {
                            IAMVideoProcAmp amp = (IAMVideoProcAmp)Marshal.GetObjectForIUnknown(ampPtr);
                            amp.Set(14, freq, 0);
                            success = true;
                            Marshal.ReleaseComObject(amp);
                        }
                        Marshal.Release(filterPtr);
                    }
                } catch (Exception) {}
            }

            Marshal.ReleaseComObject(enumMon);
            return success ? 0 : 1;
        } finally {
            CoUninitialize();
        }
    }
}
