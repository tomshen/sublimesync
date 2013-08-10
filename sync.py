#!/usr/bin/python
import os, os.path as path, platform, shutil

def get_input(message, accepted):
    i = None
    while i not in accepted:
        i = raw_input(message).lower()
    return i

def setup_directories(d, sdir, ldir):
    if path.exists(ldir):
        if path.exists(sdir):
            print('Both local and sync "%s" directory exist.' % d)
            if get_input('Keep local or sync "%s" directory? [local,sync]: '
                    % d, ['local', 'sync']) == 'sync':
                print('Deleting local "%s" directory...' % d),
                shutil.rmtree(ldir)
                print('Done.')
            else:
                print('Deleting sync "%s" directory...' % d),
                shutil.rmtree(sdir)
                print('Done.')
                print('Moving local "%s" directory to sync directory...' % d),
                shutil.move(ldir, path.split(sdir)[0])
                print('Done.')
        else:
            print('No sync "%s" directory found' % ds)
            print('Moving local "%s" to sync directory...' % d),
            shutil.move(ldir, path.split(sdir)[0])
            print('Done.')
    if not path.exists(sdir):
        os.makedirs(sdir)

def link_windows(sync_dir, local_dir):
    for d in ['Packages', 'Installed Packages']:
        ldir = path.join(local_dir, d)
        sdir = path.join(sync_dir, d)
        setup_directories(d, sdir, ldir)
        os.system('mklink /j "%s" "%s"' % (ldir, sdir))

def link_unix(sync_dir, local_dir):
    for d in ['Packages', 'Installed Packages']:
        ldir = path.join(local_dir, d)
        sdir = path.join(sync_dir, d)
        if path.islink(ldir): # only works on Unix
            print('Local "%s" directory is already a symbolic link.' % d)
        else:
            os.system('ln -s "%s" "%s"' % (path.join(sync_dir, d), path.join(local_dir, d)))

def main():
    ST_VERSION = int(get_input('Sublime Text version number [2,3]: ',
        ['2', '3']))

    sync_dir_default = path.join('~', path.join('Dropbox', path.join('config',
        'sublime-text-%d' % ST_VERSION)))
    if platform.system().lower() == 'windows':
        link = link_windows
        local_dir_default = '~\\AppData\\Roaming\\Sublime Text %d' % ST_VERSION
    elif platform.system().lower() == 'darwin': # aka OS X
        link = link_unix
        local_dir_default = '~/Library/Application Support/Sublime Text %d' % ST_VERSION
    else: # assuming some form of Unix
        link = link_unix
        local_dir_default = '~/.config/sublime-text-%d' % ST_VERSION

    local_dir = raw_input(
        'Local Sublime Text config directory (Leave blank for "%s"): ' % local_dir_default)
    if not local_dir:
        local_dir = local_dir_default

    sync_dir = raw_input('Directory to sync config to (Leave blank for "%s"): ' % sync_dir_default)
    if not sync_dir:
        sync_dir = sync_dir_default

    print('Linking directories...')

    try:
        link(path.expanduser(sync_dir), path.expanduser(local_dir))
        print('Sublime Text configuration syncing successfully set up.')
    except:
        print('Error encountered linking directories.')

if __name__ == '__main__':
    main()