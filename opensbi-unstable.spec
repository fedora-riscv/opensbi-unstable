# Disable debug packages, we don't need them.
%global debug_package %{nil}

Name:		opensbi-unstable
# The last part is short hash
Version:	2019.03.30.f9cfe30
Release:	1%{?dist}
Summary:	RISC-V Open Source Supervisor Binary Interface

License:	BSD
URL:		https://github.com/riscv/opensbi

# Download tarball, e.g.:
# https://github.com/riscv/opensbi/archive/%full_commit.tar.gz
%global full_commit f9cfe301c92aede87e46069e66e250d4039e413e
Source0:	https://github.com/riscv/opensbi/archive/%{full_commit}.tar.gz

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
%autosetup -n opensbi-%{full_commit}


%build
mkdir -p fedora-builds/{kernel,uboot-qemu-virt}
for build in kernel uboot-qemu-virt; do
    cp -r $(ls -1 | grep -v fedora-builds) "fedora-builds/$build"
done

# BUILD: kernel
pushd fedora-builds/kernel

# Use klist.txt to find the latest installed kernel
[ -f /etc/sysconfig/uboot ] && . /etc/sysconfig/uboot

ubootDir=${UBOOT_DIR:-"/boot"}
ubootKList=${UBOOT_KLIST:-"klist.txt"}

if [ ! -f $ubootDir/$ubootKList ]; then
    echo "U-Boot klist was not found! Cannot locate latest installed kernel image!"
    exit 1
fi

latestKernel="/lib/modules/$(tail -n1 "$ubootDir/$ubootKList")/vmlinuz"

file "$latestKernel"

echo "Payload: $latestKernel"

# Kernel is built with Image.gz target, we need to unpack before embedding it
# into OpenSBI
cp "$latestKernel" Image.gz
gunzip Image.gz

make PLATFORM=qemu/virt FW_PAYLOAD_PATH="$PWD/Image"
#make docs

# BUILD: kernel
popd

# BUILD: uboot-qemu-virt
pushd fedora-builds/uboot-qemu-virt

ubootFile=/usr/share/uboot/qemu-riscv64_smode/u-boot.bin
file $ubootFile
make PLATFORM=qemu/virt FW_PAYLOAD_PATH="$ubootFile"

# BUILD: uboot-qemu-virt
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

# Use klist.txt to find the latest installed kernel
[ -f /etc/sysconfig/uboot ] && . /etc/sysconfig/uboot

ubootDir=${UBOOT_DIR:-"/boot"}
ubootKList=${UBOOT_KLIST:-"klist.txt"}
latestKernelVersion=$(tail -n1 "$ubootDir/$ubootKList")


mkdir -p %{buildroot}/boot/opensbi/unstable
cp build/platform/qemu/virt/firmware/fw_jump.elf \
   %{buildroot}/boot/opensbi/unstable/fw_jump.elf
cp build/platform/qemu/virt/firmware/fw_payload.elf \
   %{buildroot}/boot/opensbi/unstable/fw_payload-${latestKernelVersion}.elf

# BUILD: kernel
popd

# BUILD: uboot-qemu-virt
pushd fedora-builds/uboot-qemu-virt

cp build/platform/qemu/virt/firmware/fw_payload.elf \
   %{buildroot}/boot/opensbi/unstable/fw_payload-uboot-qemu-virt-smode.elf

# BUILD: uboot-qemu-virt
popd

%files
%license COPYING.BSD
%doc README.md
/boot/opensbi/unstable/fw_jump.elf

%files fedora
/boot/opensbi/unstable/fw_payload-*.elf
%exclude /boot/opensbi/unstable/fw_payload-uboot-qemu-virt-smode.elf

%files libsbi-devel
#%%doc %%{_pkgdocdir}/refman.pdf
%{_prefix}/include/sbi/*
%{_libdir}/libsbi.a

%files platform-virt
%{_datadir}/%{name}

%files images-riscv64
/boot/opensbi/unstable/fw_payload-uboot-qemu-virt-smode.elf

%changelog
* Sat Mar 30 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.03.30.f9cfe30-1
- Change the way we find kernel
- Add a QEMU Virt machine build with U-Boot

* Wed Mar 20 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.03.20.e921fc2-1
- Initial version
