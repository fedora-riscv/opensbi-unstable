# Disable debug packages, we don't need them.
%global debug_package %{nil}

Name:		opensbi-unstable
# The last part is short hash
Version:	2019.03.20.e921fc2
Release:	1%{?dist}
Summary:	RISC-V Open Source Supervisor Binary Interface

License:	BSD
URL:		https://github.com/riscv/opensbi

# Download tarball, e.g.:
# https://github.com/riscv/opensbi/archive/%full_commit.tar.gz
%global full_commit e921fc26911bd27cf715483b60c22920812aab21
Source0:	https://github.com/riscv/riscv-pk/archive/%{full_commit}.tar.gz

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


%prep
%autosetup -n opensbi-%{full_commit}


%build
# Find Fedora kernel image in /boot
vmlinuz=$(find /boot | grep vmlinuz | grep -v -E '(rescue|hmac)')
if [[ "$vmlinuz" = *$'\n'* ]]; then
  echo "We expected to find a single file!"
  exit 1
fi

echo "Payload: $vmlinuz"

cp "$vmlinuz" Image.gz
gunzip Image.gz

make PLATFORM=qemu/virt FW_PAYLOAD_PATH="$PWD/Image"
#make docs


%install
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

# Find Fedora kernel image in /boot and extract version
vmlinuz=$(find /boot | grep vmlinuz | grep -v -E '(rescue|hmac)')
vmlinuz_version=$(echo "$vmlinuz" | cut -d'-' -f2-)

mkdir -p %{buildroot}/boot/opensbi/unstable
cp build/platform/qemu/virt/firmware/fw_jump.elf \
   %{buildroot}/boot/opensbi/unstable/fw_jump.elf
cp build/platform/qemu/virt/firmware/fw_payload.elf \
   %{buildroot}/boot/opensbi/unstable/fw_payload-${vmlinuz_version}.elf


%files
%license COPYING.BSD
%doc README.md
/boot/opensbi/unstable/fw_jump.elf

%files fedora
/boot/opensbi/unstable/fw_payload-*.elf

%files libsbi-devel
#%%doc %%{_pkgdocdir}/refman.pdf
%{_prefix}/include/sbi/*
%{_libdir}/libsbi.a

%files platform-virt
%{_datadir}/%{name}

%changelog
* Wed Mar 20 2019 David Abdurachmanov <david.abdurachmanov@gmail.com> 2019.03.20.e921fc2-1
- Initial version
