from solid import *
from solid.utils import *
from math import asin, atan, pi, cos, sin, sqrt, tan, acos
import toml
import os


'''
a roomba brush for inserting nylon fibers into and zip tying 
together to form a disposable roomba brush. get an old broom and place tape across then cut.
place a belt of fibers into the wedge segments on either side, insert each wedge segment into the brush and zip tie.
insert the belt of fibers into the roomba brush

TODO: snap on to remove the need for zip ties
TODO: Can insert razors 
to chop hair that gets wound around the brush.
'''
def RoombaBrush(
    motor_insert_cube_profile,
    motor_insert_cube_length,
    stator_insert_cube_profile,
    stator_insert_cube_length,
    brush_length,
    brush_diameter,
    number_fins,
    fiber_diameter,
    wall_thickness,
):
    roomba_brush = None
    # create the cube for the stator side insert
    # TODO: frustrum cone instead as a bushing
    # stator_insert = cube(
    #     [stator_insert_cube_profile, stator_insert_cube_profile, stator_insert_cube_length], center=True)
    stator_insert = cylinder(
        r1=stator_insert_cube_profile-wall_thickness,
        r2=stator_insert_cube_profile,
        h=stator_insert_cube_length,
        center=True,
    )

    # create the cube for the motor side insert
    motor_insert = cube(
        [motor_insert_cube_profile, motor_insert_cube_profile, motor_insert_cube_length], center=True)

    # create a flange with inserts for each segment of the cylinder brush and attach to motor_insert and stator_insert
    flange = cylinder(
        r=brush_diameter, h=brush_length, center=True)
    # create guides for the fins as wall_thickness cubes 
    fin_guide = cube(
        [wall_thickness, brush_diameter-wall_thickness, brush_length-wall_thickness], center=True)
    fin_guide = translate([0, brush_diameter/2+wall_thickness/2, 0])(fin_guide)


    # calculate the degrees of rotation for each fin
    fin_rotation = 360 / number_fins
    # insert the fins atop the flange
    for i in range(number_fins):
        fin = rotate([0, 0, fin_rotation * i])(fin_guide)
        flange = flange-hole()(fin)
        # flange=flange+fin

    # place the flange on motor and stator inserts
    stator_insert = stator_insert + translate([0, 0, brush_length/2+stator_insert_cube_length/2])(flange)
    motor_insert = motor_insert 
    # rotate the inserts to be parallel to the x-axis
    stator_insert = rotate([0, -90, 0])(stator_insert)
    motor_insert = rotate([0, 90, 0])(motor_insert)
    
    # move the stator to the far side of the brush
    stator_insert = translate([brush_length+stator_insert_cube_profile/2,0,0])(stator_insert)
    # move the motor back to the yz plane
    motor_insert = translate([-motor_insert_cube_profile/2,0,0])(motor_insert)
    # get the degrees due to wall_thickness chord at brush_diameter
    chord_degrees = 360*wall_thickness/(pi*brush_diameter)

    # create a wedge for each segment of the brush that starts as arclength and ends as fiber_diameter
    # stuff fibers on either side and affix with glue or tape, this is temporary as zip ties will 
    # squeeze them against the barrell
    wedge= cube(
        [wall_thickness-2*fiber_diameter, brush_diameter-wall_thickness, brush_length-wall_thickness], center=True)
    wedge= translate([0,brush_diameter/2,0])(wedge)

    for i in range(number_fins):
        wedge = wedge + rotate([0, 0, fin_rotation * i])(wedge)

    wedge = rotate([0, 90, 0])(wedge)

    roomba_brush = stator_insert + motor_insert

    return roomba_brush, wedge 


def render_object(render_object, filename):
    """
    creates a .stl and .scad solution for the given solidpython OpenSCAD object
    PARAMETERS:
        render_object: the OpenSCAD object
        filename: a string for the file to be saved
    """
    scad_render_to_file(render_object, filename + ".scad", file_header="$fn=200;")
    # render with OpenSCAD
    print("Openscad is now rendering the solution..")
    os.system("openscad -o " + filename + ".stl " + filename + ".scad &")


if __name__ == "__main__":
    config = toml.load("configuration.toml")
    roomba_brush,wedge = RoombaBrush(**config)
    render_object(roomba_brush, "roomba_brush")
    render_object(wedge, "wedge")
