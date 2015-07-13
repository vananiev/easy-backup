Name:		easy-backup
Version:	1.0.0
Release:	1%{?dist}
BuildArch:  noarch
Summary:	Easy Backup Utility Framework

Group:		Application/Internet
License:	GPLv2
URL:		an-vitek@ya.ru
Source0:	easy-backup.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

#Requires:	

%description
Easy Backup Utility Framework

%prep
%setup -q -n easy-backup



%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
bin_dir=%{buildroot}/%{_bindir}
doc_dir=%{buildroot}/%{_datadir}/doc/%{name}
sample_dir=%{buildroot}/%{_datadir}/%{name}/sample
lib_dir=%{buildroot}/%{_prefix}/lib/%{name}
backup_dir=%{buildroot}/BACKUP
mkdir -p $bin_dir $doc_dir $sample_dir $lib_dir $backup_dir
mv lib/scheduler $bin_dir/backup-scheduler
mv lib/functions $lib_dir
mv lib/config.d.example $sample_dir
mv lib/backup $sample_dir

%clean
rm -rf %{buildroot}


%files
%defattr(640,backuper,backuper,750)
%attr(750,-,-) %{_bindir}/backup-scheduler
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/sample
%dir %{_datadir}/doc/%{name}
%{_datadir}/%{name}/sample/*
%dir %{_prefix}/lib/%{name}
%{_prefix}/lib/%{name}/functions
%dir /BACKUP

# 1 - install
# 2 - upgrade
%pre
if [ "$1" -eq 1 ]; then
    id backuper &>/dev/null || useradd backuper || exit 1
fi

# 1 - install
# 2 - upgrade
#%post


# 0 - uninstall
# 1 - upgrade
#%preun


# 0 - uninstall
# 1 - upgrade
#%postun


%changelog

