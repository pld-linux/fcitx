# TODO:
# - kill /usr/bin/env dependencies
# - split gtk/qt parts, maybe engines (pinyin, qw, table)
#
# Conditional build:
%bcond_without	gtk2	# GTK+ 2.x IM module
%bcond_without	gtk3	# GTK+ 3.x IM module
%bcond_without	qt	# Qt library and IM module
%bcond_without	lua	# Lua support

Summary:	Fcitx - input method framework with extension support
Summary(pl.UTF-8):	Fcitx - szkielet metody wprowadzania znaków z obsługą rozszerzeń
Name:		fcitx
Version:	4.2.9.7
Release:	1
License:	GPL v2+ with plugins exception
Group:		X11/Applications
Source0:	https://download.fcitx-im.org/fcitx/%{name}-%{version}.tar.xz
# Source0-md5:	c58869c4ef9d3f57287a3d1f539c9850
URL:		https://fcitx-im.org/
BuildRequires:	QtCore-devel >= 4
BuildRequires:	QtDBus-devel >= 4
BuildRequires:	QtGui-devel >= 4
BuildRequires:	cairo-devel >= 1.0
BuildRequires:	cmake >= 3.1
BuildRequires:	dbus-devel >= 1.1.0
BuildRequires:	doxygen
BuildRequires:	enchant-devel
BuildRequires:	gcc >= 5:3.2
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.26
BuildRequires:	gobject-introspection-devel
%{?with_gtk2:BuildRequires:	gtk+2-devel >= 1:2.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0}
BuildRequires:	kf5-extra-cmake-modules >= 0.0.11
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
%{?with_lua:BuildRequires:	lua51-devel >= 5.1}
BuildRequires:	opencc-devel
BuildRequires:	pango-devel >= 1:1.0
BuildRequires:	pkgconfig
BuildRequires:	presage-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xkeyboard-config
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
BuildRequires:	xz
%if %{with qt}
BuildRequires:	QtCore-devel >= 4.8
BuildRequires:	QtDBus-devel >= 4.8
BuildRequires:	QtCore-devel >= 4.8
BuildRequires:	qt4-build >= 4.8
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Fcitx is an input method framework with extension support. Currently
it supports Linux and Unix systems like FreeBSD. It has three built-in
Input Method Engine, Pinyin, QuWei and Table-based input methods.

Fcitx tries to provide a native feeling under all desktop as well as a
light weight core. You can easily customize it to fit your
requirements.

%description -l pl.UTF-8
Fcitx to szkielet metody wprowadzania znaków z obsługą rozszerzeń.
Obecnie obsługuje Linuksa oraz systemy uniksowe, takie jak FreeBSD. Ma
trzy wbudowane silniki metod wprowadzania (IME): Pinyin, QuWei oraz
Table.

Fcitx próbuje zapewnić natywne zachowanie we wszystkich środowiskach,
a także lekką część główną. Można go łatwo konfigurować, aby
dostosować do własnych wymagań.

%package libs
Summary:	Fcitx shared libraries
Summary(pl.UTF-8):	Biblioteki współdzielone Fcitx
Group:		Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description libs
Fcitx shared libraries.

%description libs -l pl.UTF-8
Biblioteki współdzielone Fcitx.

%package devel
Summary:	Header files for Fcitx libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Fcitx
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Fcitx libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Fcitx.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env bash,/bin/bash,' \
	cmake/fcitx-{cmake-helper,extract-{confdesc,desktop,gettext,kde,po,qt},merge-config}.sh \
	data/script/fcitx-diagnose.sh

