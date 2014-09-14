"""
@author David W.H. Swenson
"""

import sys
import os
# I assume we're in the directory above the 
sys.path.append(os.path.abspath('../'))

import TrajFile
import trajectory
import snapshot
import storage

class TranslatorXYZ(object):
    '''
    We consider two data formats: xyz and storage (the latter being native
    for this code). Each format has associated with it trajectory object.
    For xyz, the object is TrajFile.TrajFile. For storage, the object is
    trajectory.Trajectory.

    A few relevant object names:
        self.trajfile is of type TrajFile.TrajFile 
        self.trajectory is of type trajectory.Trajectory

    Once one of these objects has been loaded, we can call self.regularize()
    to generate the other. Then we have an object which can output in either
    format.

    NB: there is no support yet for converting periodic boundary conditions
    between the to formats. In principle, that shouldn't be too hard, but it
    isn't necessary for current purposes (playing with 2D models with no
    periodicity).
    '''
    
    def __init__(self):
        self.traj = None
        self.trajectory = None

    def load_trajfile(self, tfile):
        '''Loads xyz file into self.traj, which is a TrajFile object'''
        self.traj = TrajFile.TrajFile().read_xyz(tfile)

    def load_from_storage(self, storage, loadnum=0):
        '''Loads data from storage object into self.trajectory'''
        self.trajectory = trajectory.Trajectory.load(loadnum)

    def trajfile2trajectory(self, trajfile):
        '''Converts TrajFile.TrajFile to trajectory.Trajectory'''
        res = trajectory.Trajectory()
        for frame in trajfile.frames:
            mysnap = snapshot.snapshot( coordinates=frame.pos,
                                        velocities=frame.vel )
            res.extend(mysnap)
        return res

    def trajectory2trajfile(self, trajectory):
        '''Converts trajectory.Trajectory to TrajFile.TrajFile'''
        res = TrajFile.TrajFile()
        for snap_i in len(range(trajectory.snapshots())):
            mysnap = trajectory.snapshot(snap_i)
            myframe = TrajFrame()
            myframe.natoms = mysnap.atoms()
            myframe.vel = mysnap.velocities()
            myframe.pos = mysnap.positions()
            #myframe.label = mysnap.labels() # TODO: atomlabels in snap
            myframe.mass = mysnap.masses()
            res.frames.append(myframe)
        return res

    def regularize(self):
        '''Assuming we loaded one of the objects, make the other one'''
        if self.trajectory==None:
            self.trajectory = self.trajfile2trajectory(self.traj)
        if self.trajfile==None:
            self.traj = self.trajectory2trajfile(self.trajectory)


    def output_storage(self, outfname):
        '''Writes trajectory to `outfname` as NetCDF'''
        pass

    def output_xyz(self, outfname):
        '''Writes trajectory to `outfname` as .xyz file'''
        self.traj.write_xyz(outfname)


