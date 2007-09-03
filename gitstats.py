import os, sys, re, cgi

class config:
	heading = '#AAAAFF'
	border = '#000000'
	background = '#FFFFFF'
	rowcolor1 = '#FFFFFF'
	rowcolor2 = '#AADDAA'
	font = 'Verdana, Helvetica'
	foreground = '#000000'

repo = sys.argv[1]
reponame = os.path.basename(repo)

print """<html>
 <head>
  <title>%(reponame)s git statistics</title>
 </head>
 <body bgcolor="%(background)s">
  <font color="%(foreground)s" face="%(font)s">
   <table>
    <tr bgcolor="%(background)s">
     <td align="center">
      <strong>%(reponame)s git statistics</strong>
     </td>
    </tr>
    <tr>
     <td>
      <table bgcolor="%(border)s" border="0" cellspacing="1" cellpadding="2" width="100%%">
       <tr bgcolor="%(heading)s">
        <td>Committer</td>
         <td># of Changes</td>
         <td>Lines Changed</td>
         <td>Lines per Change</td>
         <td>%% of Changed Lines</td>
        </tr>""" % {
			'reponame': reponame,
			'background': config.background,
			'foreground': config.foreground,
			'font': config.font,
			'border': config.border,
			'heading': config.heading
		}

numlines = 0
numcommits = 0
highnum = 0
highfile = ""
highcommits = 0
highcommitter = ""
lines = {}
commits = {}
files = {}

os.chdir(repo)
sock = os.popen('git log --stat --pretty=format:"Author: %an <%ae>"')
buf = sock.readlines()
sock.close()

for i in buf:
	if not len(i.strip()):
		continue
	elif i.startswith("Author:"):
		author = i[8:-1]
		if author not in lines.keys():
			lines[author] = 0
		if author not in commits.keys():
			commits[author] = 0
		commits[author] += 1
		numcommits += 1
	elif ' |' in i:
		changes = i.split(' |')[1].strip().split()[0]
		if changes == "Bin":
			continue
		changes = int(changes)
		lines[author] += changes
		numlines += changes
		file = i.split(' |')[0].strip()
		if file not in files.keys():
			files[file] = 0
		files[file] += 1
		if files[file] > highnum:
			highnum = files[file]
			highfile = file

committers = commits.keys()
committers.sort()
count = 0
for i in committers:
	number = commits[i]
	changes = lines[i]
	percent = int((float(changes)/numlines)*100)
	average = changes / number
	if number > highcommits:
		highcommits = number
		highcommitter = i
	if count % 2 == 1:
		print '<tr bgcolor="%s">' % config.rowcolor2
	else:
		print '<tr bgcolor="%s">' % config.rowcolor1
	print "<td>%s</td>" % cgi.escape(i)
	print "<td>%s</td>" % number
	print "<td>%s</td>" % changes
	print "<td>%s</td>" % average
	print "<td>%s%%</td>" % percent
	count += 1
print """</table>
      <table bgcolor="%(border)s" cellspacing="1" cellpadding="2" width="100%%">
       <tr>
        <td bgcolor="%(heading)s">
         Total committers:
        </td>
        <td align="right" bgcolor="%(rowcolor1)s">
         %(count)s
        </td>
       </tr>
       <tr>
        <td bgcolor="%(heading)s">
         Most frequently modified file:
        </td>
        <td align="right" bgcolor="%(rowcolor1)s">
         %(highfile)s (<em>%(highnum)s</em>)
        </td>
       </tr>
       <tr>
       <td bgcolor="%(heading)s">
         Most frequent committer:
        </td>
        <td align="right" bgcolor="%(rowcolor1)s">
         %(highcommitter)s (<em>%(highcommits)s</em>)
        </td>
       </tr>
      </table>
     </td>
    </tr>
    <tr bgcolor="%(background)s">
     <td align="center">
      <strong>%(reponame)s git statistics generated by <b>gitstats</b></strong>
      <br>
      These statistics are provided purely for interested developers, and
      are not intended to reflect quality -or- quality of work done by any
      given developer in git, merely to show activity of operations in the
      git repository performed by all developers.  If you want to use them
      to motivate yourself, that's fine, but keep in mind that a bit of
      useful work is more meaningful than a lot of useless work.
      <br>
      Created by <a href="http://frugalware.org/~vmiklos/">Miklos Vajna</a>
     </td>
    </tr>
   </table>
  </font>
 </body>
</html>""" % {
		'reponame': reponame,
		'background': config.background,
		'border': config.border,
		'heading': config.heading,
		'rowcolor1': config.rowcolor1,
		'count': count,
		'highfile': highfile,
		'highnum': highnum,
		'highcommitter': cgi.escape(highcommitter),
		'highcommits': highcommits
	}
