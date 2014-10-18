%define		apiver	2.91

Summary:	VTE terminal widget library
Name:		vte
Version:	0.38.1
Release:	1
License:	LGPL
Group:		X11/Libraries
Source0:	http://ftp.gnome.org/pub/gnome/sources/vte/0.38/%{name}-%{version}.tar.xz
# Source0-md5:	b34acede2cabc2a4f86775365352aabc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pkg-config
BuildRequires:	vala
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The vte package contains a terminal widget for GTK+. It's used by
gnome-terminal among other programs.

%package devel
Summary:	Headers for VTE
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The vte package contains a terminal widget for GTK+. It's used by
gnome-terminal among other programs.

You should install the vte-devel package if you would like to
compile applications that use the vte terminal widget. You do not need
to install vte-devel if you just want to use precompiled
applications.

%package apidocs
Summary:	VTE API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
VTE API documentation.

%package terminal
Summary:	Basic VTE terminal
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description terminal
Basic VTE terminal.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
cd gnome-pty-helper
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--with-html-dir=%{_gtkdocdir}
%{__make}
cd ..
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--enable-introspection		\
	--with-default-emulation=rxvt	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang vte-%{apiver}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f vte-%{apiver}.lang
%defattr(644,root,root,755)
%doc NEWS README AUTHORS
%attr(755,root,root) %ghost %{_libdir}/libvte-%{apiver}.so.?
%attr(755,root,root) %{_libdir}/libvte-%{apiver}.so.*.*.*
%{_libdir}/girepository-1.0/Vte-%{apiver}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvte-%{apiver}.so
%{_includedir}/vte-%{apiver}
%{_pkgconfigdir}/vte-%{apiver}.pc
%{_datadir}/gir-1.0/Vte-%{apiver}.gir
%{_datadir}/vala/vapi/vte-%{apiver}.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/vte-%{apiver}

%files terminal
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/vte-%{apiver}
%config(noreplace) %verify(not md5 mtime size) /etc/profile.d/vte.sh


