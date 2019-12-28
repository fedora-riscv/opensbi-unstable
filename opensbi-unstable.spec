# Disable debug packages, we don't need them.
%global debug_package %{nil}

Name:		opensbi-unstable
# The last part is short hash
# Format: <TAG>.<NUMBER_OF_COMMITS_AFTER_TAG>.<YEAR>.<MONTH>.<DAY>.<SHORT_COMMIT>
Version:	v0.5.0.2019.12.28.c7d1b12
Release:	1%{?dist}
Summary:	RISC-V Open Source Supervisor Binary Interface

License:	BSD
URL:		https://github.com/riscv/opensbi

# Download tarball, e.g.:
# https://github.com/riscv/opensbi/archive/%full_commit.tar.gz
%global full_commit c7d1b12199a11f8dcccb631a742eb31c79f8d0d2
Source0:	https://github.com/riscv/opensbi/archive/%{full_commit}.tar.gz

Patch0:     0001-Revert-lib-Remove-date-and-time-from-init-message.patch

BuildRequires:	systemd-udev
BuildRequires:	grubby-deprecated
BuildRequires:	gcc
BuildRequires:	binutils
BuildRequires:	findutils
BuildRequires:	grep
BuildRequires:	coreutils
BuildRequires:	kernel-core
BuildRequires:  make
BuildRequires:  dtc
BuildRequires:  gzip
BuildRequires:  file
# U-Boot binary builds for all platforms
BuildRequires:  uboot-images-riscv64
# For docs
#BuildRequires:  doxygen
#BuildRequires:  doxygen-latex
#BuildRequires:  doxygen-doxywizard
#BuildRequires:  graphviz


%description
RISC-V Open Source Supervisor Binary Interface compiled in jump variant.
This is only for QEMU RISC-V virt machine.


%package libsbi-devel
Summary: Platform independent static OpenSBI library


%description libsbi-devel
The main component of OpenSBI is provided in the form of a platform independent 
static library libsbi.a implementing the SBI interface. A firmware or bootloader 
implementation can link against this library to ensure conformance with the SBI 
interface specifications. libsbi.a also defines an interface for integrating 
with platform specific operations provided by the platform firmware 
implementation (e.g. console access functions, inter-processor interrupts 
control, etc).


%package platform-virt
Summary: QEMU virt machine platform specific artifacts


%description platform-virt
libplatsbi.a and bootloaders (ELF and binary) for QEMU virt machine.


%package fedora
Summary: OpenSBI QEMU virt machine firmware with Fedora kernel embedded


%description fedora
OpenSBI QEMU virt machine firmware with Fedora kernel embedded as payload.


%package images-riscv64
Summary: OpenSBI firmware binaries with Fedora U-Boot embedded


%description images-riscv64
OpenSBI firmware images for all supported platforms with embedded Fedora
U-Boot bootloader.

%prep
%autosetup -n opensbi-%{full_commit} -p1


%build
mkdir -p fedora-builds/{kernel,uboot-qemu-virt,uboot-sifive-fu540}
for build in kernel uboot-qemu-virt uboot-sifive-fu540; do
    cp -r $(ls -1 | grep -v fedora-builds) "fedora-builds/$build"
done

# BUILD: kernel
pushd fedora-builds/kernel

latestKernel=$(ls -1t /lib/modules/*/vmlinuz | head -n1)

file "$latestKernel"

echo "Payload: $latestKernel"

# Kernel is built with Image.gz target, we need to unpack before embedding it
# into OpenSBI
cp "$latestKernel" Image.gz
gunzip Image.gz

dtbFile=$(echo /boot/dtb-*/sifive/hifive-unleashed-a00.dtb)
file $dtbFile

make PLATFORM=sifive/fu540 FW_OPTIONS=0x2 FW_PAYLOAD_FDT_PATH="$dtbFile" FW_PAYLOAD_PATH="$PWD/Image"
#make docs

# BUILD: kernel
popd

# BUILD: uboot-qemu-virt
pushd fedora-builds/uboot-qemu-virt

ubootFile=/usr/share/uboot/qemu-riscv64_smode/u-boot.bin
file $ubootFile
make PLATFORM=qemu/virt FW_OPTIONS=0x2 FW_PAYLOAD_PATH="$ubootFile"

