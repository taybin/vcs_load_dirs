# arch-tag: tla working copy support 1062530429
# Copyright (C) 2003 John Goerzen
# <jgoerzen@complete.org>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import util
import os.path

class wc:
    """Object for a working copy."""

    def __init__(self, wcpath):
        self.wcpath = os.path.abspath(wcpath)
        if not self.wcverify():
            raise Exception, "%s is not a tla working copy" % self.wcpath

    def gettreeversion(self):
        return util.chdircmd(self.wcpath, util.getstdoutsafeexec, "tla",
                             ['tree-version'])[0].strip() 

    def wcverify(self):
        try:
            self.gettreeversion()
        except util.ExecProblem:
            return 0
        return 1

    def gettaggingmethod(self):
        return util.chdircmd(self.wcpath, util.getstdoutsafeexec, "tla",
                             ['tagging-method'])[0].strip()

    def gettree(self):
        return util.maketree(self.wcpath,
                             ignore = [r'^\{arch\}$',
                                       r'^,,',
                                       r'/\.arch-ids/',
                                       r'^\.arch-ids$',
                                       r'^\+\+'])
    
    def addtag(self, file):
        if file[-1] == '/':
            try:
                print "addtag: making dir %s" % file[:-1]
                os.makedirs(os.path.join(self.wcpath, file[:-1]))
            except:
                raise
        file = self.slashstrip(file)
        util.chdircmd(self.wcpath, util.safeexec, "tla",
                      ['add-tag', file])

    def movetag(self, src, dest):
        if src[-1] == '/' and dest[-1] == '/':
            # Dir to dir -- mv will catch it already.
            return
        src, dest = self.slashstrip(src, dest)
        util.chdircmd(self.wcpath, util.safeexec, "tla",
                      ['move-tag', src, dest])

    def movefile(self, src, dest):
        src, dest = self.slashstrip(src, dest)
        util.chdircmd(self.wcpath, os.rename, src, dest)


    def delfile(self, file):
        os.unlink(os.path.join(self.wcpath, file))

    def deltag(self, file):
        util.chdircmd(self.wcpath, util.safeexec, "tla",
                      ['delete-tag', file])

    def makelog(self):
        return util.chdircmd(self.wcpath, util.getstdoutsafeexec, "tla",
                             ['make-log'])[0].strip()


    def commit(self):
        util.chdircmd(self.wcpath, util.safeexec, "tla", ['commit'])
        
    def slashstrip(self, *args):
        retval = []
        for item in args:
            if not len(item):
                retval.append(item)
            if item[-1] == '/':
                item = item[:-1]
            retval.append(item)
        if len(args) == 1:
            return retval[0]
        return retval
