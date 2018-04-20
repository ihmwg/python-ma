"""Utility classes to read in information in mmCIF format"""

import ihm.format

class _IDMapper(object):
    """Handle mapping from mmCIF IDs to Python objects.

       :param list system_list: The list in :class:`ihm.System` that keeps
              track of these objects.
    """
    def __init__(self, system_list):
        self.system_list = system_list
        self._obj_by_id = {}

    def make_new(self, cls, objid, initargs):
        """Make and return a new object of type `cls` with id `objid`, or
           return an existing one."""
        if objid in self._obj_by_id:
            return self._obj_by_id[objid]
        else:
            newobj = cls(*initargs)
            newobj._id = objid
            self._obj_by_id[objid] = newobj
            self.system_list.append(newobj)
            return newobj


class _SystemReader(object):
    """Track global information for a System being read from a file, such
       as the mapping from IDs to objects."""
    def __init__(self):
        self.system = ihm.System()
        self.software = _IDMapper(self.system.software)


class _Handler(object):
    """Base class for all handlers of mmCIF data."""
    def __init__(self, sysr):
        self.sysr = sysr

    def _copy_if_present(self, obj, data, keys=[], mapkeys={}):
        """Set obj.x from data['x'] for each x in keys if present in data.
           The dict mapkeys is handled similarly except that its keys are looked
           up in data and the corresponding value used to set obj."""
        for key in keys:
            if key in data:
                setattr(obj, key, data[key])
        for key, val in mapkeys.items():
            if key in data:
                setattr(obj, val, data[key])

    system = property(lambda self: self.sysr.system)


class _StructHandler(_Handler):
    category = '_struct'

    def __call__(self, d):
        self._copy_if_present(self.system, d, keys=('title',),
                              mapkeys={'entry_id': 'id'})


class _SoftwareHandler(_Handler):
    category = '_software'

    def __call__(self, d):
        s = self.sysr.software.make_new(ihm.Software, d['pdbx_ordinal'],
                                        (None,)*4)
        self._copy_if_present(s, d,
                keys=('name', 'classification', 'description', 'version',
                      'type', 'location'))


def read(fh):
    """Read data from the mmCIF file handle `fh`.
    
       :param file fh: The file handle to read from.
       :return: A list of :class:`ihm.System` objects.
    """
    systems = []

    s = _SystemReader()
    handlers = [_StructHandler(s), _SoftwareHandler(s)]
    r = ihm.format.CifReader(fh, dict((h.category, h) for h in handlers))
    r.read_file()

    # todo: handle multiple systems (from multiple data blocks)
    systems.append(s.system)
    return systems