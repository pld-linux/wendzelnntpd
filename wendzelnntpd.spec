# TODO
# - news uid
# - initscript
# - sane build system (patch makefile, cflags, cc, destdir)
# - finish and subpackage gui
#
# Conditional build:
%bcond_with	gui		# qt gui
#
Summary:	Tiny, easy to configure NNTP server for Unix
Name:		wendzelnntpd
Version:	1.4.0
Release:	0.1
License:	GPL v3
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/wendzelnntpd/%{name}-%{version}-src.tgz
# Source0-md5:	9ad40120ebf6d72417ecc0b8b7910350
URL:		http://www.wendzel.de/?sub=softw&ssub=wendzelnntpd
BuildRequires:	bison
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
%if %{with gui}
BuildRequires:	qt4-build >= 4.3.3-3
BuildRequires:	qt4-qmake >= 4.3.3-3
%endif
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The WendzelNNTPd is a simple IPv6-ready Usenet server with the main
goal to be as easy to use as possible.

It is portable (Linux/*BSD/*nix/Win32) and comes with a Qt based GUI.
It also supports short RSS info output for the last posted messages.

%prep
%setup -q -n %{name}
%{__sed} -i -e 's,^gcc -,%{__cc} -,' configure
%{__sed} -i -e 's,BUILDFLAGS=-O2 ,BUILDFLAGS=%{rpmcflags} ,' Makefile
%{__sed} -i -e 's,CFLAGS= -c -Wall ,CFLAGS= -c -Wall %{rpmcflags},' Makefile
%{__sed} -i -e 's,/var/spool/news/wendzelnntpd,$(DESTDIR)/../&,' Makefile
%{__sed} -i -e 's,strip,echo,' Makefile

%build
export CONFDIR=%{_sysconfdir}
./configure

%{__make} \
	CC="%{__cc}"

%if %{with gui}
cd gui/src
qmake-qt4 src.pro
%{__make}

%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT%{_prefix} \
	FAKECDIR=$RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/wendzelnntpd.conf
%attr(755,root,root) %{_sbindir}/wendzelnntpadm
%attr(755,root,root) %{_sbindir}/wendzelnntpd

%dir /var/spool/news/wendzelnntpd
%config(noreplace) %verify(not md5 mtime size) /var/spool/news/wendzelnntpd/usenet.db
