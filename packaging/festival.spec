Name:       festival
Version:    2.1
Release:    2
Group:      System/Libraries
License:    MIT and GPL+ and TCL
Url:        http://www.cstr.ed.ac.uk/projects/festival/
Summary:    A free speech synthesis and text-to-speech system
Source0:    festival-%{version}.tar.gz
Source1:    speech_tools-%{version}-release.tar.gz
Source2:    festlex_CMU.tar.gz
Source3:    festvox_kallpc16k.tar.gz
Source4:    festlex_POSLEX.tar.gz
Patch0:     festival-1.95-examples.patch
Patch1:     festival-text2wave-manpage.patch
Patch2:     festival-1.95-libdir.patch
Patch3:     festival-1.95-audsp.patch
Patch4:     festival-1.96-chroot.patch
Patch5:     festival-no-LD_LIBRARY_PATH-extension.patch
Patch6:     festival-safe-temp-file.patch
# Use pulseaudio  
Patch7:     festival-use-pacat.patch  
Patch101:   speech_tools-undefined-operation.patch
Patch102:   speech_tools-1.2.95-config.patch
Patch103:   speech_tools-no-LD_LIBRARY_PATH-extension.patch
Patch104:   speech_tools-gcc47.patch

Patch200:   festival-1.96-speechtools-shared-build.patch
Patch201:   festival-1.96-bettersonamehack.patch
Patch205:   festival-1.96-main-speech_tools-shared-build.patch
Patch206:   festival-1.96-main-festival-shared-build.patch
Patch210:   no-shared-data.patch
Patch211:   festival-1.96-speechtools-linklibswithotherlibs.patch

BuildRequires:  pkgconfig(ncurses)

%description
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

%package devel
Summary:        Development Package for Festival
License:        MIT
Requires:       %{name} = %{version}

%description devel
Files needed for developing software that uses Festival.

