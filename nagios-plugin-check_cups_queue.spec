%define		plugin	check_cups_queue
Summary:	Nagios CUPS plugin
Name:		nagios-plugin-%{plugin}
Version:	0.1
Release:	0.1
License:	BSD
Group:		Networking
Source0:	http://dev.lusis.org/nagios/check_cups_queue.txt
# Source0-md5:	fe2dffc066980e2385d88755703f97fe
Patch0:		%{name}-force-locales.patch
URL:		http://dev.lusis.org/nagios/
Requires:	bc
Requires:	cups-clients
Requires:	mktemp
Requires:	nagios-core
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/nagios/plugins
%define		plugindir	%{_prefix}/lib/nagios/plugins

%description
This plugin will check the status of a remote CUPS print queue. It
will provide the size of the queue and optionally the age of the queue

%prep
%setup -qcT
install %{SOURCE0} .
%patch0 -p0

cat > nagios.cfg <<'EOF'
# Usage:
# %{plugin}
define command {
	command_name    %{plugin}
	command_line    %{plugindir}/%{plugin} -H $HOSTADDRESS$
}
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{plugindir}}
install check_cups_queue.txt $RPM_BUILD_ROOT%{plugindir}/%{plugin}
cp -a nagios.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{plugin}.cfg

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{plugin}.cfg
%attr(755,root,root) %{plugindir}/%{plugin}
