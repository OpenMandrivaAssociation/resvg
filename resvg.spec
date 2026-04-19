%define soname  0

Name:           resvg
Version:        0.47.0
Release:        1
Summary:        SVG rendering library
License:        Apache-2.0 OR MIT
Group:          Productivity/Graphics/Convertors
URL:            https://github.com/linebender/resvg
Source0:        https://github.com/linebender/resvg/releases/download/v%{version}/%{name}-%{version}.tar.xz
#Source1:        vendor.tar.zst
BuildRequires:  rust-packaging
BuildRequires:  zstd

%description
resvg is an SVG rendering library.
It can be used as a Rust library, as a C library, and as a CLI
application to render static SVG files.
The core idea is to make a fast, small, portable SVG library with the goal to
support the whole SVG spec.
Features:
* Designed for edge-cases
* Safety
* Zero bloat
* Portable
* SVG preprocessing
* Performance
* Reproducibility

%package -n usvg
Summary:        SVG simplification tool
Group:          Productivity/Graphics/Convertors

%description -n usvg
usvg is a command-line utility to simplify SVG files based on a static
SVG Full 1.1 subset. It converts an input SVG to an extremely
simple representation, which is still a valid SVG:
* No basic shapes (rect, circle, etc), only paths
* Only simple paths
* All supported attributes are resolved
* Invisible elements are removed
* Comments will be removed
* DTD will be resolved
* CSS will be resolved
and so on.

%package -n lib%{name}%{soname}
Summary:        SVG rendering library (C++/Qt API)
Group:          Development/Libraries/C and C++

%description -n lib%{name}%{soname}
An SVG rendering library (C++/Qt API).
This package contains shared library.

%package devel
Summary:        SVG rendering library (C++/Qt API)
Group:          Development/Libraries/C and C++
Requires:       lib%{name}%{soname} = %{version}-%{release}

%description devel
An SVG rendering library (C++/Qt API).
This package contains development files for %{name}.

%package devel-static
Summary:        SVG rendering library (C++/Qt API)
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel = %{version}-%{release}

%description devel-static
An SVG rendering library (C++/Qt API).
This package contains development files for %{name}.

It contains static libraries for -static linking which is highly discouraged.

%prep
%autosetup -p1
%cargo_prep -v vendor

%build
#global build_rustflags  -Clink-arg=-Wl,-z,relro,-z,now,-soname,libresvg.so.%{soname} -C debuginfo=2 -C strip=none
cargo build --all

%install
#cargo install resvg usvg
install -Dm 0755 ./target/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 0755 ./target/release/usvg %{buildroot}%{_bindir}/usvg
install -Dm 0755 ./target/release/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so.%{version}
ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so.%{soname}
ln -sf lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so
install -Dm 0644 ./target/release/lib%{name}.a %{buildroot}%{_libdir}/lib%{name}.a
install -Dm 0644 ./crates/c-api/*.h -t %{buildroot}%{_includedir}/

%files
%doc AUTHORS CHANGELOG.md README.md
%{_bindir}/%{name}
%license LICENSE-APACHE LICENSE-MIT

%files -n usvg
%{_bindir}/usvg

%files -n lib%{name}%{soname}
%{_libdir}/lib%{name}.so.*

%files devel
%{_libdir}/lib%{name}.so
%{_includedir}/%{name}.h
%{_includedir}/ResvgQt.h

%files devel-static
%{_libdir}/lib%{name}.a
