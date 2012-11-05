%define keepstatic 1

Name:           gdbm
%define lname	libgdbm
Url:            http://directory.fsf.org/GNU/gdbm.html
Version:        1.10
Release:        0
License:        GPL-2.0+
Summary:        GNU dbm key/data database
Group:          System/Libraries
Source:         ftp://prep.ai.mit.edu/gnu/gdbm/gdbm-%{version}.tar.gz
Source2:        baselibs.conf
# FIX-FOR-UPSTREAM i@marguerite.su - remove the build date from src/version.c
BuildRequires:  libtool

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

%build
aclocal
autoreconf --force --install
export CFLAGS="%{optflags} -Wa,--noexecstack"
%configure --enable-libgdbm-compat
make %{?_smp_mflags};

%install
%make_install
echo "/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
GROUP ( %{_libdir}/libgdbm.so %{_libdir}/libgdbm_compat.so )" > %{buildroot}/%{_libdir}/libndbm.so
echo "/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
GROUP ( %{_libdir}/libgdbm.a %{_libdir}/libgdbm_compat.a )" > %{buildroot}/%{_libdir}/libndbm.a

mkdir -p %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/
cp -r %{SOURCE3} %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/%{name}.mo
%find_lang %{name}

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%defattr(-,root,root)
%doc COPYING
%{_libdir}/libgdbm.so.4
%{_libdir}/libgdbm.so.4.0.0
%{_libdir}/libgdbm_compat.so.4
%{_libdir}/libgdbm_compat.so.4.0.0

%files devel
%defattr(-,root,root)
%{_bindir}/testgdbm
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
