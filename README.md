# Tinder Locations

The code from my blog post "How Tinder keeps your exact location (a bit) private".

To run it and re-generate the image from the bottom of the post:

<img src="https://github.com/robert/tinder-locations/blob/master/images/tinder-map.jpg?raw=true" />

* `pip install -r requirements.txt`
* Make 2 fake Facebook and Tinder accounts and fill in the passwords in the `config.py` file (sorry)
* `python run.py`

This will output a KML file in the `output/` directory. View it [using Google Earth](https://support.google.com/earth/answer/7365595?hl=en&co=GENIE.Platform%3DDesktop).

There are quite a few useful helper functions for investigating Tinder's management of locations further. They aren't very well-documented, but if you'd like to use them and are having trouble then [send me a message](https://robertheaton.com/about/) and I'm sure we can figure it out together.

If you notice any consequential mistakes then [please do let me know](https://robertheaton.com/about/)!
