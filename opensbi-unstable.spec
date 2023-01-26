# Disable debug packages, we don't need them.
%global debug_package %{nil}

Name:		opensbi-unstable
# The last part is short hash
# Format: <TAG>.<NUMBER_OF_COMMITS_AFTER_TAG>.<YEAR>.<MONTH>.<DAY>.<SHORT_COMMIT>
Version:	v1.2.0.2023.01.26.6b5188c
Release:	1%{?dist}
Summary:	RISC-V Open Source Supervisor Binary Interface

License:	BSD
URL:		https://github.com/riscv/opensbi

# Download tarball, e.g.:
# https://github.com/riscv/opensbi/archive/%full_commit.tar.gz
%global full_commit 6b5188ca14e59ce7bf71afe4e7d3d557c3d31bf8
Source0:	https://github.com/riscv/opensbi/archive/%{full_commit}.tar.gz

BuildRequires:	gcc
BuildRequires:	binutils
BuildRequires:	findutils
BuildRequires:	grep
BuildRequires:	coreutils
BuildRequires:  make
BuildRequires:  dtc
BuildRequires:  python3
BuildRequires:  gawk
BuildRequires:  sed


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
* Thu Jan 26 2022 David Abdurachmanov <davidlt@rivosinc.com> v1.2.0.2023.01.26.c6b5188c-1
- Use v1.2 (last stable release for now)

* Tue Jan 25 2022 David Abdurachmanov <davidlt@rivosinc.com> v1.2.34.2023.01.25.c45992c-1
- Sync with upstream master branch (v1.2-34-gc45992c)

* Thu Nov 17 2022 David Abdurachmanov <davidlt@rivosinc.com> v1.1.85.2022.11.17.14f5c4c-1
- Sync with upstream master branch (v1.1-85-g14f5c4c)

* Mon Jun 23 2022 David Abdurachmanov <davidlt@rivosinc.com> v1.1.0.2022.06.27.4489876-1
- Sync with upstream master branch (v1.1 tag)

* Thu Jun 23 2022 David Abdurachmanov <davidlt@rivosinc.com> v1.0.99.2022.06.23.6f1fe98-1
- Sync with upstream master branch

* Thu Jun 02 2022 David Abdurachmanov <davidlt@rivosinc.com> v1.0.92.2022.06.13.9dc5ec5-1
- Sync with upstream master branch

* Thu Jun 02 2022 David Abdurachmanov <davidlt@rivosinc.com> v1.0.81.2022.06.02.cb8271c-1
- Sync with upstream master branch

* Sat Nov 06 2021 David Abdurachmanov <david.abdurachmanov@gmail.com> v0.9.163.2021.11.06.0979ffd-1
- Sync with upstream master branch

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
