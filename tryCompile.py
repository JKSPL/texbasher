import sys
import re
import subprocess
import getLatexPackage


if len(sys.argv) < 2:
  print(sys.argv[0] + " <tex file>")
  sys.exit(1)

sudoproc = subprocess.call("sudo -v", shell=True)

while True:
  sudoproc = subprocess.call("sudo -v", shell=True)
  proc = subprocess.Popen("pdflatex " + sys.argv[1], shell=True,
    stdout=subprocess.PIPE
  )
  missingPackageName = ""
  for line in iter(proc.stdout.readline,''):
    current = line.rstrip()
    

    if(current.endswith(" not found.") 
        and current.startswith("! LaTeX Error:")):
      current = current.replace('`', '\'')
      missingPackageName = current.split("\'")[1]
      break

    if(current.endswith(" not found")
        and "Font" in current):
      print current
      missingPackageName = current[current.find("Font ") + len("Font ") :
      current.rfind(" at")]
      break

    if("error" in current.lower()):
      print current
      sys.exit()

  proc.kill()

  if missingPackageName == "":
    sys.exit()
  
  print "missing: " + missingPackageName

  if not getLatexPackage.installMissing(missingPackageName):
    sys.exit()
