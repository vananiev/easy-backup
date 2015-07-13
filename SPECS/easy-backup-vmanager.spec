Name:		easy-backup-vmanager
Version:	1.0.0
Release:	1%{?dist}
BuildArch:  noarch
Summary:	Web Application for Easy Backup Utility

Group:		Application/Internet
License:	GPLv2
URL:		an-vitek@ya.ru
Source0:	vmanager.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	easy-backup-vm
Requires:   httpd
Requires:   mod_ssl

%description
Allows to startup/shutdown virtual machines.
Shows the last backup day and status for virtual machines.
Additional show hypervisor statistic.

%prep
%setup -q -n vmanager



%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
doc_dir=%{buildroot}/%{_datadir}/doc/easy-backup/vmanager
bin_dir=%{buildroot}/%{_bindir}
lib_dir=%{buildroot}/%{_prefix}/lib/easy-backup/vmanager
cfg_dir=%{buildroot}/etc/vmanager.d
http_data_dir=%{buildroot}/%{_localstatedir}/www/html/vmanager
sudo_dir=%{buildroot}/etc/sudoers.d
mkdir -p $doc_dir $bin_dir $lib_dir $cfg_dir $http_data_dir $sudo_dir $http_conf_dir $crt_dir $priv_key_dir
mv README $doc_dir
mv extern-config-files/httpd-sample-vmanager.conf $doc_dir
mv lib/vmanager $bin_dir/vmanager
mv lib/functions $lib_dir
mv lib/conf.d/vmanager.conf $cfg_dir
mv www/* www/.ht* $http_data_dir
mv -f $http_data_dir/.htpasswd-sample $http_data_dir/.htpasswd
mv extern-config-files/vmanager.sudo $sudo_dir

%clean
rm -rf %{buildroot}


%files
%defattr(640,vmanager,vmanager,750)
%dir %{_datadir}/doc/easy-backup/vmanager
%{_datadir}/doc/easy-backup/vmanager/*
%dir %{_prefix}/lib/easy-backup/vmanager
%{_prefix}/lib/easy-backup/vmanager/*
%attr(750,-,-) %{_bindir}/*
%dir /etc/vmanager.d
%config(noreplace) /etc/vmanager.d/*.conf
%dir %attr(-,-,apache) %{_localstatedir}/www/html/vmanager
%attr(-,-,apache) %{_localstatedir}/www/html/vmanager/*
%attr(-,-,apache) %{_localstatedir}/www/html/vmanager/.ht*
/etc/sudoers.d/*

# 1 - install
# 2 - upgrade
%pre
if [ "$1" -eq 1 ]; then
    id vmanager &>/dev/null || { groupadd vmanager &>/dev/null; useradd -g vmanager -G vmanager,backuper vmanager; } || exit 1
fi

# 1 - install
# 2 - upgrade
%post
[ "$1" -eq 1 ] && {
    touch /var/log/vmanager && chown vmanager:vmanager /var/log/vmanager
    cron_file=/var/spool/cron/vmanager
    if ! grep "/usr/bin/vmanager" $cron_file &>/dev/null; then
        echo "*/2 9-17 * * * /usr/bin/vmanager autostartWatchDog | grep -v 'Autostart vms for host' &>> /var/log/vmanager" >> $cron_file && {
            chown root:root $cron_file
            chmod 600 $cron_file
        }
    fi
    chmod o+r /var/log/messages*
}
    service httpd restart &>/dev/null

# 0 - uninstall
# 1 - upgrade
#%preun

# 0 - uninstall
# 1 - upgrade
%postun
[ "$1" -eq 0 ] && rm -f /var/log/vmanager

%changelog