# BUILD: uboot-qemu-virt
popd

# BUILD: uboot-sifive-fu540
pushd fedora-builds/uboot-sifive-fu540

ubootFile=/usr/share/uboot/sifive_fu540/u-boot.bin
# We only have one kernel installed in buildroot
dtbFile=$(echo /boot/dtb-*/sifive/hifive-unleashed-a00.dtb)
#dtbFile=$(find /boot/dtb-*/sifive -type f -name hifive-unleashed-a00.dtb -print -quit 2>/dev/null)
file $ubootFile
file $dtbFile
make PLATFORM=sifive/fu540 FW_OPTIONS=0x2 FW_PAYLOAD_PATH="$ubootFile" FW_PAYLOAD_FDT_PATH="$dtbFile"

# BUILD: uboot-sifive-fu540
popd

%install
# BUILD: kernel
pushd fedora-builds/kernel

make PLATFORM=qemu/virt I=%{buildroot} install
#make I=%{buildroot} install_docs

mkdir -p %{buildroot}%{_usr}
mv %{buildroot}/lib %{buildroot}%{_libdir}
mv %{buildroot}/include %{buildroot}%{_usr}/

mkdir -p %{buildroot}%{_datadir}/%{name}
mv %{buildroot}/platform %{buildroot}%{_datadir}/%{name}/

#mkdir -p %{buildroot}%{_pkgdocdir}
#mv %{buildroot}/docs/refman.pdf %{buildroot}%{_pkgdocdir}/
#rm -rf %{buildroot}/docs

latestKernelVersion=$(ls -1t /lib/modules/*/vmlinuz | head -n1 | cut -d'/' -f4)

mkdir -p %{buildroot}/boot/opensbi/unstable
cp build/platform/sifive/fu540/firmware/fw_jump.elf \
   %{buildroot}/boot/opensbi/unstable/fw_jump.elf
cp build/platform/sifive/fu540/firmware/fw_jump.bin \
   %{buildroot}/boot/opensbi/unstable/fw_jump.bin
cp build/platform/sifive/fu540/firmware/fw_payload.elf \
   %{buildroot}/boot/opensbi/unstable/fw_payload-${latestKernelVersion}.elf
cp build/platform/sifive/fu540/firmware/fw_payload.bin \
   %{buildroot}/boot/opensbi/unstable/fw_payload-${latestKernelVersion}.bin

# BUILD: kernel
popd

# BUILD: uboot-qemu-virt
pushd fedora-builds/uboot-qemu-virt

cp build/platform/qemu/virt/firmware/fw_payload.elf \
   %{buildroot}/boot/opensbi/unstable/fw_payload-uboot-qemu-virt-smode.elf
cp build/platform/qemu/virt/firmware/fw_payload.bin \
   %{buildroot}/boot/opensbi/unstable/fw_payload-uboot-qemu-virt-smode.bin

# BUILD: uboot-qemu-virt
popd

# BUILD: uboot-sifive-fu540
pushd fedora-builds/uboot-sifive-fu540

cp build/platform/sifive/fu540/firmware/fw_payload.elf \
   %{buildroot}/boot/opensbi/unstable/fw_payload-uboot-sifive-fu540.elf
cp build/platform/sifive/fu540/firmware/fw_payload.bin \
   %{buildroot}/boot/opensbi/unstable/fw_payload-uboot-sifive-fu540.bin

# BUILD: uboot-sifive-fu540
popd


%files
%license COPYING.BSD
%doc README.md
/boot/opensbi/unstable/fw_jump.{bin,elf}

%files fedora
/boot/opensbi/unstable/fw_payload-*.{bin,elf}
%exclude /boot/opensbi/unstable/fw_payload-uboot-qemu-virt-smode.{bin,elf}

%files libsbi-devel
#%%doc %%{_pkgdocdir}/refman.pdf
%{_prefix}/include/sbi/*
%{_prefix}/include/sbi_utils/*
%{_libdir}/libsbi.a
%{_libdir}/libsbiutils.a

%files platform-virt
%{_datadir}/%{name}

%files images-riscv64
/boot/opensbi/unstable/fw_payload-uboot-qemu-virt-smode.{bin,elf}
/boot/opensbi/unstable/fw_payload-uboot-sifive-fu540.{bin,elf}

%changelog
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
