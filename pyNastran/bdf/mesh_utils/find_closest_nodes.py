"""
defines:
    * nids_close = find_closest_nodes(nodes_xyz, nids, xyz_compare, neq_max, tol)
    * ieq = find_closest_nodes_index(nodes_xyz, xyz_compare, neq_max, tol)
"""
from __future__ import print_function
import numpy as np

from pyNastran.bdf.mesh_utils.bdf_equivalence import (
    _get_tree)

def find_closest_nodes(nodes_xyz, nids, xyz_compare, neq_max=1, tol=None):
    """
    Finds the closest nodes to an arbitrary set of xyz points

    Parameters
    ----------
    nodes_xyz : (Nnodes, 3) float ndarray
        the source points
    nids : (Nnodes, ) int ndarray
        the source node ids
    xyz_compare : (Ncompare, 3) float ndarray
        the xyz points to compare to
    tol : float; default=None
        the max spherical tolerance; the whole model
    neq_max : int; default=1.0
        the number of "close" points

    Returns
    -------
    nids_close: (Ncompare, ) int ndarray
        the close node ids
    """
    if not isinstance(neq_max, int):
        raise TypeError('neq_max=%r must be an int; type=%s' % (neq_max, type(neq_max)))
    tol = None
    if tol is None:
        xyz_max = nodes_xyz.max(axis=0)
        xyz_min = nodes_xyz.min(axis=0)
        assert len(xyz_max) == 3, xyz_max
        dxyz = np.linalg.norm(xyz_max - xyz_min)
        tol = 2. * dxyz
    #ieq = find_closest_nodes_index(nodes_xyz, xyz_compare, neq_max, tol)
    ncompare = xyz_compare.shape[0]


    # kdt, ieq, slots = _not_equal_nodes_build_tree(...)
    # ieq = _not_equal_nodes_build_tree(...)[1]
    # slots = _not_equal_nodes_build_tree(...)[2:]

    # [2:] - similar
    # [1]  - different
    ieq = _not_equal_nodes_build_tree(nodes_xyz, xyz_compare, tol,
                                      neq_max=neq_max)[2:]  # TODO: is this [2:] or [1]???
    assert len(ieq) == ncompare, 'increase the tolerance; tol=%s' % tol
    try:
        found_nids = nids[ieq]
    except IndexError:
        msg = 'increase the tolerance; tol=%s' % tol
        raise IndexError(msg)
    return found_nids


def find_closest_nodes_index(nodes_xyz, xyz_compare, neq_max, tol):
    """
    Finds the closest nodes to an arbitrary set of xyz points

    Parameters
    ----------
    nodes_xyz : (Nnodes, 3) float ndarray
        the source points
    xyz_compare : (Ncompare, 3) float ndarray
        the xyz points to compare to
    neq_max : int
        the number of "close" points (default=4)
    tol : float
        the max spherical tolerance

    Returns
    -------
    slots : (Ncompare, ) int ndarray
        the indices of the close nodes corresponding to nodes_xyz
    """
    #nodes_xyz, model, nids, inew = _eq_nodes_setup(
        #bdf_filename, tol, renumber_nodes=renumber_nodes,
        #xref=xref, node_set=node_set, debug=debug)
    ieq, slots = _not_equal_nodes_build_tree(nodes_xyz, xyz_compare, tol,
                                             neq_max=neq_max)[1:3]
    return ieq


def _not_equal_nodes_build_tree(nodes_xyz, xyz_compare, tol, neq_max=4):
    """
    helper function for `bdf_equivalence_nodes`

    Parameters
    ----------
    nodes_xyz : (Nnodes, 3) float ndarray
         the source points
    xyz_compare : (Ncompare, 3) float ndarray
         the xyz points to compare to
    tol : float
        the max spherical tolerance
    neq_max : int; default=4
        the number of close nodes

    Returns
    -------
    kdt : cKDTree() or KDTree()
        the kdtree object
    ieq : int ndarray
        The indices of nodes_xyz where the nodes in xyz_compare are close???
        neq_max = 1:
            (N, ) int ndarray
        neq_max > 1:
            (N, N) int ndarray
    slots : int ndarray
        The indices of nodes_xyz where the nodes in xyz_compare are close???
        neq_max = 1:
            (N, ) int ndarray
        neq_max > 1:
            (N, N) int ndarray
    """
    assert isinstance(xyz_compare, np.ndarray), type(xyz_compare)
    if nodes_xyz.shape[1] != xyz_compare.shape[1]:
        msg = 'nodes_xyz.shape=%s xyz_compare.shape=%s' % (
            str(nodes_xyz.shape), str(xyz_compare.shape))
        raise RuntimeError(msg)

    kdt = _get_tree(nodes_xyz)
    # check the closest 10 nodes for equality
    deq, ieq = kdt.query(xyz_compare, k=neq_max, distance_upper_bound=tol)
    #print(deq)
    #print('ieq =', ieq)
    #print('neq_max = %s' % neq_max)

    # get the ids of the duplicate nodes
    nnodes = nodes_xyz.shape[0]
    if neq_max == 1:
        assert len(deq.shape) == 1, deq.shape
        slots = np.where(ieq < nnodes)
    else:
        assert len(deq.shape) == 2, deq.shape
        slots = np.where(ieq[:, :] < nnodes)
    #print('slots =', slots)
    return kdt, ieq, slots
