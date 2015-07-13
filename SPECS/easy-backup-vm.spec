Name:		easy-backup-vm
Version:	1.0.0
Release:	1%{?dist}
BuildArch:  x86_64
Summary:	Easy Backup Utility for KVM virtual machines

Group:		Application/Internet
License:	GPLv2
URL:		an-vitek@ya.ru
Source0:	easy-backup.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	easy-backup

%description
Easy Backup Utility for KVM virtual machines

%prep
%setup -q -n easy-backup



%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
doc_dir=%{buildroot}/%{_datadir}/doc/easy-backup/backup_vm
bin_dir=%{buildroot}/%{_bindir}
lib_dir=%{buildroot}/%{_prefix}/lib/easy-backup/backup_vm
backup_dir=%{buildroot}/BACKUP/servers
cfg_dir=%{buildroot}/etc/backup_vm.d/
lock_dir=%{buildroot}/%{_localstatedir}/lock/backup_vm
mkdir -p $doc_dir $bin_dir $lib_dir $backup_dir $cfg_dir $lock_dir
mv backup_vm/README $doc_dir
mv backup_vm/backup $bin_dir/backup_vm
mv backup_vm/functions $lib_dir
mv backup_vm/vmsnapshot $lib_dir
mv backup_vm/winexe $bin_dir
mv backup_vm/backup_vm.d/scheduler.conf.template $cfg_dir/scheduler.conf
mv backup_vm/backup_vm.d/backup_vm.conf.template $cfg_dir/backup_vm.conf
mkdir $cfg_dir/vmsnapshot.d
mv backup_vm/vmsnapshot.d/default $cfg_dir/vmsnapshot.d/


%clean
rm -rf %{buildroot}


%files
%defattr(640,backuper,backuper,750)
%dir %{_datadir}/doc/easy-backup/backup_vm
%{_datadir}/doc/easy-backup/backup_vm/*
%dir %{_prefix}/lib/easy-backup/backup_vm
%attr(750,-,-) %{_bindir}/*
%{_prefix}/lib/easy-backup/backup_vm/*
%dir /etc/backup_vm.d
%config(noreplace) /etc/backup_vm.d/*.conf
%dir /etc/backup_vm.d/vmsnapshot.d
%config(noreplace) /etc/backup_vm.d/vmsnapshot.d/default
%dir %{_localstatedir}/lock/backup_vm
/BACKUP/servers

# 1 - install
# 2 - upgrade
#%pre

# 1 - install
# 2 - upgrade
%post
[ "$1" -eq 1 ] && {
    touch /var/log/backup_vm && chown backuper:backuper /var/log/backup_vm
    cron_file=/var/spool/cron/backuper
    if ! grep backup_vm $cron_file &>/dev/null; then
        echo "#*/10 *  * * * /bin/nice -n 19 backup-scheduler /usr/bin/backup_vm" >> $cron_file && {
            chown root:root $cron_file
            chmod 600 $cron_file
        }
    fi
}

# 0 - uninstall
# 1 - upgrade
#%preun


# 0 - uninstall
# 1 - upgrade
%postun
[ "$1" -eq 0 ] && rm -f /var/log/backup_vm

%changelog

