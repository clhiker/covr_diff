import os
import subprocess

for name in os.listdir("/home/clhiker/smt_random"):
    path = os.path.join("/home/clhiker/smt_random", name)
    subprocess.run(['/home/clhiker/z3/build/z3', path])