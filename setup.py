import os
from setuptools import setup, find_packages
from setuptools.command.develop import develop

namespace = ""

if [True for d in os.listdir(os.path.dirname(os.sys.executable)) if d.lower() == "lib"]:
    PYDIR = os.path.dirname(os.sys.executable)  ;# global python
else:
    PYDIR = os.path.dirname(os.path.dirname(os.sys.executable)) ;# virtualenv
SITEPKGS = os.path.join(PYDIR, "lib", "site-packages")

if namespace:
    __import__("pkg_resources").declare_namespace(namespace)

__version__ = "0.0.0" 

# -- Edit Start
zip_safe = False

easy_installs = []

modules = []

dependencies = ["pyaml",
                "neo4j-driver",
                "neomodel",
                "pandas",
                "psycopg2"]

dependency_links = []

entry_points = {
    "console_scripts": []
}
# -- Edit Stop

# Post develop hook
class CustomDevelop(develop):
    def run(self):
        develop.run(self)
        self.run_command(self._post_develop())
    
    def _post_develop(*args):
        # When installing a namespace package using 'python setup.py develop'
        # adjacent to other packages which are installed normally 
        # (e.g. python setup.py install | pip install <pkg>) then the 'develop'
        # install will fail with the package load failing.
        # This appears to be due to the fact that *develop* installs use an egg.link 
        # whilst normal installations use an *nspkg.pth* helper.
        # Currently appears that no side effects should exist since we use the *__init__* 
        # namespace helper during development anyway...essentially all seems a bit broken
        # but it this is well acknowledged in the community.
        # 
        # To resolve this we will recreate the *__init__* file for development installs only
        # where there is a namespace match
        # Further info:
        #   https://github.com/pypa/pip/issues/3
        #   http://stackoverflow.com/questions/13400291/namespace-packages-and-pip-install-e
        #   http://mail.python.org/pipermail/distutils-sig/2005-August/004970.html
        #   http://www.python.org/dev/peps/pep-0420/#differences-between-namespace-packages-and-regular-packages
        if namespace:
            # Note, this is currently non-recursive but we may need to traverse 
            # and update the directory __init__ which is *not* preferable in this instance
            ns = namespace.split(".")[0]
            fn = os.path.join(SITEPKGS, ns)
            # Write a new NS __init__ file 
            if os.path.exists(fn):
                fh = open(fn + "/__init__.py", "w")
                fh.write("""# NAMESPACE PACKAGE - DO NOT EDIT\n__import__("pkg_resources").declare_namespace("%s")""" % ns)
                fh.close()
                print "Installed namespace __init__ file for 'develop'"
            else:
                print "No namespace package currently installed...", \
                      "\nYou may need to re-run 'setup.py develop' again", \
                      "if you have installed a related namespace package..."
        print "Completed post develop install tasks"
        exit()
        
command_class = {"develop": CustomDevelop}

# Easy Installs
for install in easy_installs:
    subprocess.call("easy_install -d %s %s" % (SITEPKGS, install))

    
setup(
    name="utm",
    version=__version__,
    description="",
    author="analyticsandplanning",
    author_email="dl-analyticsandplanning-broadband@bskyb.internal",
    packages=find_packages(),
    py_modules=modules,
    include_package_data=True,
    install_requires=dependencies,
    dependency_links=dependency_links,
    zip_safe=zip_safe,
    entry_points=entry_points
)