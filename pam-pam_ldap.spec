%define 	modulename pam_ldap
Summary:	LDAP Pluggable Authentication Module
Summary(es):	M�dulo de autenticaci�n que puede conectarse (PAM) para LDAP
Summary(pl):	Modu� PAM do uwierzytelniania z u�yciem LDAP
Summary(pt_BR):	M�dulo de autentica��o plug�vel (PAM) para o LDAP
Name:		pam-%{modulename}
Version:	180
Release:	4
Epoch:		1
Vendor:		Luke Howard <lukeh@padl.com>
License:	LGPL
Group:		Base
Source0:	http://www.padl.com/download/%{modulename}-%{version}.tar.gz
# Source0-md5:	627f053fdffb8267ba73261394e0ecde
Patch0:		%{name}-install.patch
Patch1:		%{name}-chkuser.patch
Patch2:		%{name}-nolibs.patch
Patch3:		%{name}-no-access-after-free.patch
URL:		http://www.padl.com/OSS/pam_ldap.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	openldap-devel >= 2.3.0
BuildRequires:	pam-devel
Obsoletes:	pam_ldap
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}
%define		schemadir	/usr/share/openldap/schema

%description
This is pam_ldap, a pluggable authentication module that can be used
with linux-PAM. This module supports password changes, V2 clients,
Netscapes SSL, ypldapd, Netscape Directory Server password policies,
access authorization, crypted hashes, etc.

%description -l es
pam_ldap es un m�dulo de autenticaci�n que puede conectarse y usarse
con Linux-PAM. Este m�dulo acepta cambio de contrase�as, clientes V2,
Netscape SSL, ypldapd, pol�tica de contrase�as de Netscape Directory
Server, autorizaci�n de acceso, etc.

%description -l pl
To jest pam_ldap, wymienny modu� uwierzytelniania, kt�ry mo�e by�
u�yty z linux-PAM. Modu� ten wspiera zmienianie hase�, klient�w V2,
SSL firmy Netscape, ypldapd, polisy hase� Netscape Directory Server,
autoryzacj� dost�pu, zakodowane skr�ty, itd.

%description -l pt_BR
pam_ldap � um m�dulo de autentica��o plug�vel que pode ser usado com o
Linux-PAM. Esse m�dulo aceita mudan�a de senhas, clientes V2, Netscape
SSL, ypldapd, pol�tica de senhas do Netscape Directory Server,
autoriza��o de acesso, etc.

%package -n openldap-schema-pam_ldap
Summary:	pam_ldap LDAP schema
Summary(pl):	Schemat LDAP dla pam_ldap
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers

%description -n openldap-schema-pam_ldap
This package contains LDAP schema used by pam_ldap.

%description -n openldap-schema-pam_ldap -l pl
Ten pakiet zawiera schemat LDAP u�ywany przez pam_ldap.

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
if ! grep -q %{schemadir}/pam_ldap-ns.schema /etc/openldap/slapd.conf; then
	sed -i -e '
		/^include.*local.schema/{
			i\
include		%{schemadir}/pam_ldap-ns.schema
		}
	' /etc/openldap/slapd.conf
fi
if ! grep -q %{schemadir}/ns-pwd-policy.schema /etc/openldap/slapd.conf; then
	sed -i -e '
		/^include.*local.schema/{
			i\
include		%{schemadir}/ns-pwd-policy.schema
		}
	' /etc/openldap/slapd.conf
fi


if [ -f /var/lock/subsys/ldap ]; then
	/etc/rc.d/init.d/ldap restart >&2
fi

%postun -n openldap-schema-pam_ldap
if [ "$1" = "0" ]; then
	if grep -q %{schemadir}/pam_ldap-ns.schema /etc/openldap/slapd.conf; then
		sed -i -e '
		/^include.*\/usr\/share\/openldap\/schema\/pam_ldap-ns.schema/d
		' /etc/openldap/slapd.conf
	fi

	if grep -q %{schemadir}/ns-pwd-policy.schema /etc/openldap/slapd.conf; then
		sed -i -e '
		/^include.*\/usr\/share\/openldap\/schema\/ns-pwd-policy.schema/d
		' /etc/openldap/slapd.conf
	fi

	if [ -f /var/lock/subsys/ldap ]; then
		/etc/rc.d/init.d/ldap restart >&2 || :
	fi
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog ldap.conf pam.d
%attr(755,root,root) %{_libdir}/security/pam_ldap.so
%{_mandir}/man5/*

%files -n openldap-schema-pam_ldap
%defattr(644,root,root,755)
%{schemadir}/*
