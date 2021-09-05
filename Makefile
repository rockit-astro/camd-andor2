RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

GIT_VERSION = $(shell git name-rev --name-only --tags --no-undefined HEAD 2>/dev/null || echo git-`git rev-parse --short HEAD`)
SERVER_VERSION=$(shell awk '/Version:/ { print $$2; }' observatory-andor-camera-server.spec)

all:
	mkdir -p build
	cp andor_camd andor_camd.bak
	awk '{sub("SOFTWARE_VERSION = .*$$","SOFTWARE_VERSION = \"$(SERVER_VERSION) ($(GIT_VERSION))\""); print $0}' andor_camd.bak > andor_camd
	${RPMBUILD} -ba observatory-andor-camera-server.spec
	${RPMBUILD} -ba observatory-andor-camera-client.spec
	${RPMBUILD} -ba python3-warwick-observatory-andor-camera.spec
	${RPMBUILD} -ba onemetre-andor-camera-data.spec
	mv build/noarch/*.rpm .
	rm -rf build
	mv andor_camd.bak andor_camd
