

from GangaCore.testlib.GangaUnitTest import GangaUnitTest


class TestSavannah40220(GangaUnitTest):
    def test_Savannah40220(self):
        from GangaCore.GPI import LCG, Job, export, load

        j = Job(backend=LCG())
        import tempfile
        f, self.fname = tempfile.mkstemp()

        self.assertTrue(export(j, self.fname))

        self.assertTrue(load(self.fname))

    def tearDown(self):
        import os
        os.remove(self.fname)

        super(TestSavannah40220, self).tearDown()
