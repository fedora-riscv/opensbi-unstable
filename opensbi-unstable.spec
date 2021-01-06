# Disable debug packages, we don't need them.
%global debug_package %{nil}

Name:		opensbi-unstable
# The last part is short hash
# Format: <TAG>.<NUMBER_OF_COMMITS_AFTER_TAG>.<YEAR>.<MONTH>.<DAY>.<SHORT_COMMIT>
Version:	v0.8.81.2021.01.06.7dcb1e1
Release:	1%{?dist}
Summary:	RISC-V Open Source Supervisor Binary Interface

License:	BSD
URL:		https://github.com/riscv/opensbi

# Download tarball, e.g.:
# https://github.com/riscv/opensbi/archive/%full_commit.tar.gz
%global full_commit 7dcb1e1753e9c5daec0580779ea8c31778bff152
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
make PLATFORM=generic

%install
make PLATFORM=generic I=%{buildroot} INSTALL_LIB_PATH=lib64 install

rm -rfv %{buildroot}/lib64
rm -rfv %{buildroot}/include
rm -rfv %{buildroot}%{_datadir}/%{name}/*/firmware/payloads


%files
%license COPYING.BSD
%doc README.md
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*


%changelog
* Wed Jan 06 2021 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.8.81.2021.01.06.7dcb1e1
- New version
- Switch to generic platform
- Remove all others special Fedora variants of firmware
- Remove development library and documentation (not needed)
- Remove example payloads

* Wed Feb 19 2020 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2020.02.19.c66543d-1
- Rebuild for a new OpenSBI (incl. a fix for FU540 TLB flush issue)

* Tue Jan 07 2020 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2020.01.07.a67fd68-1
- Rebuild for a new U-Boot and kernel

* Thu Jan 02 2020 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2020.01.02.c0849cd-2
- Rebuild for new U-Boot

* Thu Jan 02 2020 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2020.01.02.c0849cd-1
- New revision of OpenSBI

* Mon Dec 30 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.12.28.c7d1b12-2
- Rebuild for new U-Boot

* Sat Dec 28 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.12.28.c7d1b12-1
- Rebuild for new kernel

* Sun Dec 15 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.12.05.813f7f4-12
- Rebuild for new kernel

* Thu Dec 06 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.12.05.813f7f4-3
- Increase stack size for (QEMU virt, sifive_u and SiFive FU540) to 16K (new default in U-Boot)

* Thu Dec 05 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.12.05.813f7f4-2
- Rebuild for new U-Boot

* Thu Dec 05 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.12.05.813f7f4-1
- New OpenSBI revision
- New U-Boot (2020.01 RC4)

* Tue Nov 19 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.11.19.215421c-1
- New OpenSBI revision
- New U-Boot

* Fri Nov 16 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.11.13.18897aa-2
- Rebuilt for new U-Boot

* Wed Nov 13 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.11.13.18897aa-1
- New OpenSBI revision
- New kernel
- New U-Boot
- Incl. a patch to enable all L2 ways on SiFive FU540 (final patch will be in FSBL)

* Wed Oct 30 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-10
- Rebuild for new U-Boot

* Tue Oct 29 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-9
- Rebuild for new U-Boot

* Mon Oct 28 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-8
- Rebuild for new U-Boot

* Mon Oct 28 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-7
- Rebuild for new U-Boot

* Wed Oct 23 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-6
- Rebuild for new kernel

* Wed Oct 23 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-5
- Update DTB patch from upstream review

* Wed Oct 23 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-4
- Fix linker error if DTB size is not 16-byte aligned

* Tue Oct 22 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-3
- Rebuild for new kernel

* Thu Oct 17 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-2
- Rebuild for new U-Boot

* Wed Oct 09 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.5.0.2019.10.09.be92da2-1
- Update to the official v0.5 OpenSBI
- Rebuild for the official U-Boot v2019.10

* Mon Sep 30 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4.42.2019.09.30.1e9f888-1
- Bump OpenSBI revision

* Thu Sep 26 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4.32.2019.09.24.98ee15c-2
- Bump Release for new U-Boot

* Fri Aug 30 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4.32.2019.09.24.98ee15c-1
- Bump OpenSBI to latest revision

* Fri Aug 30 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4.22.2019.08.24.3cbb419-4
- Rebuild for new U-Boot

* Tue Aug 27 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4.22.2019.08.24.3cbb419-3
- Rebuild for U-Boot 2019.10 RC3

* Mon Aug 26 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4.22.2019.08.24.3cbb419-2
- Add DTB for SiFive FU540 from upstream kernel

* Sat Aug 24 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4.22.2019.08.24.3cbb419-1
- Add SiFive Unleashed (FU540) U-Boot payload firmware variant

* Fri Aug 23 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> v0.4-22-g3cbb419-0
- Update OpenSBI to incl. fixes for TLB flush

* Wed Jul 03 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.07.03.ce228ee-1
- Rebuilt for kernel-5.2.0-0.rc7.git0.1.0.riscv64.fc31

* Tue Jul 02 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.07.02.ce228ee-0
- Update to OpenSBI 4.0 commit
- Might improve situation where not all cores come online if QEMU instance is
  configured with more than 2 cores

* Sat Jun 29 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.06.24.65aa587-5
- Rebuild for new U-Boot

* Sat Jun 29 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.06.24.65aa587-4
- Rebuild for new U-Boot

* Fri Jun 28 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.06.24.65aa587-3
- Rebuild for new U-Boot

* Wed Jun 26 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.06.24.65aa587-2
- Rebuild for new U-Boot

* Mon Jun 24 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.06.24.65aa587-1
- Update OpenSBI revision

* Fri Jun 21 2019 David Abdurachmanov <david.abdurachmanov@sifive.com> 2019.06.21.cd2dfdc-1
- Update OpenSBI revision (new kernel, new U-Boot)

* Mon May 06 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.05.06.243a5e0-1
- Update OpenSBI revision and rebuild for kernel-5.1.0-0.rc7.git4.1.1.riscv64.fc31

* Sun Apr 14 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.04.05.40086da-3
- Rebuild for kernel-5.1.0-0.rc4.git2.1.1.riscv64.fc31

* Mon Apr 08 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.04.05.40086da-2
- Rebuild for new uboot (SMP support)

* Fri Apr 05 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.04.05.40086da-1
- Update revision and rebuild for new u-boot

* Fri Apr 05 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.04.05.09f9768-1
- Update version and bump for new u-boot & kernel

* Sat Mar 30 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.03.30.f9cfe30-1
- Change the way we find kernel
- Add a QEMU Virt machine build with U-Boot

* Wed Mar 20 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.03.20.e921fc2-1
- Initial version
