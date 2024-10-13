Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "win\\killClitor.bat " & WScript.Arguments(0), 0
