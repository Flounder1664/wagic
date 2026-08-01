# Push G:\Wagic-windows\User\sets\* image bundles to an Android device's
# /storage/<UUID>/Wagic/User/sets/ path (public SD card root, requires MANAGE_EXTERNAL_STORAGE).
#
# Safe to resume — for each set on PC, compares per-file sizes against the
# device and re-pushes the whole set dir if anything is missing or different.
# Skips already-matching sets, so subsequent runs are cheap.
#
# Usage:
#   .\push_sets_to_device.ps1 -Serial R52X10ACZCW -SdUuid 0449-B4A1     # S9
#   .\push_sets_to_device.ps1 -Serial d15e0854   -SdUuid 3963-3235      # RP5
#
# Optional:
#   -SrcRoot   custom source root (default G:\Wagic-windows\User\sets)
#   -DryRun    list what would be pushed, push nothing
#   -OnlySets  comma-separated whitelist (e.g. -OnlySets ALL,DSK,ECL)

param(
    [Parameter(Mandatory=$true)] [string]$Serial,
    [Parameter(Mandatory=$true)] [string]$SdUuid,
    [string]$SrcRoot = 'G:\Wagic-windows\User\sets',
    [switch]$DryRun,
    [string]$OnlySets = ''
)

$adb = 'C:\Android-SDK\platform-tools\adb.exe'
$dst = "/storage/$SdUuid/Wagic/User/sets/"

if (-not (Test-Path $adb))     { throw "adb not found at $adb" }
if (-not (Test-Path $SrcRoot)) { throw "source not found at $SrcRoot" }

# Confirm device is reachable
$devices = & $adb devices
if (-not ($devices -match $Serial)) {
    throw "Device $Serial not in 'adb devices'. Plug it in / authorize USB debugging."
}

# Pull whole-tree listing in ONE shell call (much faster than per-set ls)
Write-Host "Inventorying device $Serial..."
$listOutput = & $adb -s $Serial shell "find $dst -maxdepth 2 -type f -printf '%P %s\n' 2>/dev/null"
$deviceFiles = @{}  # key = "SET/filename", value = size
foreach ($line in ($listOutput -split "`n")) {
    $line = $line.Trim()
    if (-not $line) { continue }
    $parts = $line -split ' '
    if ($parts.Count -lt 2) { continue }
    $path = $parts[0..($parts.Count-2)] -join ' '
    $size = [int64]$parts[-1]
    $deviceFiles[$path] = $size
}
Write-Host "  Device has $($deviceFiles.Count) files under User/sets/"

# Build PC inventory
$pcSets = Get-ChildItem $SrcRoot -Directory | Where-Object { $_.Name -ne 'primitives' } | Sort-Object Name
if ($OnlySets) {
    $whitelist = $OnlySets -split ',' | ForEach-Object { $_.Trim() }
    $pcSets = $pcSets | Where-Object { $_.Name -in $whitelist }
    Write-Host "Filtered to $($pcSets.Count) sets: $($pcSets.Name -join ', ')"
}

$toPush = @()
$alreadyOk = 0
foreach ($d in $pcSets) {
    $localFiles = Get-ChildItem $d.FullName -File
    $needsPush = $false
    foreach ($lf in $localFiles) {
        $key = "$($d.Name)/$($lf.Name)"
        if (-not $deviceFiles.ContainsKey($key) -or $deviceFiles[$key] -ne $lf.Length) {
            $needsPush = $true
            break
        }
    }
    if ($needsPush) { $toPush += $d } else { $alreadyOk++ }
}

$totalBytes = ($toPush | ForEach-Object { (Get-ChildItem $_.FullName -File | Measure-Object Length -Sum).Sum } | Measure-Object -Sum).Sum
Write-Host "$alreadyOk sets already match (skip), $($toPush.Count) need push, $('{0:N0}' -f ($totalBytes/1MB)) MB to transfer"

if ($DryRun) {
    Write-Host "DRY-RUN. Would push:"
    $toPush | ForEach-Object { Write-Host "  $($_.Name)" }
    return
}

if ($toPush.Count -eq 0) { Write-Host "Nothing to do."; return }

$startedAt = Get-Date
$pushed = 0
$pushedBytes = 0L
$failed = @()
foreach ($d in $toPush) {
    $output = & $adb -s $Serial push $d.FullName $dst 2>&1
    if ($LASTEXITCODE -ne 0) {
        $failed += $d.Name
        Write-Host "FAIL: $($d.Name)"
        Write-Host ($output | Select-Object -Last 3 | Out-String)
    } else {
        $size = (Get-ChildItem $d.FullName -File | Measure-Object Length -Sum).Sum
        $pushedBytes += $size
        $pushed++
        if ($pushed % 10 -eq 0 -or $pushed -eq $toPush.Count) {
            $elapsed = (Get-Date) - $startedAt
            $mbps = if ($elapsed.TotalSeconds -gt 0) { ($pushedBytes/1MB)/$elapsed.TotalSeconds } else { 0 }
            $pct = [math]::Round(100 * $pushed / $toPush.Count, 1)
            Write-Host ("[{0,3}/{1}] {2,-8} {3:N0} MB @ {4:N1} MB/s, {5:mm\:ss} elapsed, {6}%" -f $pushed, $toPush.Count, $d.Name, ($pushedBytes/1MB), $mbps, $pct)
        }
    }
}
$elapsed = (Get-Date) - $startedAt
Write-Host "---"
Write-Host ("DONE: {0} pushed, {1} failed, {2:N0} MB in {3:hh\:mm\:ss}" -f $pushed, $failed.Count, ($pushedBytes/1MB), $elapsed)
if ($failed.Count -gt 0) {
    Write-Host "FAILED: $($failed -join ', ')"
    Write-Host "Re-run the same command to retry just the failed/partial sets."
}