%prep
%setup -q -b 1 -b 2 -b 3 -b 4
mv ../festival/lib/* lib/
%patch0 -p1
%patch1 -p1
%patch2
%patch3
%patch4
%patch5 -p1
%patch6 -p1
%patch7 -p1 -b .use-pacat 
cd ../speech_tools
%patch101 -p1
%patch102
%patch103 -p1
%patch104 -p1

%patch200 -p2 -b .shared-build
%patch201 -p2 -b .bettersoname
%patch205 -p2 -b .shared
cd ../festival-2.1
%patch206 -p1 -b .shared
cd ../speech_tools
%patch210 -p1 -b .no-shared-data
%patch211 -p1 -b .linklibswithotherlibs

%build
# festival
%configure --prefix=%_prefix \
	    --libdir=%_libdir \
	    --datadir=%_datadir/festival \
	    --sysconfdir=%_sysconfdir

cd ..
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/speech_tools/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/festival-2.1/src/lib

# speech tools
cd speech_tools
%configure --prefix=%_prefix \
            --libdir=%_libdir \
	        --datadir=%_datadir/festival \
            --sysconfdir=%_sysconfdir

make CC="gcc -fPIC $RPM_OPT_FLAGS" CXX="g++ $RPM_OPT_FLAGS -fPIC -Wno-non-template-friend -ffriend-injection -fno-strict-aliasing"
cd ../%{name}-%{version}
make CC="gcc -fPIC $RPM_OPT_FLAGS" CXX="g++ $RPM_OPT_FLAGS -fPIC -Wno-non-template-friend -ffriend-injection -fno-strict-aliasing"
make doc


%install
cd ..
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/speech_tools/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/festival-2.1/src/lib
cd -
#%make_install
#make INSTALLED_BIN=$RPM_BUILD_ROOT%{_bindir} make_installed_bin_shared
cd ../speech_tools
%make_install
cd ../%{name}-%{version}
# install binarys
install -D bin/text2wave $RPM_BUILD_ROOT%_bindir/text2wave
install -m 755 src/main/festival $RPM_BUILD_ROOT%_bindir/
install -m 755 src/main/festival_client $RPM_BUILD_ROOT%_bindir/
install -m 755 bin/festival_server* $RPM_BUILD_ROOT%_bindir/
install -m 755 examples/saytime $RPM_BUILD_ROOT%_bindir/
# install manpages
install -D -m 644 doc/festival.1 $RPM_BUILD_ROOT%_mandir/man1/festival.1
install -m 644 doc/festival_client.1 $RPM_BUILD_ROOT%_mandir/man1/
install -m 644 doc/text2wave.1 $RPM_BUILD_ROOT%_mandir/man1/
# install configs
install -D lib/festival.scm $RPM_BUILD_ROOT%_sysconfdir/festival.scm
# install dictionarys
install -D lib/dicts/cmu/cmudict-0.4.out $RPM_BUILD_ROOT%_datadir/%name/dicts/cmu/cmudict-0.4.out
install -m 644 lib/dicts/cmu/*.scm $RPM_BUILD_ROOT%_datadir/%name/dicts/cmu/
install -m 644 lib/dicts/wsj.wp39.poslexR $RPM_BUILD_ROOT%_datadir/%name/dicts/
install -m 644 lib/dicts/wsj.wp39.tri.ngrambin $RPM_BUILD_ROOT%_datadir/%name/dicts/
# install voices
mkdir -p $RPM_BUILD_ROOT/usr/share/festival/voices/english/kal_diphone/festvox
mkdir -p $RPM_BUILD_ROOT/usr/share/festival/voices/english/kal_diphone/group
cp lib/voices/english/kal_diphone/group/* $RPM_BUILD_ROOT/usr/share/festival/voices/english/kal_diphone/group/
cp lib/voices/english/kal_diphone/festvox/*.scm $RPM_BUILD_ROOT/usr/share/festival/voices/english/kal_diphone/festvox
# install data
cp lib/*.scm $RPM_BUILD_ROOT/usr/share/festival/
cp lib/*.ngrambin $RPM_BUILD_ROOT/usr/share/festival/
cp lib/*.gram $RPM_BUILD_ROOT/usr/share/festival/
cp lib/*.el $RPM_BUILD_ROOT/usr/share/festival/
install -D lib/etc/unknown_Linux/audsp $RPM_BUILD_ROOT/usr/lib/festival/audsp
# install libs
install -D src/lib/libFestival.so  $RPM_BUILD_ROOT/%_libdir/libFestival.so
# install includes
mkdir -p $RPM_BUILD_ROOT%_includedir/
install -m 644 src/include/*.h $RPM_BUILD_ROOT%_includedir/
cd ../speech_tools
# install includes
mkdir -p $RPM_BUILD_ROOT%_includedir/instantiate
mkdir -p $RPM_BUILD_ROOT%_includedir/ling_class
mkdir -p $RPM_BUILD_ROOT%_includedir/rxp
mkdir -p $RPM_BUILD_ROOT%_includedir/sigpr
mkdir -p $RPM_BUILD_ROOT%_includedir/unix
install -m 644 include/*h $RPM_BUILD_ROOT%_includedir
install -m 644 include/instantiate/*h $RPM_BUILD_ROOT%_includedir/instantiate
install -m 644 include/ling_class/*h $RPM_BUILD_ROOT%_includedir/ling_class
install -m 644 include/rxp/*h $RPM_BUILD_ROOT%_includedir/rxp
install -m 644 include/sigpr/*h $RPM_BUILD_ROOT%_includedir/sigpr
install -m 644 include/unix/*h $RPM_BUILD_ROOT%_includedir/unix
# make sure we have no static libs, install shared ones
install -m 644 lib/lib*.so* $RPM_BUILD_ROOT%_libdir
rm -f $RPM_BUILD_ROOT%_libdir/*.a

# install init script
# install -m 755 -D %{S:6} $RPM_BUILD_ROOT/etc/init.d/%name
# install -d $RPM_BUILD_ROOT%_sbindir
# ln -sf ../../etc/init.d/%name $RPM_BUILD_ROOT/usr/sbin/rc%name
# installl sysconfig file
#install -m 644 -D %{S:5} $RPM_BUILD_ROOT/var/adm/fillup-templates/sysconfig.%name

%clean
rm -rf $RPM_BUILD_ROOT

%post
ldconfig

%postun
ldconfig

%post devel
ldconfig

%postun devel
ldconfig

%files 
%defattr(-,root,root)
%doc COPYING README INSTALL examples/*.text examples/ex1.* examples/*.scm examples/*.dtd
%_sysconfdir/festival.scm
#%_sysconfdir/init.d/%name
%_bindir/festival
%_bindir/festival_client
%_bindir/festival_server
%_bindir/festival_server_control
%_bindir/text2wave
%_bindir/saytime
%_libdir/libe*.so.*
%_libdir/libFestival.so

%_prefix/lib/festival
%_datadir/festival
%_mandir/man1/*

%files devel
%defattr(-,root,root)
%_includedir/*
%_libdir/libe*.so
