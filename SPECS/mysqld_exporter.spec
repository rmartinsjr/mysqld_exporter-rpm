Name:           prometheus-mysqld-exporter
Version:        %{pkg_version}
Release:        %{rpm_release}%{?dist}
Summary:        Prometheus exporter for mysqld metrics.
License:        ASL 2.0
URL:            https://prometheus.io

Source0:        mysqld_exporter-%{pkg_version}.linux-amd64.tar.gz
Source1:        %{name}.service
Source2:        logrotate.conf
Source3:        rsyslog.conf
Source4:        environment.conf
Source5:        mysqld_exporter

BuildRoot:      %{buildroot}
BuildArch:      x86_64
BuildRequires:  systemd-units
Requires:       systemd, logrotate, rsyslog > 7.2
Requires(pre):  shadow-utils

%description

Prometheus is a systems and service monitoring system. It collects metrics from
configured targets at given intervals, evaluates rule expressions, displays the
results, and can trigger alerts if some condition is observed to be true.

This package contains binary to export mysqld metrics to prometheus.

%prep
%setup -q -n mysqld_exporter-%{version}.linux-amd64

%install

# Directory for storing log files.
mkdir -p %{buildroot}%{_localstatedir}/log/prometheus

# Logrotate config
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}.conf

# RSyslog config to enable writing to a file.
mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d/
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rsyslog.d/%{name}.conf

# SystemD unit definition and environment settings to go alongside unit file.
systemd_unit_dir="%{buildroot}%{_unitdir}"
systemd_unit_file="$systemd_unit_dir/%{name}.service"
mkdir -p $systemd_unit_dir
install -m 644 %{SOURCE1} $systemd_unit_file

# Make dependency directory for unit, and put environment file in there.
mkdir -p $systemd_unit_dir/%{name}.service.d
install -m 644 %{SOURCE4} $systemd_unit_dir/%{name}.service.d/environment.conf

# Add configuration file to /etc/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 600 %{SOURCE5} %{buildroot}%{_sysconfdir}/sysconfig/mysqld_exporter

# Binaries
mkdir -p %{buildroot}%{_bindir}
install -m 755 mysqld_exporter %{buildroot}%{_bindir}/mysqld_exporter

# Copy over License and notice
mkdir -p %{buildroot}/usr/share/prometheus/mysqld_exporter
install -m 644 LICENSE %{buildroot}/usr/share/prometheus/mysqld_exporter/LICENSE
install -m 644 NOTICE %{buildroot}/usr/share/prometheus/mysqld_exporter/NOTICE

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
          -c "Prometheus services" prometheus

%post
%systemd_post %{name}.service

echo
echo "NOTES ##############################################################################"
echo "Please restart RSyslog so that logs are written to %{_localstatedir}/log/prometheus"
echo "    systemctl restart rsyslog.service"
echo "To have %{name} start automatically on boot:"
echo "    systemctl enable %{name}.service"
echo "Start %{name}:"
echo "    systemctl daemon-reload"
echo "    systemctl start %{name}.service"
echo "Please reload firewalld:"
echo "    systemctl reload firewalld"
echo "####################################################################################"
echo

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,prometheus,prometheus,-)
%attr(755, root, root) %{_bindir}/mysqld_exporter
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/logrotate.d/%{name}.conf
%config(noreplace) %attr(644, root, root) %{_sysconfdir}/rsyslog.d/%{name}.conf
%config(noreplace) %{_unitdir}/%{name}.service
%config(noreplace) %{_unitdir}/%{name}.service.d/environment.conf
%config(noreplace) %attr(600, root, root) %{_sysconfdir}/sysconfig/mysqld_exporter
# Log directory
%dir %attr(755, prometheus, prometheus) %{_localstatedir}/log/prometheus

/usr/share/prometheus/mysqld_exporter
/usr/share/prometheus/mysqld_exporter/NOTICE
/usr/share/prometheus/mysqld_exporter/LICENSE

%changelog

* Sat Aug 29 2020 rmartinsjr@gmail.com
- Adapt project to mysqld_exporter

* Mon Feb 04 2019 talk@devghai.com
- Added support for handling breaking changes introduced in 0.15.0.

* Tue May 23 2017 talk@devghai.com
- Initial release for packaging Prometheus's Node Exporter.
  See https://github.com/meowtochondria/mysqld_exporter-rpm/blob/master/README.md.

