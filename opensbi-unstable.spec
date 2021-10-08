# Disable debug packages, we don't need them.
%global debug_package %{nil}

Name:		opensbi-unstable
# The last part is short hash
# Format: <TAG>.<NUMBER_OF_COMMITS_AFTER_TAG>.<YEAR>.<MONTH>.<DAY>.<SHORT_COMMIT>
Version:	v0.9.152.2021.10.08.754d511
Release:	1%{?dist}
Summary:	RISC-V Open Source Supervisor Binary Interface

License:	BSD
URL:		https://github.com/riscv/opensbi

# Download tarball, e.g.:
# https://github.com/riscv/opensbi/archive/%full_commit.tar.gz
%global full_commit 754d51192b6bf6a4afd9d46c5f736a9f6dd1b404
Source0:	https://github.com/riscv/opensbi/archive/%{full_commit}.tar.gz

BuildRequires:	gcc
BuildRequires:	binutils
BuildRequires:	findutils
BuildRequires:	grep
BuildRequires:	coreutils
BuildRequires:  make
BuildRequires:  dtc


%description
RISC-V Open Source Supervisor Binary Interface compiled in jump variant.
This is only for QEMU RISC-V virt machine.


%prep
%autosetup -n opensbi-%{full_commit}


%build
make \
  PLATFORM=generic


%install
make \
  PLATFORM=generic \
  I=%{buildroot} \
  INSTALL_LIB_PATH=lib64 \
  INSTALL_FIRMWARE_PATH=%{_datadir}/%{name} \
  install


rm -rfv %{buildroot}/lib64
rm -rfv %{buildroot}/include
rm -rfv %{buildroot}%{_datadir}/%{name}/*/firmware/payloads


%files
%license COPYING.BSD
%doc README.md
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%changelog
* Fri Oct 08 2021 David Abdurachmanov <david.abdurachmanov@gmail.com> v0.9.152.2021.10.08.754d511-1
- Sync with upstream master branch

* Tue Aug 17 2021 David Abdurachmanov <david.abdurachmanov@gmail.com> v0.9.134.2021.08.17.7aa6c9a-1
- Sync with upstream master branch
- Upstream support for SiFive HiFive Unmatched

* Wed Apr 21 2021 David Abdurachmanov <david.abdurachmanov@gmail.com> v0.9.35.2021.04.21.f41196a
- Update to v0.9+

* Wed Jan 06 2021 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.8.81.2021.01.06.7dcb1e1
- New version
- Switch to generic platform
- Remove all others special Fedora variants of firmware
- Remove development library and documentation (not needed)
- Remove example payloads
