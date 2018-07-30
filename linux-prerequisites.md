# Linux-only prerequisites

The project requires wxPython, which, on Linux, doesn't have a nice wheel ready built.  This means you'll need to compile wx, which will take a bunch of development libraries, and 3-4GiB of hard drive space during installation of dependencies.  If you run `detox` straight away, all of the test containers will attempt to install dependencies at the same time, meaning you'll need 3-4GiB * the amount of containers.

The recommendation is to run `tox` first to build the containers one by one, if you're short on disk space.

As for development libraries, these will differ per distro.  For recent versions of Ubuntu, (and Mint 18, upon which I develop), the bootstrapping is as follows:

```shell
# Deadsnakes is pretty invaluable for Python development full stop.
add-apt-repository ppa:deadsnakes/ppa
apt update

apt install -y build-essential dpkg-dev
apt install -y aptitude mc

apt install -y libgtk2.0-dev libgtk-3-dev
apt install -y libjpeg-dev libtiff-dev \
	libsdl1.2-dev libgstreamer-plugins-base1.0-dev \
	libnotify-dev freeglut3 freeglut3-dev libsm-dev \
	libwebkitgtk-dev libwebkitgtk-3.0-dev


# Install all available Python packages and their dev packages
apt install -y python2.7 python2.7-dev libpython2.7-dev python-virtualenv
apt install -y python3.6 python3.6-dev libpython3.6-dev python3.6-venv
apt install -y python3.7 python3.7-dev libpython3.7-dev python3.7-venv
```

Those were found in the vagrant bootstrapping files [here](https://github.com/wxWidgets/Phoenix/tree/a17558cccd12398e5d5a19bfcbc8ae740add9da8/vagrant).

## Alternative method

There are wheels built for each linux platform available, but they require extra work.  Personally, it worked well for me when simply running `pip install -r requirements.txt`, but I ran into issues when testing.  Feel free to experiment on your own and open a PR if you come up with an elegant solution.

For more information, see [here](https://wiki.wxpython.org/How%20to%20install%20wxPython#Installing_wxPython-Phoenix_using_pip).
