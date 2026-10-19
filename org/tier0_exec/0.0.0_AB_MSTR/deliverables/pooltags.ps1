param([int]$WaitSec = 60, [int]$Top = 12)
Add-Type -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public static class PoolTags {
  [DllImport("ntdll.dll")] static extern int NtQuerySystemInformation(int cls, IntPtr buf, int len, out int ret);
  public class Row { public string Tag; public long PagedUsed, NonPagedUsed; public uint PagedAllocs, PagedFrees; }
  public static Dictionary<string,Row> Read(out int status) {
    int size = 1 << 20, ret; IntPtr p = IntPtr.Zero; status = 0;
    for (int i = 0; i < 12; i++) {
      p = Marshal.AllocHGlobal(size);
      status = NtQuerySystemInformation(22, p, size, out ret);
      if (status == unchecked((int)0xC0000004)) { Marshal.FreeHGlobal(p); size = Math.Max(size * 2, ret + 65536); continue; }
      break;
    }
    var d = new Dictionary<string,Row>();
    if (status != 0) { Marshal.FreeHGlobal(p); return d; }
    int n = Marshal.ReadInt32(p);
    long off = 8;
    for (int i = 0; i < n; i++) {
      byte[] t = new byte[4]; Marshal.Copy(new IntPtr(p.ToInt64() + off), t, 0, 4);
      var r = new Row();
      r.Tag = System.Text.Encoding.ASCII.GetString(t);
      r.PagedAllocs = (uint)Marshal.ReadInt32(p, (int)off + 4);
      r.PagedFrees  = (uint)Marshal.ReadInt32(p, (int)off + 8);
      r.PagedUsed   = Marshal.ReadInt64(p, (int)off + 16);
      r.NonPagedUsed = Marshal.ReadInt64(p, (int)off + 32);
      d[r.Tag] = r;
      off += 40;
    }
    Marshal.FreeHGlobal(p);
    return d;
  }
}
'@
$s1 = 0; $a = [PoolTags]::Read([ref]$s1)
"status1=0x{0:X8} tags={1}" -f $s1, $a.Count
if ($s1 -ne 0) { exit 3 }
"paged total at t0 MB: {0:N0}" -f (($a.Values | Measure-Object PagedUsed -Sum).Sum / 1MB)
Start-Sleep -Seconds $WaitSec
$s2 = 0; $b = [PoolTags]::Read([ref]$s2)
"status2=0x{0:X8} tags={1}" -f $s2, $b.Count
"paged total at t1 MB: {0:N0}" -f (($b.Values | Measure-Object PagedUsed -Sum).Sum / 1MB)
"--- top PAGED by size at t1 (MB), with delta over $WaitSec s (MB) ---"
$b.Values | Sort-Object PagedUsed -Descending | Select-Object -First $Top | ForEach-Object {
  $prev = if ($a.ContainsKey($_.Tag)) { $a[$_.Tag].PagedUsed } else { 0 }
  "{0}  {1,9:N1} MB  delta {2,8:N2} MB  allocs-frees {3}" -f $_.Tag, ($_.PagedUsed/1MB), (($_.PagedUsed-$prev)/1MB), ([int64]$_.PagedAllocs - [int64]$_.PagedFrees)
}
"--- fastest-growing PAGED tags over the window ---"
$b.Values | ForEach-Object { $prev = if ($a.ContainsKey($_.Tag)) { $a[$_.Tag].PagedUsed } else { 0 }; [pscustomobject]@{Tag=$_.Tag; DeltaMB=($_.PagedUsed-$prev)/1MB; MB=$_.PagedUsed/1MB} } |
  Sort-Object DeltaMB -Descending | Select-Object -First 5 | ForEach-Object { "{0}  delta {1:N2} MB  now {2:N1} MB" -f $_.Tag, $_.DeltaMB, $_.MB }
