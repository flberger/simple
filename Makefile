help:
	@echo targets:
	@echo '    check'
	@echo '    errors'
	@echo '    sdist'
	@echo '    docs'
	@echo '    exe'
	@echo '    user_install'
	@echo '    pypi'
	@echo '    doctest'
	@echo '    README.rst'
	@echo '    freecode'
	@echo '    sign'
	@echo '    clean'
	@echo '    commit.txt'
	@echo '    commit'
	@echo '    bitbucket'

check:
	pylint quickhtml

errors:
	pylint --errors-only quickhtml

ifdef PYTHON

sdist:
	rm -vf MANIFEST
	$(PYTHON) setup.py sdist --force-manifest --formats=zip

docs: clean
	pydoctor --verbose \\
	         --add-package $NAME$ \\
	         --make-html \\
	         --html-output doc/

exe: sdist
	rm -rf build/exe.*
	$(PYTHON) setup.py build

user_install:
	$(PYTHON) setup.py install --user --record user_install-filelist.txt

pypi:
	$(PYTHON) setup.py register

doctest:
	$(PYTHON) -m doctest README

else

sdist:
	@echo Please supply Python executable as PYTHON=executable.

exe:
	@echo Please supply Python executable as PYTHON=executable.

user_install:
	@echo Please supply Python executable as PYTHON=executable.

pypi:
	@echo Please supply Python executable as PYTHON=executable.

doctest:
	@echo Please supply Python executable as PYTHON=executable.

endif

README.rst: README
	pandoc --output README.rst README

freecode:
	@echo RETURN to submit to freecode.com using freecode-submit.txt, CTRL-C to cancel:
	@read DUMMY
	freecode-submit < freecode-submit.txt

sign:
	rm -vf dist/*.asc
	for i in dist/*.zip ; do gpg --sign --armor --detach $$i ; done
	gpg --verify --multifile dist/*.asc

clean:
	@echo About to remove all log files. RETURN to proceed && read DUMMY && rm -vf `find . -iname '*.log'`
	rm -rvf `find . -type d -iname '__pycache__'`
	rm -vf `find . -iname '*.pyc'`

commit.txt:
	hg diff > commit.txt

commit: commit.txt
	@echo commit.txt:
	@echo ------------------------------------------------------
	@cat commit.txt
	@echo ------------------------------------------------------
	@echo RETURN to commit using commit.txt, CTRL-C to cancel:
	@read DUMMY
	hg commit --logfile commit.txt && rm -v commit.txt

bitbucket:
	hg push https://flberger@bitbucket.org/flberger/simplegui
