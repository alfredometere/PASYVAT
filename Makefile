F2PY = f2py

F2PYFLAGS= -g

F2PYOPTS = --fcompiler=gfortran

LOGDIR = log

DIRS = analysis gui fio toolbox

TDIR = modules/analysis

all: clean fortune bsel rdist bseek cseek bidx binary

fortune:
	@ echo "This Makefile compiles the wrapped FORTRAN modules"
	@ echo "Creating compilation log directory"
	@ mkdir $(LOGDIR)

bsel:
	@ echo "Compiling bsel module ..."
	@ $(F2PY) -m bsel -c $(TDIR)/bsel.f90 $(F2PYOPTS) > $(LOGDIR)/bsel.log
	@ mv bsel.so $(TDIR)/bsel.so
	@ echo "Done"

rdist:
	@ echo "Compiling rdist module ..."
	$(F2PY) --verbose -m rdist -c $(TDIR)/rdist.f90 $(F2PYOPTS) > $(LOGDIR)/rdist.log
	@ mv rdist.so $(TDIR)/rdist.so
	@ echo "Done!"

bseek:
	@ echo "Compiling bseek module ..."
	@ $(F2PY) -m bseek -c $(TDIR)/bseek.f90 $(F2PYOPTS) > $(LOGDIR)/bseek.log
	@ mv bseek.so $(TDIR)/bseek.so
	@ echo "Done!"

bidx:
	@ echo "Compiling bidx module ..."
	@ $(F2PY) -m bidx -c $(TDIR)/bidx.f90  $(F2PYOPTS) > $(LOGDIR)/bidx.log
	@ mv bidx.so $(TDIR)/bidx.so
	@ echo "Done!"

cseek:
	@ echo "Compiling cseek module ..."
	@ $(F2PY) -m cseek -c $(TDIR)/cseek.f90 $(F2PYOPTS) > $(LOGDIR)/cseek.log
	@ mv cseek.so $(TDIR)/cseek.so
	@ echo "Done!"

cstruct:
	@ echo "Compiling cstruct module ..."
	@ $(F2PY) -m cstruct -c $(TDIR)/cstruct.f90 $(F2PYOPTS) > $(LOGDIR)/cstruct.log
	@ mv cstruct.so $(TDIR)/cstruct.so
	@ echo "Done!"

binary:
	@ echo "Flagging the Python script as executable"
	@ chmod 0775 ./pasyvat
	@ echo "Done!"
	@ echo "To run PASYVAT, simply type './pasyvat'"

clean:
	@ echo "Doing some housekeeping!"
	@ chmod 0664 ./pasyvat
	@ rm -rf *.pyc *~
	@ rm -rf full_rd.csv
	@ rm -rf $(TDIR)/*.so
	@ rm -rf $(LOGDIR)
	@ rm -rf modules/*.pyc modules/*~
	@ for prefix in $(DIRS); do \
	      rm -rf ./modules/$$prefix/*.pyc; \
	  done;
