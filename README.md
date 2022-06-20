# Running with Python
[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

# Requirements
Install [SwitchPresence](https://github.com/SunResearchInstitute/SwitchPresence-Rewritten) on your Switch 

Download and install the [latest version of Python](https://www.python.org/downloads/) for your platform
### Use pip to install requirements
Just run the following command
```sh
pip install pypresence
```
:warning: **If you plan on running this headlessly,** be aware for any rich presence application to work, the client must also be running an instance of the [Discord](https://discord.com/download) client.

# Usage
Clone/download the repo

Add your switch's IP address to settings-example.ini then rename the file to settings.ini

Then just run the following command in the same directory as your ```presence-client.py``` file
```sh
python presence-client.py
```
### Customization
in `settings.ini` you can change the fallback image by replacing the Wikipedia URL with a link to an image of your choice.

### Limitations
Although most games will show the game logo, not every game is supported through the method used. Some have mismatching names(Legends Arceus), or aren't official(tinfoil). In these cases a default Switch logo is shown

In addition, game collections such as Mario 3D All-Stars don't work correctly.

## TODO
Find a better URL for game assets, `f_auto,q_auto,t_product_tile_desktop` stretches the game logo to a square, but it doesn't look very good. Cropping is our best option right now.
EU Nintendo site has square logos available, but they use NSUID in the URL, and only have the EU version.