%define keepstatic 1

Name:           gdbm
%define lname   libgdbm
Url:            http://directory.fsf.org/GNU/gdbm.html
Version:        1.11
Release:        0
License:        GPL-3.0+
Summary:        GNU dbm key/data database
Group:          System/Libraries
Source:         ftp://prep.ai.mit.edu/gnu/gdbm/gdbm-%{version}.tar.gz
Source2:        baselibs.conf
Source1001:     gdbm.manifest
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
Summary:        GNU dbm key/data database
Group:          System/Libraries
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
Summary:        Include Files and Libraries mandatory for Development
Group:          System/Libraries
Requires:       gdbm = %{version}
Provides:       gdbm:/usr/lib/libgdbm.so

%description devel
This package contains all necessary include files and libraries needed
to develop applications that require these.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="%{optflags} -Wa,--noexecstack"
%configure --enable-libgdbm-compat --disable-nls
%__make %{?_smp_mflags};

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

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%files -n  %lname
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%{_bindir}/gdbm_dump
%{_bindir}/gdbm_load
%{_bindir}/gdbmtool
%{_libdir}/libgdbm.so.4
%{_libdir}/libgdbm.so.4.0.0
%{_libdir}/libgdbm_compat.so.4
%{_libdir}/libgdbm_compat.so.4.0.0

%files devel
%manifest %{name}.manifest
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
%{_mandir}/man1/gdbm_dump.1.gz
%{_mandir}/man1/gdbm_load.1.gz
%{_mandir}/man1/gdbmtool.1.gz
