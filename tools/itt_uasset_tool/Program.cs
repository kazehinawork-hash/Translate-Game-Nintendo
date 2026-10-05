using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UAssetAPI;
using UAssetAPI.UnrealTypes;

class Conv
{
    static UAsset Load(string path, long ver = 522)
    {
        var ovType = typeof(ObjectVersion);
        var byVal = new Dictionary<long, string>();
        foreach (var n in Enum.GetNames(ovType)) byVal[Convert.ToInt64(Enum.Parse(ovType, n))] = n;
        var objV = (ObjectVersion)Enum.Parse(ovType, byVal[ver]);
        var objV5 = (ObjectVersionUE5)Enum.Parse(typeof(ObjectVersionUE5), Enum.GetNames(typeof(ObjectVersionUE5)).First());
        return new UAsset(path, objV, objV5, new List<CustomVersion>(), null, CustomSerializationFlags.None);
    }

    static void Main(string[] argv)
    {
        string path = @"E:\ITT_work\ST_UTG_MenuLabels.uasset";
        var asset = Load(path);
        string json = asset.SerializeJson(Newtonsoft.Json.Formatting.Indented);
        var lines = json.Split('\n').Where(l => l.Contains("\"Value\":") || l.Contains("Key:") || l.Contains("EULA") || l.Contains("accept")).Take(30);
        Console.WriteLine("=== vai dong JSON co chu ===");
        foreach (var l in lines) Console.WriteLine("  " + l.Trim().Substring(0, Math.Min(150, l.Trim().Length)));

        // ROUNDTRIP: ghi lai roi doc lai, so sanh
        string outPath = @"E:\ITT_work\rt_test.uasset";
        try
        {
            asset.Write(outPath);
            long a = new FileInfo(path).Length;
            long b = new FileInfo(outPath).Length;
            var again = Load(outPath);
            string json2 = again.SerializeJson(Newtonsoft.Json.Formatting.Indented);
            Console.WriteLine($"\n=== ROUNDTRIP ===");
            Console.WriteLine($"  goc {a:N0} byte -> ghi lai {b:N0} byte | lech {Math.Abs(a-b):N0}");
            Console.WriteLine($"  JSON trung nhau: {json == json2}");
        }
        catch (Exception ex)
        {
            Console.WriteLine("  LOI ghi: " + ex.GetType().Name + ": " + ex.Message);
        }
    }
}
