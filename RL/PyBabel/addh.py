#############################################################################
#
# Author: Michel F. SANNER
# Reimplemented from Babel v1.6 from Pat Walters and Math Stahl
#
# Copyright: M. Sanner TSRI 2000
#
#############################################################################
#
# $Header: /opt/cvs/python/packages/share1.5/PyBabel/addh.py,v 1.6 2007/10/11 17:43:48 sargis Exp $
#
# $Id: addh.py,v 1.6 2007/10/11 17:43:48 sargis Exp $
#

"""
This file implements the AddHydrogens class.

Before this AddHydrogens object can be used, atoms must have been assigned
a type see (AtomHybridization in types.py).

Hydrogen atoms can be added using 2 different methods. The first one requires
bondOrders to have been calculated previousely.

example:
    
      >>> atype = AtomHybridization()
      >>> atype.assignHybridization(atoms)
      >>> addh = AddHydrogens()
      >>> hat = addh.addHydrogens(atoms)

      atoms has to be a list of atom objects
      Atom:
          a.coords : 3-sequence of floats
          a.bonds : list of Bond objects
          babel_type: string
          babel_atomic_number: int

      Bond:
          b.atom1 : instance of Atom
          b.atom2 : instance of Atom

      or
      
      >>> addh = AddHydrogens()
      >>> hat = addh.addHydrogens(atoms, method='withBondOrder')

      atoms has to be a list of atom objects as above and
      Bond:
          b.atom1 : instance of Atom
          b.atom2 : instance of Atom
          b.bondOrder : integer
          
      these calls return a list 'hat' containing a tuple for each Hydrogen
      atom to be added. This tuple provides:
          coordsH       : 3-float coordinates of the H atom
          atom          : the atom to which the H atom is to be connected
          atomic_number : the babel_atomic_number of the H atom
          type          : tyhe babel_type of the H atom

reimplmentation of Babel1.6 in Python by Michel Sanner April 2000
Original code by W. Patrick Walters and Matthew T. Stahl 
"""

import math

from .atomTypes import TypeConverter
from .util import *

ONE_OVER_SQRT3 = 0.577350269
SQRT_TWO_THIRDS = 0.816496581

SP3_C_H_DIST = 1.115
SP2_C_H_DIST = 1.103
SP_C_H_DIST = 1.090

SP3_N_H_DIST = 1.020
SP2_N_H_DIST = 1.020

SP3_O_H_DIST = 0.950


