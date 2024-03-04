from distutils.core import setup
import py2exe

version = "1.1.0"
version_name = "AIU_" + version

icon_path = "AIU-Iconv3.2.2.ico"

setup(
    windows = [
        {
            "script": version_name + ".py", # main python script
            "icon_resources": [(1, icon_path)], # icon to emebed into the PE file
            "dest_base": version_name # output file name
        }
    ],
)