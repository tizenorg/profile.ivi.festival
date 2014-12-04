Name:       festival
Version:    2.1
Release:    0
Group:      System/Libraries
License:    MIT and GPL-2.0+ and TCL
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
%configure --prefix=%{_prefix} \
           --libdir=%{_libdir} \
           --datadir=%{_datadir}/festival \
           --sysconfdir=%{_sysconfdir}

cd ..
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/speech_tools/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/festival-2.1/src/lib
# speech tools
cd speech_tools
%_configure --prefix=%{_prefix} \
            --libdir=%{_libdir} \
            --datadir=%{_datadir}/festival \
            --sysconfdir=%{_sysconfdir}

%__make CC="%__cc -fPIC $RPM_OPT_FLAGS" CXX="%__cxx $RPM_OPT_FLAGS -fPIC -Wno-non-template-friend -ffriend-injection -fno-strict-aliasing"
cd ../%{name}-%{version}
%__make CC="%__cc -fPIC $RPM_OPT_FLAGS" CXX="%__cxx $RPM_OPT_FLAGS -fPIC -Wno-non-template-friend -ffriend-injection -fno-strict-aliasing"
%__make doc


%install
cd ..
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/speech_tools/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/festival-2.1/src/lib
cd -
#%%make_install
#make INSTALLED_BIN=%%{buildroot}%%{_bindir} make_installed_bin_shared
cd ../speech_tools
%make_install
cd ../%{name}-%{version}
# install binarys
install -D bin/text2wave %{buildroot}%{_bindir}/text2wave
install -m 755 src/main/festival %{buildroot}%{_bindir}/
install -m 755 src/main/festival_client %{buildroot}%{_bindir}/
install -m 755 bin/festival_server* %{buildroot}%{_bindir}/
install -m 755 examples/saytime %{buildroot}%{_bindir}/
# install manpages
install -D -m 644 doc/festival.1 %{buildroot}%{_mandir}/man1/festival.1
install -m 644 doc/festival_client.1 %{buildroot}%{_mandir}/man1/
install -m 644 doc/text2wave.1 %{buildroot}%{_mandir}/man1/
# install configs
install -D lib/festival.scm %{buildroot}%{_sysconfdir}/festival.scm
# install dictionarys
install -D lib/dicts/cmu/cmudict-0.4.out %{buildroot}%{_datadir}/%name/dicts/cmu/cmudict-0.4.out
install -m 644 lib/dicts/cmu/*.scm %{buildroot}%{_datadir}/%name/dicts/cmu/
install -m 644 lib/dicts/wsj.wp39.poslexR %{buildroot}%{_datadir}/%name/dicts/
install -m 644 lib/dicts/wsj.wp39.tri.ngrambin %{buildroot}%{_datadir}/%name/dicts/
# install voices
mkdir -p %{buildroot}%{_datadir}/festival/voices/english/kal_diphone/festvox
mkdir -p %{buildroot}%{_datadir}/festival/voices/english/kal_diphone/group
cp lib/voices/english/kal_diphone/group/* %{buildroot}%{_datadir}/festival/voices/english/kal_diphone/group/
cp lib/voices/english/kal_diphone/festvox/*.scm %{buildroot}%{_datadir}/festival/voices/english/kal_diphone/festvox
# install data
cp lib/*.scm %{buildroot}%{_datadir}/festival/
cp lib/*.ngrambin %{buildroot}%{_datadir}/festival/
cp lib/*.gram %{buildroot}%{_datadir}/festival/
cp lib/*.el %{buildroot}%{_datadir}/festival/
install -D lib/etc/unknown*/audsp %{buildroot}%{_prefix}/lib/festival/audsp
# install libs
install -D src/lib/libFestival.so  %{buildroot}/%{_libdir}/libFestival.so
# install includes
mkdir -p %{buildroot}%{_includedir}/
install -m 644 src/include/*.h %{buildroot}%{_includedir}/
cd ../speech_tools
# install includes
mkdir -p %{buildroot}%{_includedir}/instantiate
mkdir -p %{buildroot}%{_includedir}/ling_class
mkdir -p %{buildroot}%{_includedir}/rxp
mkdir -p %{buildroot}%{_includedir}/sigpr
mkdir -p %{buildroot}%{_includedir}/unix
install -m 644 include/*h %{buildroot}%{_includedir}
install -m 644 include/instantiate/*h %{buildroot}%{_includedir}/instantiate
install -m 644 include/ling_class/*h %{buildroot}%{_includedir}/ling_class
install -m 644 include/rxp/*h %{buildroot}%{_includedir}/rxp
install -m 644 include/sigpr/*h %{buildroot}%{_includedir}/sigpr
install -m 644 include/unix/*h %{buildroot}%{_includedir}/unix
# make sure we have no static libs, install shared ones
install -m 644 lib/lib*.so* %{buildroot}%{_libdir}
rm -f %{buildroot}%{_libdir}/*.a

# install init script
# install -m 755 -D %%{S:6} %%{buildroot}/etc/init.d/%%name
# install -d %%{buildroot}%%_sbindir
# ln -sf ../../etc/init.d/%%name %%{buildroot}/usr/sbin/rc%%name
# installl sysconfig file
#install -m 644 -D %%{S:5} %%{buildroot}/var/adm/fillup-templates/sysconfig.%%name

%clean
rm -rf %{buildroot}

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
%license COPYING
%doc README INSTALL examples/*.text examples/ex1.* examples/*.scm examples/*.dtd
%{_sysconfdir}/festival.scm
#%%{_sysconfdir}/init.d/%%name
%{_bindir}/festival
%{_bindir}/festival_client
%{_bindir}/festival_server
%{_bindir}/festival_server_control
%{_bindir}/text2wave
%{_bindir}/saytime
%{_libdir}/libe*.so.*
%{_libdir}/libFestival.so
%{_prefix}/lib/festival
%{_datadir}/festival
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libe*.so