class AddHydrogens:
    """ """

    def addHydrogens(self, atoms, method="noBondOrder"):
        """ """
        Hatoms = []
        # method = 'noBondOrder'
        if method == "noBondOrder":
            num_H_to_add = self.count_missing_hydrogens(atoms)
            if num_H_to_add:
                Hatoms = self.place_hydrogens1(atoms, num_H_to_add)

        else:
            num_H_to_add = self.count_missing_bo_hydrogens(atoms)
            if num_H_to_add:
                Hatoms = self.place_hydrogens2(atoms, num_H_to_add)

        # cleanup
        for a in atoms:
            delattr(a, "_redo")

        return Hatoms

    def place_hydrogens1(self, atoms, num_H_to_add):
        """ """
        Hat = []
        for a in atoms:
            if a.babel_type == "C3":
                val = len(a.bonds)
                if val == 3:
                    Hat = Hat + self.add_tertiary_hydrogen(a, SP3_C_H_DIST)
                elif val == 2:
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_C_H_DIST)
                elif val == 1:
                    Hat = Hat + self.add_methyl_hydrogen(a, SP3_C_H_DIST)
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_C_H_DIST, Hat[-1])

            elif a.babel_type == "N3+":
                val = len(a.bonds)
                if val == 2:
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_N_H_DIST)
                elif val == 1:
                    Hat = Hat + self.add_methyl_hydrogen(a, SP3_N_H_DIST)
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_N_H_DIST, Hat[-1])

            elif a.babel_type == "C2" or a.babel_type == "Car":
                val = len(a.bonds)
                if val == 2:
                    Hat = Hat + self.add_sp2_hydrogen(a, SP2_C_H_DIST)

            elif (
                a.babel_type == "Npl" or a.babel_type == "Nam" or a.babel_type == "Ng+"
            ):
                val = len(a.bonds)
                if val == 2:
                    Hat = Hat + self.add_sp2_hydrogen(a, SP2_N_H_DIST)

            elif a.babel_type == "C1":
                if len(a.bonds) == 1:
                    Hat = Hat + self.add_sp_hydrogen(a, SP_C_H_DIST)

            elif a.babel_type == "O3":
                if len(a.bonds) == 1:
                    Hat = Hat + self.add_methyl_hydrogen(a, SP3_O_H_DIST)

        for a in atoms:
            if a.babel_type == "C2":
                if len(a.bonds) == 1:
                    Hat = Hat + self.add_vinyl_hydrogens(a, SP2_C_H_DIST)

            elif (
                a.babel_type == "Npl" or a.babel_type == "Nam" or a.babel_type == "Ng+"
            ):
                if len(a.bonds) == 1:
                    # FIXME babel C code says SP2_C_H_DIST here ???
                    Hat = Hat + self.add_vinyl_hydrogens(a, SP2_N_H_DIST)

        return Hat

    def place_hydrogens2(self, atoms, num_H_to_add):
        """ """
        Hat = []
        converter = TypeConverter("HYB")

        for a in atoms:
            type_name = converter.convert(a.babel_type, "zero")
            hyb = int(type_name)
            code = a.babel_atomic_number * 10 + hyb
            to_add = a._redo

            if code == 63:  # sp3 carbon
                if to_add == 1:
                    Hat = Hat + self.add_tertiary_hydrogen(a, SP3_C_H_DIST)
                elif to_add == 2:
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_C_H_DIST)
                elif to_add == 3:
                    Hat = Hat + self.add_methyl_hydrogen(a, SP3_C_H_DIST)
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_C_H_DIST, Hat[-1])
            elif code == 73:  # sp3 nitrogen
                if to_add == 1:
                    if a.babel_type == "N3+":
                        Hat = Hat + self.add_tertiary_hydrogen(a, SP3_N_H_DIST)
                    else:
                        Hat = Hat + self.add_sp3_N_hydrogen(a, SP3_N_H_DIST)
                elif to_add == 2:
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_N_H_DIST)
                elif to_add == 3:
                    Hat = Hat + self.add_methyl_hydrogen(a, SP3_N_H_DIST)
                    Hat = Hat + self.add_methylene_hydrogens(a, SP3_N_H_DIST, Hat[-1])

            elif code == 62:  # sp2 carbon
                if to_add == 1:
                    Hat = Hat + self.add_sp2_hydrogen(a, SP2_C_H_DIST)

            elif code == 72:  # sp2 nitrogen
                if to_add == 1:
                    Hat = Hat + self.add_sp2_hydrogen(a, SP2_N_H_DIST)

            elif code == 61:  # sp carbon
                if to_add == 1:
                    Hat = Hat + self.add_sp_hydrogen(a, SP_C_H_DIST)

            elif code == 83:  # sp3 oxygen
                if to_add == 1:
                    Hat = Hat + self.add_methyl_hydrogen(a, SP3_O_H_DIST)

            # save vinyl and amide protons for last,
            # this way we know where to put them

        for a in atoms:
            type_name = converter.convert(a.babel_type, "zero")
            hyb = int(type_name)
            code = a.babel_atomic_number * 10 + hyb
            to_add = a._redo

            if code == 62:  # sp2 carbon
                if to_add == 2:
                    Hat = Hat + self.add_vinyl_hydrogens(a, SP2_C_H_DIST)

            elif code == 72:  # sp2 nitrogen
                if to_add == 1:
                    Hat = Hat + self.add_vinyl_hydrogens(a, SP2_N_H_DIST)

        return Hat

    def count_missing_hydrogens(self, atoms):
        """ """
        num_H = 0

        for a in atoms:
            num_H += a._redo

        return num_H

    def count_missing_bo_hydrogens(self, atoms):
        """ """
        num_H = 0

        for a in atoms:
            num_H += a._redo

        return num_H

    def add_methyl_hydrogen(self, a, h_distance):
        """ """
        coords = [0.0, 0.0, 0.0]
        return self.add_hydrogen(a, coords, h_distance)

    def add_tertiary_hydrogen(self, a, h_distance):
        """ """
        coords = [0.0, 0.0, 0.0]
        return self.add_hydrogen(a, coords, h_distance)

    def add_methylene_hydrogens(self, a, h_distance):
        """ """
        coords = [0.0, 0.0, 0.0]
        return self.add_hydrogen(a, coords, h_distance)

    def add_sp_hydrogen(self, a, h_distance):
        """ """
        coords = [0.0, 0.0, 0.0]
        return self.add_hydrogen(a, coords, h_distance)

    def add_sp2_hydrogen(self, a, h_distance):
        """ """
        coords = [0.0, 0.0, 0.0]
        return self.add_hydrogen(a, coords, h_distance)

    def add_vinyl_hydrogens(self, a, h_distance):
        """ """
        coords = [0.0, 0.0, 0.0]
        return self.add_hydrogen(a, coords, h_distance)

    def add_sp3_N_hydrogen(self, a, h_distance):
        """ """
        coords = [0.0, 0.0, 0.0]
        return self.add_hydrogen(a, coords, h_distance)

    def add_hydrogen(self, a, coords, h_distance):
        """ """
        return [(coords[0], coords[1], coords[2], a.babel_atomic_number, a.babel_type)]
