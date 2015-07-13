Name:		easy-backup-oracle
Version:	1.0.0
Release:	1%{?dist}
BuildArch:  noarch
Summary:	Easy Backup Utility for Oracle DBs

Group:		Application/Internet
License:	GPLv2
URL:		an-vitek@ya.ru
Source0:	easy-backup.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

Requires:	easy-backup

%description
Easy Backup Utility for Oracle DBs.
Performs cold backup for given DBs selected by
DB's host-dns-name (same as backup config file name in db.d/) and SID
given in this file. For multiply SID on one DB-host config file
named by template '[dns-hostname]-[some-identifier]'.

%prep
%setup -q -n easy-backup



%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
doc_dir=%{buildroot}/%{_datadir}/doc/easy-backup/backup_oracle
bin_dir=%{buildroot}/%{_bindir}
lib_dir=%{buildroot}/%{_prefix}/lib/easy-backup/backup_oracle
backup_dir=%{buildroot}/BACKUP/ORACLE
cfg_dir=%{buildroot}/etc/backup_oracle.d/
lock_dir=%{buildroot}/%{_localstatedir}/lock/backup_oracle
mkdir -p $doc_dir $bin_dir $lib_dir $backup_dir $cfg_dir $lock_dir
mv backup_oracle/README $doc_dir
mv backup_oracle/backup $bin_dir/backup_oracle
mv backup_oracle/functions $lib_dir
mv backup_oracle/backup_oracle.d/scheduler.conf.template $cfg_dir/scheduler.conf
mv backup_oracle/backup_oracle.d/backup_oracle.conf.template $cfg_dir/backup_oracle.conf
mkdir $cfg_dir/db.d
mv backup_oracle/db.d/example $cfg_dir/db.d


%clean
rm -rf %{buildroot}


%files
%defattr(640,backuper,backuper,750)
%dir %{_datadir}/doc/easy-backup/backup_oracle
%{_datadir}/doc/easy-backup/backup_oracle/*
%dir %{_prefix}/lib/easy-backup/backup_oracle
%attr(750,-,-) %{_bindir}/*
%{_prefix}/lib/easy-backup/backup_oracle/*
%dir /etc/backup_oracle.d
%config(noreplace) /etc/backup_oracle.d/*.conf
%dir /etc/backup_oracle.d/db.d
%config(noreplace) /etc/backup_oracle.d/db.d/example
%dir %{_localstatedir}/lock/backup_oracle
/BACKUP/ORACLE

# 1 - install
# 2 - upgrade
#%pre

# 1 - install
# 2 - upgrade
%post
[ "$1" -eq 1 ] && {
    touch /var/log/backup_oracle && chown backuper:backuper /var/log/backup_oracle
    cron_file=/var/spool/cron/backuper
    if ! grep backup_oracle $cron_file &>/dev/null; then
        echo "#*/10 *  * * * /bin/nice -n 19 backup-scheduler /usr/bin/backup_oracle" >> $cron_file && {
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
[ "$1" -eq 0 ] && rm -f /var/log/backup_oracle

%changelog

