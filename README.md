# BookMyShow-Notify

A command-line application you can use to notify you when a show is available on 
[BookMyShow](https://in.bookmyshow.com/).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and 
testing purposes.

### Prerequisites

#### Supported platforms
- Linux
- Windows
- Mac

#### Install Python
You'll need Python 3.0+ installed before installing and using this package. 

##### On Linux
Debian/Ubuntu users can use the following command to install `python3` and `pip` on your system.
```
sudo apt install python3 python3-pip
```

##### On Windows
If you're a Windows user, you can download Python3 [here](https://www.python.org/downloads/). Make sure you check the
option __Add Python to PATH__.


##### On Mac
If you're a MacOS user, follow [this](https://docs.python-guide.org/starting/install3/osx/) link to see how to install
Python.

Or you can run the following commands to install Python using __homebrew__:
```
brew install python
easy_install pip
```

### Installing
After installing Python, run the following command from the cloned project directory to install the package:

```
python3 ./bookmyshow_notify/setup.py install
```

Once the installation is complete, you can verify the installation by running:

```
bookmyshow_notify --help
```

which should give you the following output:
```
usage: bookmyshow_notify [-h] [--url URL] [--date DATE]
                   [--keywords [KEYWORDS [KEYWORDS ...]]] [--seconds S]
                   [--movie MOVIE] [--location LOCATION] [--format FORMAT]

BookMyShow notifier CLI.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             URL to the movie's page on in.bookmyshow.com
  --date DATE           Date to check for, in format DD-MM-YYYY.
  --keywords [KEYWORDS [KEYWORDS ...]]
                        Names of multiplexes or theatres to check for. If no
                        arguments are passed, it checks for any venue on the
                        given date.
  --seconds S           Time in seconds to keep checking after (default: 60s).
  --movie MOVIE         Name of the show you're searching for.
  --location LOCATION   Your location. Eg: bengaluru, kochi, trivandrum.
  --format FORMAT       Movie format. Eg: 2D, 3D, IMAX3D etc.

```

### TODOs
- [ ] Concise error handling and validation
- [ ] Host this package on PyPI
- [ ] Proper releases
- [ ] Write unit tests
- [ ] TravisCI integration

## Built With

* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - The Python library used to work with HTML

## Authors

* **Sreesh Mallya** - *Initial work* - [sreesh-mallya](https://github.com/sreesh-mallya)

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* Original idea inspired from [this answer](https://qr.ae/TaOysV) on Quora by [@manojmj92](https://github.com/manojmj92).
