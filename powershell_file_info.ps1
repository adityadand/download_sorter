cd $env:USERPROFILE\Downloads
Get-ChildItem -File |
    Group-Object Extension |
    Select-Object Name,
                  @{Name='Count'; Expression={$_.Count}},
                  @{Name='TotalSize(MB)'; Expression={[math]::Round(($_.Group | Measure-Object Length -Sum).Sum / 1MB,2)}},
                  @{Name='AverageSize(MB)'; Expression={[math]::Round(($_.Group | Measure-Object Length -Average).Average / 1MB,2)}} |
    Sort-Object Count -Descending |
    Format-Table -AutoSize
