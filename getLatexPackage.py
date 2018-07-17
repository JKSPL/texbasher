import fileinput
import sys
import subprocess
if len(sys.argv) < 2 :
  print(sys.argv[0] + " <name of file>")
  sys.exit()

def findPackageName(plik, output):
  label = ""
  second = ""
  for line in output.splitlines():
    if line.endswith(":"):
      label = line[:-1]
    if line.endswith(plik) and label != "":
      return label
    if plik in line:
      second = label
  return second

def installMissing(pack):
  plik = "/" + pack
  output = subprocess.check_output(
    "tlmgr --no-persistent-downloads search --global --file " +
    plik, shell=True 
  )
  pkgName = findPackageName(plik, output)
  if pkgName == "":
    print("didn't find the package")
    return False

  print("Found package " + pkgName)
  subprocess.call("sudo -v", shell=True)

  subprocess.call("sudo tlmgr --no-persistent-downloads install "
    + pkgName, shell=True
  )
  return True
