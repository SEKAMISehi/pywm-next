import subprocess
import glob
import shutil
from setuptools import setup

proc = subprocess.Popen(["meson", "build"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc.communicate()
if proc.returncode != 0:
    raise Exception("Fatal: Error executing 'meson build': \n%r\n%r" % (stdout, stderr))


proc1 = subprocess.Popen(["ninja", "-C", "build"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = proc1.communicate()
if proc1.returncode != 0:
    raise Exception("Fatal: Error executing 'ninja -C build': \n%r\n%r" % (stdout, stderr))

so = None
for f in glob.glob('build/_pywm.*.so'):
    so = f

if so is not None:
    try:
        shutil.copy(so, 'pywm/_pywm.so')
    except shutil.SameFileError:
        pass
else:
    raise Exception("Fatal: Could not find shared library")

setup(name='pywm',
      version='0.3.1',
      description='wlroots-based Wayland compositor with Python frontend',
      url="https://github.com/jbuchermn/pywm",
      author='Jonas Bucher',
      author_email='j.bucher.mn@gmail.com',
      package_data={'pywm': ['_pywm.so', 'py.typed']},
      packages=['pywm'],
      install_requires=['evdev', 'imageio', 'pycairo', 'numpy'])
