import os
import sys
import simplekml
from polycircles import polycircles
import time
import hashlib

M_IN_MILE = 1609.34

parent_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"


def points(points, filepath=None):
    kml_obj = simplekml.Kml()

    for p in points:
        label = p[0]
        point = p[1]
        p = kml_obj.newpoint(
                # name = label,
                coords=[(point[1], point[0])])
        # TODO: this is silly
        hex_color = hashlib.md5(label).hexdigest()[6:14]
        p.style.iconstyle.color = simplekml.Color.hex(hex_color)

    if filepath is None:
        filepath = str(time.time())

    kml_obj.save(parent_folder + "output/" + filepath)

def save_kml(markers, filepath=None, extra_locations={}):
    if filepath is None:
        filepath = str(time.time())

    kml_obj = simplekml.Kml()
    for marker in markers:
        centre_lat = marker.location[0]
        centre_lon = marker.location[1]

        outer_polycircle = polycircles.Polycircle(
            latitude=centre_lat,
            longitude=centre_lon,
            radius=(marker.distance + (marker.precision / 2.0))*M_IN_MILE,
            number_of_vertices=50)
        inner_polycircle = polycircles.Polycircle(
            latitude=centre_lat,
            longitude=centre_lon,
            radius=(marker.distance - (marker.precision / 2.0))*M_IN_MILE,
            number_of_vertices=50)

        pol = kml_obj.newpolygon(
            name="%.6f, %.6f | %.3f" % (centre_lat, centre_lon, marker.distance),
            outerboundaryis=outer_polycircle.to_kml(),
            innerboundaryis=inner_polycircle.to_kml())
        pol.style.polystyle.color = simplekml.Color.changealphaint(
            100, simplekml.Color.red)

    for key, loc in extra_locations.iteritems():
        kml_obj.newpoint(
            name=key,
            coords=[(loc[1], loc[0])])
    kml_obj.save(parent_folder + "output/" + filepath)
