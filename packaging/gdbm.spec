#
# spec file for package gdbm
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           gdbm
Version:        1.8.3
Release:        0
License:        GPL-2.0+
Summary:        GNU dbm key/data database
%define lname	libgdbm
Url:            http://directory.fsf.org/GNU/gdbm.html
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
Source2:        baselibs.conf
Patch0:         gdbm-%{version}.dif
Patch1:         gdbm-protoize_dbm_headers.patch
Patch2:         gdbm-prototype_static_functions.patch
Patch3:         gdbm-fix_testprogs.patch
Patch4:         gdbm-1.8.3-no-build-date.patch
BuildRequires:  libtool
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
GNU dbm is a library of database functions that use extensible
hashing and work similar to the standard UNIX dbm. These routines are
provided to a programmer needing to create and manipulate a hashed
database.

The basic use of GDBM is to store key/data pairs in a data file. Each
key must be unique and each key is paired with only one data item.

The library provides primitives for storing key/data pairs, searching
and retrieving the data by its key and deleting a key along with its
data. It also supports sequential iteration over all key/data pairs in
a database.

For compatibility with programs using old UNIX dbm functions, the
package also provides traditional dbm and ndbm interfaces.

%package -n %lname
License:        GPL-2.0+
Summary:        GNU dbm key/data database
Group:          System/Libraries
# O/P added in 12.2
Obsoletes:      gdbm < %{version}-%{release}
Provides:       gdbm = %{version}-%{release}

%description -n %lname
GNU dbm is a library of database functions that use extensible
hashing and work similar to the standard UNIX dbm. These routines are
provided to a programmer needing to create and manipulate a hashed
database.

The basic use of GDBM is to store key/data pairs in a data file. Each
key must be unique and each key is paired with only one data item.

The library provides primitives for storing key/data pairs, searching
and retrieving the data by its key and deleting a key along with its
data. It also supports sequential iteration over all key/data pairs in
a database.

For compatibility with programs using old UNIX dbm functions, the
package also provides traditional dbm and ndbm interfaces.

%package devel
License:        GPL-2.0+ ; LGPL-2.1+
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries/C and C++
Requires:       gdbm = %{version}
Provides:       gdbm:/usr/lib/libgdbm.so

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q
%patch0
%patch1
%patch2
%patch3
%patch4

%build
aclocal
autoreconf --force --install
%ifarch sparc64
export CC="gcc -m64"
%endif
export CFLAGS="%{optflags} -Wa,--noexecstack"
%configure
make %{?_smp_mflags};

%install
make install INSTALL_ROOT=%{buildroot}
make install-compat INSTALL_ROOT=%{buildroot}
echo "/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
GROUP ( %{_libdir}/libgdbm.so %{_libdir}/libgdbm_compat.so )" > %{buildroot}/%{_libdir}/libndbm.so
echo "/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
GROUP ( %{_libdir}/libgdbm.a %{_libdir}/libgdbm_compat.a )" > %{buildroot}/%{_libdir}/libndbm.a

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%files -n %lname
%defattr(-,root,root)
%doc COPYING README NEWS
%{_libdir}/libgdbm.so.3
%{_libdir}/libgdbm.so.3.0.0
%{_libdir}/libgdbm_compat.so.3
%{_libdir}/libgdbm_compat.so.3.0.0

%files devel
%defattr(-,root,root)
%{_includedir}/dbm.h
%{_includedir}/gdbm.h
%{_includedir}/ndbm.h
%{_infodir}/gdbm.info.gz
%{_libdir}/libgdbm.a
%{_libdir}/libgdbm.so
%{_libdir}/libgdbm_compat.a
%{_libdir}/libgdbm_compat.so
%{_libdir}/libndbm.a
%{_libdir}/libndbm.so
%{_mandir}/man3/gdbm.3.gz
%exclude %{_libdir}/*.la


%changelog