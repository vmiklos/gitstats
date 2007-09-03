doc: HEADER.html Changelog

HEADER.html: README
	ln -s README HEADER.txt
	asciidoc -a toc -a numbered -a sectids HEADER.txt
	rm HEADER.txt

Changelog: .git/refs/heads/master
	git log --no-merges |git name-rev --tags --stdin >Changelog
