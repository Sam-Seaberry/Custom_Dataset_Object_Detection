"""
A simple setup script to create an executable using PyQt5. This also
demonstrates the method for creating a Windows executable that does not have
an associated console.

test_pyqt5.py is a very simple type of PyQt5 application

Run the build process by running the command 'python setup.py build'

If everything works well you should find a subdirectory in the build
subdirectory that contains the files needed to run the application
"""

from __future__ import annotations

import sys

from cx_Freeze import Executable, setup

try:
    from cx_Freeze.hooks import get_qt_plugins_paths
except ImportError:
    get_qt_plugins_paths = None


#include_files = ['../res/icons/icon.ico', '../Object_Detection_Help_Guide.pdf', '../res/pages/ObjDet.ui', '../res/icons/tensorflow_icon.ico',
#                 '../res/pages/help_viewer.ui','../res/pages/eval_dialog.ui', '../res/pages/createproj.ui','C:/Users/andrew/Documents/Programming/tensorflow/', 
#                 'C:/Users/andrew/Documents/Ext/Gui2/protoc/', "../res/pages/install.ui","C:/Users/andrew/Documents/Ext/Gui2/nvvm/",
#                  '../res/pages/About.ui' ]

include_files = ['../res', '../Object_Detection_Help_Guide.pdf',
                 'C:/Users/andrew/Documents/Programming/tensorflow/', 
                 'C:/Users/andrew/Documents/Ext/Gui2/protoc/', "C:/Users/andrew/Documents/Ext/Gui2/nvvm/" ]
if get_qt_plugins_paths:
    # Inclusion of extra plugins (since cx_Freeze 6.8b2)
    # cx_Freeze imports automatically the following plugins depending of the
    # use of some modules:
    # imageformats, platforms, platformthemes, styles - QtGui
    # mediaservice - QtMultimedia
    # printsupport - QtPrintSupport
    for plugin_name in (
        # "accessible",
        # "iconengines",
        # "platforminputcontexts",
        # "xcbglintegrations",
        # "egldeviceintegrations",
        "wayland-decoration-client",
        "wayland-graphics-integration-client",
        # "wayland-graphics-integration-server",
        "wayland-shell-integration",
    ):
        include_files += get_qt_plugins_paths("PyQt5", plugin_name)

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None
packages = ["PyQt5", "cv2", "os", "sys", "matplotlib.figure", "matplotlib.backends.backend_qt5agg", 
                 "numpy", "PyQt5.QtGui", "PyQt5.QtCore", "PyQt5.QtWidgets", "matplotlib", "pandas", 
                 "sklearn.model_selection", "tensorflow", "queue", "threading", "subprocess", "signal",
                 "time", "io", "tf_slim", "shutil", "PIL", "random", "logging", "object_detection",
                 "csv", "fnmatch", "winreg", "absl", "traceback", "tensorflow_io", 'avro',
                 'apache_beam','lxml', 'Cython', 'contextlib2','six','pycocotools', 'lvis',
                 'scipy','pandas','official', 'orbit', 'tensorflow_models','keras','pyparsing', 
                 'sacrebleu']
build_exe_options = {
    # exclude packages that are not really needed
    "include_files": include_files,
    "zip_include_packages": ["PyQt5"],
    "includes": ["PyQt5", "cv2", "os", "sys", "matplotlib.figure", "matplotlib.backends.backend_qt5agg", 
                 "numpy", "PyQt5.QtGui", "PyQt5.QtCore", "PyQt5.QtWidgets", "matplotlib", "pandas", 
                 "sklearn.model_selection", "tensorflow", "queue", "threading", "subprocess", "signal",
                 "time", "io", "tf_slim", "shutil", "PIL", "random", "logging", "object_detection",
                 "csv", "fnmatch", "winreg", "absl", "traceback", "tensorflow_io",'avro',
                 'apache_beam','lxml', 'Cython', 'contextlib2','six','pycocotools', 'lvis',
                 'scipy','pandas','official', 'orbit', 'tensorflow_models','keras','pyparsing', 
                 'sacrebleu'],
    "packages": packages,
    "include_msvcr": True,
}



bdist_mac_options = {
    "bundle_name": "Test",
}

bdist_dmg_options = {
    "volume_label": "TEST",
}

bdist_msi_options = {
    "add_to_path" : True

}

executables = [Executable("../src/MainGUI.py", base=base, icon="../res/icons/icon.ico"), 
               Executable("C:/Users/andrew/Documents/Programming/tensorflow/models/research/object_detection/model_main_tf2.py", base=base, icon="../res/icons/tensorflow_icon.ico") ]


setup(
    name="Object Detector",
    version="0.4",
    description="Object Detection GUI",
    options={
        "build_exe": build_exe_options,
        "bdist_mac": bdist_mac_options,
        "bdist_dmg": bdist_dmg_options,
        "bdist_msi": bdist_msi_options,
    },
    

    executables=executables,
    
)