%build
install -d build
cd build
%cmake .. \
	%{?debug:-DENABLE_DEBUG=ON} \
	%{!?with_gtk2:-DENABLE_GTK2_IM_MODULE=OFF} \
	%{?with_gtk3:-DENABLE_GTK3_IM_MODULE=ON} \
	%{?with_lua:-DENABLE_LUA=ON} \
	%{!?with_qt:-DENABLE_QT=OFF} \
	-DLIB_INSTALL_DIR=%{_libdir} \
	-DSYSCONFDIR=%{_sysconfdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/fcitx

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING.LIBS COPYING.MIT ChangeLog README THANKS doc/{API.txt,Develop_Readme,cjkvinput.txt,pinyin.txt,wb_fh.htm}
%attr(755,root,root) %{_bindir}/createPYMB
%attr(755,root,root) %{_bindir}/fcitx
%attr(755,root,root) %{_bindir}/fcitx-autostart
%attr(755,root,root) %{_bindir}/fcitx-configtool
%attr(755,root,root) %{_bindir}/fcitx-dbus-watcher
%attr(755,root,root) %{_bindir}/fcitx-diagnose
%attr(755,root,root) %{_bindir}/fcitx-remote
%attr(755,root,root) %{_bindir}/fcitx-skin-installer
%attr(755,root,root) %{_bindir}/mb2org
%attr(755,root,root) %{_bindir}/mb2txt
%attr(755,root,root) %{_bindir}/readPYBase
%attr(755,root,root) %{_bindir}/readPYMB
%attr(755,root,root) %{_bindir}/scel2org
%attr(755,root,root) %{_bindir}/txt2mb
/etc/xdg/autostart/fcitx-autostart.desktop
%attr(755,root,root) %{_libdir}/fcitx/fcitx-*.so
%attr(755,root,root) %{_libdir}/fcitx/libexec/comp-spell-dict
%if %{with qt}
%attr(755,root,root) %{_libdir}/fcitx/libexec/fcitx-qt-gui-wrapper
%attr(755,root,root) %{_libdir}/qt4/plugins/inputmethods/qtim-fcitx.so
%endif
%if %{with gtk2}
%attr(755,root,root) %{_libdir}/gtk-2.0/2.*/immodules/im-fcitx.so
%endif
%if %{with gtk3}
%attr(755,root,root) %{_libdir}/gtk-3.0/3.*/immodules/im-fcitx.so
%endif
%{_datadir}/dbus-1/services/org.fcitx.Fcitx.service
%{_datadir}/fcitx
%{_datadir}/mime/packages/x-fskin.xml
%{_desktopdir}/fcitx.desktop
%{_desktopdir}/fcitx-configtool.desktop
%{_desktopdir}/fcitx-skin-installer.desktop
%{_iconsdir}/hicolor/*x*/apps/fcitx*.png
%{_iconsdir}/hicolor/scalable/apps/fcitx*.svg
%{_mandir}/man1/createPYMB.1*
%{_mandir}/man1/fcitx.1*
%{_mandir}/man1/fcitx-remote.1*
%{_mandir}/man1/mb2org.1*
%{_mandir}/man1/mb2txt.1*
%{_mandir}/man1/readPYBase.1*
%{_mandir}/man1/readPYMB.1*
%{_mandir}/man1/scel2org.1*
%{_mandir}/man1/txt2mb.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfcitx-config.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfcitx-config.so.4
%attr(755,root,root) %{_libdir}/libfcitx-core.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfcitx-core.so.0
%attr(755,root,root) %{_libdir}/libfcitx-gclient.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfcitx-gclient.so.1
%attr(755,root,root) %{_libdir}/libfcitx-utils.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfcitx-utils.so.0
%if %{with qt}
%attr(755,root,root) %{_libdir}/libfcitx-qt.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libfcitx-qt.so.0
%endif
%{_libdir}/girepository-1.0/Fcitx-1.0.typelib
# common for base and -devel
%dir %{_libdir}/fcitx
%dir %{_libdir}/fcitx/libexec

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fcitx4-config
%attr(755,root,root) %{_libdir}/libfcitx-config.so
%attr(755,root,root) %{_libdir}/libfcitx-core.so
%attr(755,root,root) %{_libdir}/libfcitx-gclient.so
%attr(755,root,root) %{_libdir}/libfcitx-utils.so
%attr(755,root,root) %{_libdir}/fcitx/libexec/fcitx-po-parser
%attr(755,root,root) %{_libdir}/fcitx/libexec/fcitx-scanner
%{_includedir}/fcitx
%{_includedir}/fcitx-config
%{_includedir}/fcitx-gclient
%{_includedir}/fcitx-utils
%{_datadir}/gir-1.0/Fcitx-1.0.gir
%{_pkgconfigdir}/fcitx.pc
%{_pkgconfigdir}/fcitx-config.pc
%{_pkgconfigdir}/fcitx-gclient.pc
%if %{with qt}
%attr(755,root,root) %{_libdir}/libfcitx-qt.so
%{_includedir}/fcitx-qt
%{_pkgconfigdir}/fcitx-qt.pc
%endif
%{_pkgconfigdir}/fcitx-utils.pc
%dir %{_datadir}/cmake/fcitx
%{_datadir}/cmake/fcitx/Fcitx*.cmake
# scripts
%attr(755,root,root) %{_datadir}/cmake/fcitx/fcitx-cmake-helper.sh
%attr(755,root,root) %{_datadir}/cmake/fcitx/fcitx-extract-*.sh
%attr(755,root,root) %{_datadir}/cmake/fcitx/fcitx-merge-config.sh
%attr(755,root,root) %{_datadir}/cmake/fcitx/getdescpo
# shell function libs
%{_datadir}/cmake/fcitx/fcitx-parse-po.sh
%{_datadir}/cmake/fcitx/fcitx-write-po.sh
