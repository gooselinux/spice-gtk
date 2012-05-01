# we don't want to provide private python extension libs
%{?filter_setup:
%filter_provides_in %{python_sitearch}/.*\.so$
%filter_setup
}

Name:           spice-gtk
Version:        0.6
Release:        2%{?dist}
Summary:        A GTK2 widget for SPICE clients

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://spice-space.org/page/Spice-Gtk
Source0:        http://www.spice-space.org/download/gtk/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: intltool
BuildRequires: gtk2-devel >= 2.14
BuildRequires: spice-protocol >= 0.6.3
BuildRequires: pixman-devel openssl-devel libjpeg-devel
BuildRequires: celt051-devel pulseaudio-libs-devel
BuildRequires: pygtk2-devel python-devel zlib-devel
BuildRequires: cyrus-sasl-devel
# Hack because of bz #613466
BuildRequires: libtool

ExclusiveArch: %{ix86} x86_64

# Patches to fix build issues with glib 2.22, they have all been merged upstream
Patch0: spice-gtk-controller-includes.patch
Patch1: spice-gtk-0.6-vala-glib-226.patch
Patch2: spice-gtk-0.6-g_define_boxed.patch
Patch3: spice-gtk-0.6-g_object_notify_param_spec.patch
Patch4: spice-gtk-0.6-link-with-gthread.patch
# Patch to avoid needing perl-Text-CSV to build spice-gtk
# Next release will include these files in the tarball so the
# patch will no longer be needed
Patch5: spice-gtk-0.6-add-generated-files.patch


%description
Client libraries for SPICE desktop servers.

%package devel
Summary: Development files to build GTK2 applications with spice-gtk-2.0
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: spice-glib-devel = %{version}-%{release}
Requires: pkgconfig
Requires: gtk2-devel

%description devel
spice-client-gtk-2.0 provides a SPICE viewer widget for GTK2.

Libraries, includes, etc. to compile with the spice-gtk2 libraries

%package -n spice-glib
Summary: A GObject for communicating with Spice servers
Group: Development/Libraries

%description -n spice-glib
spice-client-glib-2.0 is a SPICE client library for GLib2.

%package -n spice-glib-devel
Summary: Development files to build Glib2 applications with spice-glib-2.0
Group: Development/Libraries
Requires: spice-glib = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel

%description -n spice-glib-devel
spice-client-glib-2.0 is a SPICE client library for GLib2.

Libraries, includes, etc. to compile with the spice-glib-2.0 libraries

%package python
Summary: Python bindings for the spice-gtk-2.0 library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description python
SpiceClientGtk module provides a SPICE viewer widget for GTK2.

A module allowing use of the spice-gtk-2.0 widget from python

%package tools
Summary: Spice-gtk tools
Group: Applications/Internet

%description tools
Simple clients for interacting with SPICE servers.
spicy is a client to a SPICE desktop server.
snappy is a tool to capture screen-shots of a SPICE desktop.

%prep
%setup -q
%patch0 -p1 -b .controller-includes
%patch1 -p1 -b .vala
%patch2 -p1 -b .gdefineboxed
%patch3 -p1 -b .gobjectnotify
%patch4 -p1 -b .gthread
%patch5 -p1 -b .generated

%build

%configure --disable-gtk-doc --with-gtk=2.0 --disable-introspection
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.a
rm -f %{buildroot}%{_libdir}/python*/site-packages/*.la
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS
%doc COPYING
%doc README
%doc NEWS
%{_libdir}/libspice-client-gtk-2.0.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libspice-client-gtk-2.0.so
%{_includedir}/spice-client-gtk-2.0
%{_libdir}/pkgconfig/spice-client-gtk-2.0.pc

%files -n spice-glib -f %{name}.lang
%defattr(-,root,root,-)
%{_libdir}/libspice-client-glib-2.0.so.*
%{_libdir}/libspice-controller.so.*

%files -n spice-glib-devel
%defattr(-,root,root,-)
%{_libdir}/libspice-client-glib-2.0.so
%{_libdir}/libspice-controller.so
%{_includedir}/spice-client-glib-2.0
%{_includedir}/spice-controller/*
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_libdir}/pkgconfig/spice-controller.pc
%{_datadir}/vala/vapi/spice-protocol.vapi
%doc %{_datadir}/gtk-doc/html/*

%files python
%defattr(-,root,root,-)
%{_libdir}/python*/site-packages/SpiceClientGtk.so

%files tools
%defattr(-,root,root,-)
%{_bindir}/snappy
%{_bindir}/spicy

%changelog
* Mon Jul 18 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-2
- Set release to -2 so that the EPEL package gets upgraded
- Related: rhbz#708417

* Mon Jul 18 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Added spice-gtk-0.6-add-generated-files.patch to be able to build without
  perl-Text-CSV
- Initial import of spice-gtk in RHEL CVS based on the EPEL .spec
- Related: rhbz#708417

* Fri May 27 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Initial EPEL release based on the rawhide .spec cleaned up from the parts
  that are not useful for EPEL (because the needed dependencies are not available)

* Wed May 25 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Upstream release 0.6

* Tue Mar  1 2011 Hans de Goede <hdegoede@redhat.com> - 0.5-6
- Fix spice-glib requires in .pc file (#680314)

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-5
- Fix build against glib 2.28

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-4
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-2
- Rebuild against newer gtk

* Thu Jan 27 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.5-1
- Upstream release 0.5

* Fri Jan 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4-2
- Add support for parallel GTK3 build

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 0.4-2
- add ExclusiveArch as only x86 is supported

* Sun Jan 09 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-1
- Upstream release 0.4
- Initial release (#657403)

* Thu Nov 25 2010 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.1.0-1
- Initial packaging
