

from GangaCore.GPIDev.Base.Proxy import stripProxy, isType

from GangaCore.testlib.monitoring import run_until_completed


def test_job_create(gpi):
    j = gpi.Job()


def test_job_kill(gpi):

    j = gpi.Job()

    # assert True if it gives an error while killing the job
    def cannot_kill(j):
        try:
            j.kill()
            return False, "should raise JobError"
        except:
            return True

    # cannot kill a job with status "new"
    assert cannot_kill(j)

    j.submit()
    run_until_completed(j)

    # cannot kill a job with status "completed"
    assert cannot_kill(j)


def test_job_submit(gpi):
    j = gpi.Job()
    j.submit()


def test_job_completed(gpi):
    j = gpi.Job()
    j.submit()
    assert run_until_completed(j)


def test_job_assignment(gpi):
    """Test assignment of all job properties"""

    j = gpi.Job()
    j.application.exe = "sleep"
    j.application.args = ['myarg']
    j.backend = gpi.ARC()
    j.backend.CE = "my.ce"
    j.inputdata = gpi.GangaDataset()
    j.inputdata.files = [gpi.LocalFile("*.txt")]
    j.inputfiles = [gpi.LocalFile("*.txt")]
    j.name = "testname"
    j.outputfiles = [gpi.LocalFile("*.txt")]
    j.postprocessors = gpi.FileChecker(files=['stdout'], searchStrings=['my search'])
    j.splitter = gpi.GenericSplitter()
    j.splitter.attribute = "application.args"
    j.splitter.values = ['arg 1', 'arg 2', 'arg 3']

    # test all the assignments
    assert isType(j, gpi.Job)
    assert j.application.exe == "sleep"
    assert j.application.args == ["myarg"]
    assert isType(j.backend, gpi.ARC)
    assert j.backend.CE == "my.ce"
    assert isType(j.inputdata, gpi.GangaDataset)
    assert len(j.inputdata.files) == 1
    assert isType(j.inputdata.files[0], gpi.LocalFile)
    assert j.inputdata.files[0].namePattern == "*.txt"
    assert len(j.inputfiles) == 1
    assert isType(j.inputfiles[0], gpi.LocalFile)
    assert j.inputfiles[0].namePattern == "*.txt"
    assert j.name == "testname"
    assert len(j.outputfiles) == 1
    assert isType(j.outputfiles[0], gpi.LocalFile)
    assert j.outputfiles[0].namePattern == "*.txt"
    assert len(j.postprocessors) == 1
    assert isType(j.postprocessors[0], gpi.FileChecker)
    assert j.postprocessors[0].files == ["stdout"]
    assert j.postprocessors[0].searchStrings == ["my search"]
    assert isType(j.splitter, gpi.GenericSplitter)
    assert j.splitter.attribute == "application.args"
    assert j.splitter.values == ['arg 1', 'arg 2', 'arg 3']


def test_job_copy(gpi):
    """Test that a job copy copies everything properly"""

    j = gpi.Job()
    j.application.exe = "sleep"
    j.application.args = ['myarg']
    j.backend = gpi.ARC()
    j.backend.CE = "my.ce"
    j.inputdata = gpi.GangaDataset()
    j.inputdata.files = [gpi.LocalFile("*.txt")]
    j.inputfiles = [gpi.LocalFile("*.txt")]
    j.name = "testname"
    j.outputfiles = [gpi.LocalFile("*.txt")]
    j.postprocessors = gpi.FileChecker(files=['stdout'], searchStrings=['my search'])
    j.splitter = gpi.GenericSplitter()
    j.splitter.attribute = "application.args"
    j.splitter.values = ['arg 1', 'arg 2', 'arg 3']
    j2 = j.copy()

    # test the copy has worked
    assert isType(j2, gpi.Job)
    assert j2.application.exe == "sleep"
    assert j2.application.args == ["myarg"]
    assert isType(j2.backend, gpi.ARC)
    assert j2.backend.CE == "my.ce"
    assert isType(j2.inputdata, gpi.GangaDataset)
    assert len(j2.inputdata.files) == 1
    assert isType(j2.inputdata.files[0], gpi.LocalFile)
    assert j2.inputdata.files[0].namePattern == "*.txt"
    assert len(j2.inputfiles) == 1
    assert isType(j2.inputfiles[0], gpi.LocalFile)
    assert j2.inputfiles[0].namePattern == "*.txt"
    assert j2.name == "testname"
    assert len(j2.outputfiles) == 1
    assert isType(j2.outputfiles[0], gpi.LocalFile)
    assert j2.outputfiles[0].namePattern == "*.txt"
    assert len(j2.postprocessors) == 1
    assert isType(j2.postprocessors[0], gpi.FileChecker)
    assert j2.postprocessors[0].files == ["stdout"]
    assert j2.postprocessors[0].searchStrings == ["my search"]
    assert isType(j2.splitter, gpi.GenericSplitter)
    assert j2.splitter.attribute == "application.args"
    assert j2.splitter.values == ['arg 1', 'arg 2', 'arg 3']

    # make sure properties are not shared between the copies
    j2.name = "testname2"
    j2.application.exe = "echo"

    # test the properties are not shared between copies
    assert j.name == "testname"
    assert j2.name == "testname2"
    assert j.application.exe == "sleep"
    assert j2.application.exe == "echo"


def test_job_equality(gpi):
    """Check that copies of Jobs are equal to each other"""
    j = gpi.Job()
    j2 = j.copy()
    j3 = gpi.Job(j)
    assert j == j2
    assert j2 == j3
    assert stripProxy(j) == stripProxy(j2)
    assert stripProxy(j2) == stripProxy(j3)


def test_job_naming_iteration(gpi):

    gpi.jobs.remove()

    s1 = gpi.Job(name="SameName")
    s2 = gpi.Job(name="SameName")
    d1 = gpi.Job(name="DifferentName")

    for j in gpi.jobs:
        assert gpi.jobs(j.id)

    # 2 items in slice
    SameName_jobs = gpi.jobs.select(name="SameName")

    assert s1 in SameName_jobs
    assert s2 in SameName_jobs

    # 1 item in slice
    assert (d1 in gpi.jobs.select(name="DifferentName"))
    assert (d1 is gpi.jobs["DifferentName"])

    # delete jobs with SameName
    SameName_jobs.remove()

    assert len(gpi.jobs) == 1
    assert gpi.jobs[-1].name == "DifferentName"

    # delete job with DifferentName
    gpi.jobs.select(name="DifferentName").remove()

    assert len(gpi.jobs) == 0
