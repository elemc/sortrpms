#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ==================================================== #
# Python script to sort and move RPM packages for koji #
# Author: Alexei Panov                                 #
# e-mail: elemc AT atisserv DOT ru                     #
# ==================================================== #

from sortrpms import RPM, SortRPMs
from os.path import join as pathjoin

class SortKojiRPMs(SortRPMs):

#sourcedir               = "/srv/koji/incoming-pkgs"
    sourcedir               = '/home/alex/temp/koji-pkg-move/source'
#destdir                 = "/srv/koji/packages"
    destdir                 = '/home/alex/temp/koji-pkg-move/packages'
    create_repo_cmd         = 'echo %s' #createrepo -x debug/* %s > /dev/null'
    remove_source_files     = False

    def __init__(self):
        SortRPMs.__init__(self)

    def _get_dest_path(self, pkg):
        dest_path = self.destdir

        # first for koji        - package name
        dest_path = pathjoin(dest_path, pkg.name)
        # second                - package version 
        dest_path = pathjoin(dest_path, pkg.version)
        # third                 - release
        dest_path = pathjoin(dest_path, pkg.release)
        # last                  - arch
        if pkg.is_srpm():
            dest_path = pathjoin(dest_path, 'src')
        else:
            dest_path = pathjoin(dest_path, pkg.arch)
        
        return dest_path

if __name__ == "__main__":
    s = SortKojiRPMs()
    if not s.is_empty():
        s.move_packages()
        s.create_repo()
        s.show()
