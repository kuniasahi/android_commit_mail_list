#!/usr/bin/env python
#
# Copyright (C) 2009 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import time
import os,sys
import xml.dom.minidom
import subprocess

def main(argv):
	codepath = os.getenv('ANDROID_BUILD_TOP')
	if codepath == None:
		print "useage:put it to your aosp root and source android project"
		return
	else:
		print "codepath = " + codepath
	manifestfile = codepath + "/.repo/manifest.xml"
	repopath = codepath + "/.repo/repo"
	projectpath = get_project_path(manifestfile)
	for path in projectpath:
		print get_project_git_logs(path)
		time.sleep(5)
	
	
def get_project_git_logs(projectpath):
	stdout = subprocess.PIPE
	stdin = subprocess.PIPE
	stderr = subprocess.PIPE
	command = ["git"]
	command.append("log")
	#command.append("--format=%h,%an,%ae,%ci")
	command.append("--format=%an,%ae,%ci")
	cwd = projectpath
	env = None
	mailist = None
	try:
		p = subprocess.Popen(command,cwd = cwd,env = env,stdin = stdin ,stdout = stdout,stderr = stderr)
		mailist=p.stdout.read();
	except Exception as e:
		print "run git error %s: %s" %(command[1],e)
	return mailist

def get_project_path(manifestfile):
	rootpath = manifestfile[0:len(manifestfile) - len("/.repo/manifest.xml")]
	print rootpath
	try:
		root = xml.dom.minidom.parse(manifestfile)
	except (OSError,xml.parsers.expat.ExpatError) as e:
		print "error to parsing manifest %s : %s" % (manifestfile.e)
	if not root or not root.childNodes:
		print "not root node in %s" % manifestfile
	manifest = []
	for manifest in root.childNodes:
		if manifest.nodeName == 'manifest':
			break
		else:
			print "error to get manifest"
	nodes = []
	projectlist = []
	for nodes in manifest.childNodes:
		if nodes.nodeName == 'project':
			#print nodes.getAttribute('path')
			projectlist.append(rootpath + "/" + nodes.getAttribute('path'))
	return projectlist

if __name__ == '__main__':
	main(sys.argv)
