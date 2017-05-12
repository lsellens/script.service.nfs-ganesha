import xbmc
import xbmcvfs
import xbmcaddon
from os import system


class MyMonitor(xbmc.Monitor):
    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)
    
    def onSettingsChanged(self):
        writeexports()


# addon
__addon__ = xbmcaddon.Addon(id='script.service.nfs-ganesha')
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path'))
__addonhome__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__scriptname__ = "nfs-ganesha"
__author__ = "lsellens"
__url__ = "https://github.com/lsellens/xbmc.addons"


def writeexports():
    shares = __addon__.getSetting("SHARES")
    file = xbmcvfs.File(xbmc.translatePath(__addonhome__ + 'ganesha/ganesha.conf'), 'w')
    file.write('NFS_CORE_PARAM{NFS_Protocols=4;}\n')
    file.write('EXPORT_DEFAULTS{SecType=none;Protocols=4;Squash=All_Squash;Anonymous_uid=0;Anonymous_gid=0;}\n')
    for i in range(0, int(shares)):
        exec('folder{0} = __addon__.getSetting("SHARE_FOLDER{0}")'.format(i))
        exec('permission{0} = __addon__.getSetting("PERMISSION{0}")'.format(i))
        file.write('EXPORT{\n')
        file.write('Export_Id={0};Path="{1}";Pseudo="{1}";Access_Type={2};\n'.format(i+1, eval('folder{0}'.format(i)),
                                                                                     eval('permission{0}'.format(i))))
        file.write('FSAL{Name=VFS;}}\n')
    file.close()
    system("systemctl reload script.service.nfs-ganesha.service")


if not xbmcvfs.exists(xbmc.translatePath(__addonhome__ + 'ganesha/ganesha.conf')):
    writeexports()

monitor = MyMonitor()
while not monitor.abortRequested():
    if monitor.waitForAbort():
        break

