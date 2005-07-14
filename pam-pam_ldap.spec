# TODO
# - SECURITY http://security.gentoo.org/glsa/glsa-200507-13.xml
%define 	modulename pam_ldap
Summary:	LDAP Pluggable Authentication Module
Summary(es):	Módulo de autenticación que puede conectarse (PAM) para LDAP
Summary(pl):	Modu³ PAM do uwierzytelniania z u¿yciem LDAP
Summary(pt_BR):	Módulo de autenticação plugável (PAM) para o LDAP
Name:		pam-%{modulename}
Version:	178
Release:	1
Epoch:		1
Vendor:		Luke Howard <lukeh@padl.com>
License:	LGPL
Group:		Base
Source0:	http://www.padl.com/download/%{modulename}-%{version}.tar.gz
# Source0-md5:	222186c498d24a7035e8a7494fc0797d
Patch0:		%{name}-install.patch
Patch1:		%{name}-chkuser.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-no-access-after-free.patch
URL:		http://www.padl.com/OSS/pam_ldap.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
Obsoletes:	pam_ldap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}

%description
This is pam_ldap, a pluggable authentication module that can be used
with linux-PAM. This module supports password changes, V2 clients,
Netscapes SSL, ypldapd, Netscape Directory Server password policies,
access authorization, crypted hashes, etc.

%description -l es
pam_ldap es un módulo de autenticación que puede conectarse y usarse
con Linux-PAM. Este módulo acepta cambio de contraseñas, clientes V2,
Netscape SSL, ypldapd, política de contraseñas de Netscape Directory
Server, autorización de acceso, etc.

%description -l pl
To jest pam_ldap, wymienny modu³ uwierzytelniania, który mo¿e byæ
u¿yty z linux-PAM. Modu³ ten wspiera zmienianie hase³, klientów V2,
SSL firmy Netscape, ypldapd, polisy hase³ Netscape Directory Server,
autoryzacjê dostêpu, zakodowane skróty, itd.

%description -l pt_BR
pam_ldap é um módulo de autenticação plugável que pode ser usado com o
Linux-PAM. Esse módulo aceita mudança de senhas, clientes V2, Netscape
SSL, ypldapd, política de senhas do Netscape Directory Server,
autorização de acesso, etc.

%prep
%setup -q -n %{modulename}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALLUSER=`id -u` \
	INSTALLGROUP=`id -g`

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog ldap.conf pam.d
%attr(755,root,root) %{_libdir}/security/pam_ldap.so
%{_mandir}/man5/*
