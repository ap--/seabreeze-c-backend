# seabreeze_c_backend for python-seabreeze

This is a work in progress repository for providing `python-seabreeze`'s C backend as an extra package.

Once all requirements are met, this will allow to compile a python abi3 wheel using the py limited api for python 3.11,
which will be forward compatible with all python3 versions >= 3.11

There are 2 requirements:

- [x] CPython needs to add the buffer interface to its limited API (which apparently happened in py311)
- [x] Cython needs ~full~ enough support for the limited api (it currently still fails..., see [issue 1](https://github.com/ap--/seabreeze-c-backend/issues/1))

In the end this should save quite a bit of CI time, because it's very likely that there are not going to be any code changes to this backend anymore...
