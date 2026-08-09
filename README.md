# seabreeze_c_backend for python-seabreeze

This repository provides `python-seabreeze`'s C backend as an extra package.

The extension module is compiled against CPython's stable ABI (`Py_LIMITED_API >= 0x030B0000`), so a single
`cp311-abi3` wheel is forward compatible with all python versions `>= 3.11` and does not have to be rebuilt for
newer python releases.

Both requirements for this are met now:

- [x] CPython needs to add the buffer interface to its limited API (which happened in py311)
- [x] Cython needs enough support for the limited api (available since cython 3.1)

## Building

The build uses [CMake](https://cmake.org/) via [scikit-build-core](https://scikit-build-core.readthedocs.io/):

```bash
pip install .
```

On linux `libusb` (the `libusb-0.1` api, i.e. `libusb-dev` / `libusb-compat`) is required.

### libseabreeze as a standalone shared library

`libseabreeze` is a self contained CMake project in [`src/libseabreeze`](src/libseabreeze). It can be built and
installed independently of the python package, i.e. for packaging it in `conda-forge`:

```bash
cmake -S src/libseabreeze -B build/libseabreeze -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build build/libseabreeze
cmake --install build/libseabreeze
```

This installs the shared library, its headers, a CMake package (`find_package(seabreeze)`) and a
`libseabreeze.pc` pkg-config file.

The python package can then be built against an existing `libseabreeze` installation:

```bash
pip install . --config-settings=cmake.define.SEABREEZE_C_BACKEND_USE_SYSTEM_LIBSEABREEZE=ON
```

### Development with pixi

A [pixi](https://pixi.sh) manifest provides the full build stack:

```bash
pixi run test               # build the package and run the tests
pixi run build-wheel        # build an abi3 wheel
pixi run install-libseabreeze  # build and install libseabreeze as a shared library
pixi run lint               # run the pre-commit hooks
```
