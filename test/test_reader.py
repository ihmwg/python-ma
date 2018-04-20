import utils
import os
import unittest
import sys
if sys.version_info[0] >= 3:
    from io import StringIO
else:
    from io import BytesIO as StringIO

TOPDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
utils.set_search_paths(TOPDIR)
import ihm.reader

class Tests(unittest.TestCase):
    def test_read(self):
        """Test read() function"""
        fh = StringIO("data_model\n_struct.entry_id testid\n")
        s, = ihm.reader.read(fh)
        self.assertEqual(s.id, 'testid')

    def test_system_reader(self):
        """Test SystemReader class"""
        s = ihm.reader._SystemReader()

    def test_id_mapper(self):
        """Test IDMapper class"""
        class MockObject(object):
            def __init__(self, x, y):
                self.x, self.y = x, y

        testlist = []
        im = ihm.reader._IDMapper(testlist)
        a = im.make_new(MockObject, 'ID1', ('1', '2'))
        b = im.make_new(MockObject, 'ID1', ('3', '4'))
        self.assertEqual(id(a), id(b))
        self.assertEqual(a.x, '1')
        self.assertEqual(a.y, '2')
        self.assertEqual(testlist, [a])

    def test_handler(self):
        """Test Handler base class"""
        class MockObject(object):
            pass
        o = MockObject()
        o.system = 'foo'
        h = ihm.reader._Handler(o)
        self.assertEqual(h.system, 'foo')

    def test_handler_copy_if_present(self):
        """Test copy_if_present method"""
        class MockObject(object):
            pass
        o = MockObject()
        h = ihm.reader._Handler(None)
        h._copy_if_present(o, {'foo':'bar', 'bar':'baz', 't':'u'},
                           keys=['test', 'foo'],
                           mapkeys={'bar':'baro', 'x':'y'})
        self.assertEqual(o.foo, 'bar')
        self.assertEqual(o.baro, 'baz')
        self.assertFalse(hasattr(o, 't'))
        self.assertFalse(hasattr(o, 'x'))
        self.assertFalse(hasattr(o, 'bar'))

    def test_struct_handler(self):
        """Test StructHandler"""
        fh = StringIO("_struct.entry_id eid\n_struct.title 'Test title'")
        s, = ihm.reader.read(fh)
        self.assertEqual(s.id, 'eid')
        self.assertEqual(s.title, 'Test title')

    def test_software_handler(self):
        """Test SoftwareHandler"""
        fh = StringIO("""
loop_
_software.pdbx_ordinal
_software.name
_software.classification
_software.description
_software.version
_software.type
_software.location
1 'test software' 'test class' 'test desc' program 1.0.1 https://example.org
""")
        s, = ihm.reader.read(fh)
        software, = s.software
        self.assertEqual(software._id, '1')
        self.assertEqual(software.name, 'test software')
        self.assertEqual(software.classification, 'test class')


if __name__ == '__main__':
    unittest.main()