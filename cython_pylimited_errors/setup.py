import os
from setuptools import Extension
from setuptools import find_packages
from setuptools import setup


def strtobool(val: str) -> int:
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return 1
    elif val in ("n", "no", "f", "false", "off", "0"):
        return 0
    else:
        raise ValueError(f"invalid truth value {val!r}")


compile_opts = {}

if strtobool(os.getenv("BUILD_ABI3", "false")):
    compile_opts["py_limited_api"] = True
    compile_opts["define_macros"] = [
        ("CYTHON_LIMITED_API", "1"),
        ("Py_LIMITED_API", "0x030B0000"),
    ]
    
ext = Extension(
    "limitedtest.bytes_decode",
    language="c++",
    sources=["limitedtest/bytes_decode.pyx"],
    **compile_opts,
)
ext.cython_directives = {
    "language_level": "3str"
}

setup(
    name="limitedtest",
    version="0.0.0",
    packages=find_packages(),
    setup_requires=[
        "setuptools>=18.0",
        "cython>=3.0.1",
        "wheel>=0.31.0",
    ],
    install_requires=[],
    extras_require={},
    python_requires=">=3.11",
    ext_modules=[ext],
)
