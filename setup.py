"""
seabreeze-c-backend
===================

C Backend for python-seabreeze

Author: Andreas Poehlmann
Email: andreas@poehlmann.io

"""
import os
import platform
import sys

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext
from wheel.bdist_wheel import bdist_wheel


def strtobool(val: str) -> int:
    """distutils.util.strtobool(val)
    Convert a string representation of truth to true (1) or false (0).

    True values are y, yes, t, true, on and 1;
    false values are n, no, f, false, off and 0.
    Raises ValueError if val is anything else.
    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError(f"invalid truth value {val!r}")


compile_opts: dict

# Platform specific libraries and source files
if platform.system() == "Windows":
    ignore_subdirs = {"linux", "osx", "posix"}
    compile_opts = dict(
        define_macros=[("_WINDOWS", None)],
        include_dirs=[],
        libraries=["winusb", "ws2_32", "setupapi"],
        library_dirs=[],
    )

elif platform.system() == "Darwin":
    ignore_subdirs = {"linux", "winusb", "windows"}
    compile_opts = dict(
        define_macros=[], include_dirs=[], libraries=[], library_dirs=[]
    )
    compile_opts["extra_link_args"] = [
        "-framework",
        "Carbon",
        "-framework",
        "CoreFoundation",
        "-framework",
        "IOKit",
    ]

else:
    ignore_subdirs = {"osx", "winusb", "windows"}
    try:
        import pkgconfig
    except ImportError:
        compile_opts = dict(
            define_macros=[], include_dirs=[], libraries=["usb"], library_dirs=[]
        )
    else:
        compile_opts = pkgconfig.parse("libusb")

    if not strtobool(os.getenv("CSEABREEZE_DEBUG_INFO", "0")):
        # strip debug symbols
        compile_opts["extra_compile_args"] = ["-g0"]

# Collect all source files for cseabreeze backend
# sources = ["src/seabreeze_c_backend/_libseabreeze_wrapper.pyx"]
sources = ["src/seabreeze_c_backend/_libseabreeze_wrapper.cpp"]
for root, subdirs, fns in os.walk("src/libseabreeze/src"):
    subdirs[:] = (d for d in subdirs if d not in ignore_subdirs)
    sources.extend(os.path.join(root, fn) for fn in fns)
# Add seabreeze include dirs
compile_opts["include_dirs"].append(os.path.relpath("src/libseabreeze/include"))

build_abi3 = not strtobool(os.getenv("NO_CSEABREEZE_ABI3", "false"))

if sys.version_info >= (3, 11) and build_abi3:
    compile_opts["py_limited_api"] = True
    compile_opts["define_macros"].extend(
        [("CYTHON_LIMITED_API", "1"), ("Py_LIMITED_API", "0x030B0000")]
    )

# define extension
libseabreeze = Extension(
    "seabreeze_c_backend._libseabreeze_wrapper",
    language="c++",
    sources=[os.path.relpath(s) for s in sources],
    **compile_opts,
)

building_sphinx_documentation = bool(strtobool(os.environ.get("READTHEDOCS", "false")))
libseabreeze.cython_directives = {
    "binding": building_sphinx_documentation,  # fix class method parameters for sphinx
    "embedsignature": not building_sphinx_documentation,  # add function signature to docstring for ipython
    "language_level": "3str",
}
extensions = [libseabreeze]


# noinspection PyPep8Naming
class sb_build_ext(build_ext):
    def build_extensions(self):
        # Deal with windows command line limit
        if os.name == "nt":
            org_spawn = self.compiler.spawn

            def win_spawn(_, cmd, *args, **kwargs):
                # the windows shell can't handle all the object files provided to link.exe
                from subprocess import list2cmdline

                if cmd[0].endswith("link.exe"):
                    with open("ihatewindowssomuch.rsp", "w") as f:
                        f.write(list2cmdline(cmd[1:]) + "\n\r")
                    new_cmd = cmd[:1] + [f"@{os.path.abspath(f.name)}"]
                    return org_spawn(new_cmd, *args, **kwargs)
                else:
                    return org_spawn(cmd, *args, **kwargs)

            # noinspection PyArgumentList
            self.compiler.spawn = win_spawn.__get__(self.compiler)

        # prevent cpp compiler warning
        # - see: https://stackoverflow.com/a/36293331
        # - see: https://github.com/python/cpython/pull/7476/files
        try:
            self.compiler.compiler_so.remove("-Wstrict-prototypes")
        except (AttributeError, ValueError):
            pass

        # see: https://github.com/matplotlib/matplotlib/pull/18322
        if self.compiler.compiler_type == "msvc" and strtobool(
            os.environ.get("SEABREEZE_DISABLE_FH4", "0")
        ):
            # Disable FH4 Exception Handling implementation so that we don't
            # require VCRUNTIME140_1.dll. For more details, see:
            # https://devblogs.microsoft.com/cppblog/making-cpp-exception-handling-smaller-x64/
            # https://github.com/joerick/cibuildwheel/issues/423#issuecomment-677763904
            for ext in self.extensions:
                ext.extra_compile_args.append("/d2FH4-")

        return super().build_extensions()


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp") and sys.version_info >= (3, 11):
            # on CPython, our wheels are abi3 and compatible back to 3.11
            return "cp311", "abi3", plat

        return python, abi, plat


setup(
    use_scm_version={
        "write_to": "src/seabreeze_c_backend/_version.py",
        "version_scheme": "post-release",
    },
    cmdclass={
        "build_ext": sb_build_ext,
        "bdist_wheel": bdist_wheel_abi3,
    },
    ext_modules=extensions,
)
