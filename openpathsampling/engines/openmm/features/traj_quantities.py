import numpy as np
from simtk import unit

functions = ['trajectory_coordinates', 'trajectory_box_vectors',
             'trajectory_velocities']

def _trajectory_units(traj, feature, unit_):
    def strip_unit(obj):
        try:
            obj = obj.value_in_unit(unit_)
        except AttributeError:
            pass  # not a simtk.unit.Quantity
        return obj

    vals = [getattr(snap, feature) for snap in traj]
    print(feature, vals)
    result = [strip_unit(val) for val in vals]
    non_none = any([x is not None for x in result])
    if non_none:
        result = result * unit_
    print(result)
    return result

def trajectory_coordinates(traj):
    _trajectory_units(traj, 'coordinates', unit.nanometer)

def trajectory_box_vectors(traj):
    _trajectory_units(traj, 'box_vectors', unit.nanometer)

def trajectory_velocities(traj):
    _trajectory_units(traj, 'velocities', unit.nanometer / unit.picosecond)

