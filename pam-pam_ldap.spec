%define 	modulename pam_ldap
Summary:	LDAP Pluggable Authentication Module
Summary(es.UTF-8):   Módulo de autenticación que puede conectarse (PAM) para LDAP
Summary(pl.UTF-8):   Moduł PAM do uwierzytelniania z użyciem LDAP
Summary(pt_BR.UTF-8):   Módulo de autenticação plugável (PAM) para o LDAP
Name:		pam-%{modulename}
Version:	183
Release:	1
Epoch:		1
License:	LGPL
Group:		Base
Source0:	http://www.padl.com/download/%{modulename}-%{version}.tar.gz
# Source0-md5:	c0ad81e9d9712ddc6599a6e7a1688778
Patch0:		%{name}-install.patch
Patch1:		%{name}-chkuser.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-no-access-after-free.patch
URL:		http://www.padl.com/OSS/pam_ldap.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openldap-devel >= 2.3.0
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.304
Obsoletes:	pam_ldap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}
%define		schemadir	/usr/share/openldap/schema

%description
This is pam_ldap, a pluggable authentication module that can be used
with linux-PAM. This module supports password changes, V2 clients,
Netscapes SSL, ypldapd, Netscape Directory Server password policies,
access authorization, crypted hashes, etc.

%description -l es.UTF-8
pam_ldap es un módulo de autenticación que puede conectarse y usarse
con Linux-PAM. Este módulo acepta cambio de contraseñas, clientes V2,
Netscape SSL, ypldapd, política de contraseñas de Netscape Directory
Server, autorización de acceso, etc.

%description -l pl.UTF-8
To jest pam_ldap, wymienny moduł uwierzytelniania, który może być
użyty z linux-PAM. Moduł ten wspiera zmienianie haseł, klientów V2,
SSL firmy Netscape, ypldapd, polisy haseł Netscape Directory Server,
autoryzację dostępu, zakodowane skróty, itd.

%description -l pt_BR.UTF-8
pam_ldap é um módulo de autenticação plugável que pode ser usado com o
Linux-PAM. Esse módulo aceita mudança de senhas, clientes V2, Netscape
SSL, ypldapd, política de senhas do Netscape Directory Server,
autorização de acesso, etc.

%package -n openldap-schema-pam_ldap
Summary:	pam_ldap LDAP schema
Summary(pl.UTF-8):   Schemat LDAP dla pam_ldap
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-pam_ldap
This package contains LDAP schema used by pam_ldap.

%description -n openldap-schema-pam_ldap -l pl.UTF-8
Ten pakiet zawiera schemat LDAP używany przez pam_ldap.

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
install -d $RPM_BUILD_ROOT%{schemadir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALLUSER=`id -u` \
	INSTALLGROUP=`id -g`

install ldapns.schema $RPM_BUILD_ROOT%{schemadir}/pam_ldap-ns.schema
install ns-pwd-policy.schema $RPM_BUILD_ROOT%{schemadir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post -n openldap-schema-pam_ldap
%openldap_schema_register %{schemadir}/{pam_ldap-ns,ns-pwd-policy}.schema
%service -q ldap restart

%postun -n openldap-schema-pam_ldap
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/{pam_ldap-ns,ns-pwd-policy}.schema
	%service -q ldap restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README ldap.conf pam.d
%attr(755,root,root) %{_libdir}/security/pam_ldap.so
%{_mandir}/man5/*

%files -n openldap-schema-pam_ldap
%defattr(644,root,root,755)
%{schemadir}/*
