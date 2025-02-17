from GangaCore.Core.GangaRepository import addRegistry
from GangaCore.GPIDev.Lib.Registry.TransientRegistry import TransientRegistry


def establishNamedTemplates(registryname, filebase, doc='', file_ext='tpl', pickle_files=False):
    j = TransientRegistry(
        registryname, filebase, doc, file_ext=file_ext, pickle_files=pickle_files)
    addRegistry(j)
