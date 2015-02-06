# Copyright (c) 2006-2008 oc2pus
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments to toni@links2linux.de

# norootforbuild

%define debug_package %{nil}

Summary:	The port of Descent 2 for Linux
Name:		d2x-rebirth
Version:	0.58.1
Release:	2
License:	GPL
Group:		Games/Arcade
URL:		http://www.dxx-rebirth.com/
Source:		http://www.dxx-rebirth.com/download/dxx/%{name}_v%{version}-src.tar.gz
Source1:	%{name}.png
Source2:	D2XBDE01.zip
BuildRequires:	dos2unix
BuildRequires:	gcc-c++
BuildRequires:	nasm
BuildRequires:	scons
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(SDL_mixer)
BuildRequires:	physfs-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	unzip
Requires:	physfs

%description
This is the port of Descent 2, the famous 3D game for PC.

D2X is based on source code that was released the 14 December 1999 by
Parallax Software Corporation.

To use this package you'll need some datafiles installed in
/usr/share/games/descent2. See dxx-readme.txt.

%package sdl
Group:		Games/Arcade
Summary:	Descent 2 for Linux, SDL version
Requires:	d2x-rebirth = %{version}
Conflicts:	d2x-rebirth-gl

%description sdl
This is the port of Descent 2, the famous 3D game for PC.

D2X is based on source code that was released the 14 December 1999
by Parallax Software Corporation.

To use this package you'll need some datafiles installed in
/usr/share/games/descent2. See dxx-readme.txt.

This version uses SDL for Audio, Input/Output and graphics
rendering.

%package gl
Group:		Games/Arcade
Summary:	Descent 2 for Linux, OpenGL version
Requires:	d2x-rebirth = %{version}
Conflicts:	d2x-rebirth-sdl

%description gl
This is the port of Descent 2, the famous 3D game for PC.

D2X is based on source code that was released the 14 December 1999 by
Parallax Software Corporation.

To use this package you'll need some datafiles installed in
/usr/share/games/descent2.  See dxx-readme.txt.

This version uses SDL for Audio and Input/Output and OpenGL for
graphics rendering.


%prep
%setup -q -n %{name}_v%{version}-src -a2
dos2unix     d2x.ini *.txt
%__chmod 644 d2x.ini *.txt
dos2unix CHANGELOG.txt

%build
# d2x-sdl
scons %{?jobs:-j%{jobs}} \
	sharepath=%{_gamesdatadir}/descent2 \
	sdl_only=1 \
	sdlmixer=1 \
	no_asm=1
mv d2x-rebirth d2x-rebirth-sdl

# d2x-gl
scons -c
scons %{?jobs:-j%{jobs}} \
	sharepath=%{_gamesdatadir}/descent2 \
	sdlmixer=1 \
	PREFIX=%{buildroot}%{_prefix}
cp d2x-rebirth d2x-rebirth-gl

%install
# binaries
install -dm 755 %{buildroot}%{_prefix}/games/
install -m 755 d2x-rebirth  \
	%{buildroot}%{_prefix}/games/d2x-rebirth-gl
install -m 755 d2x-rebirth-sdl \
	%{buildroot}%{_prefix}/games/

install -dm 755 %{buildroot}%{_datadir}/games/descent2
# german translations
install -m 644 D2XBDE01/D2XbDE01/*.txb \
	%{buildroot}%{_datadir}/games/descent2
install -m 644 D2XBDE01/*.txt \
	%{buildroot}%{_datadir}/games/descent2
# directory for original descent data
install -dm 755 %{buildroot}%{_datadir}/games/descent2/missions

# man-pages
install -dm 755 %{buildroot}%{_mandir}/man1/
install  -m 644 libmve/*.1 \
	%{buildroot}%{_mandir}/man1/

# icon
install -dm 755 %{buildroot}%{_datadir}/pixmaps
install -m 644 %{SOURCE1} \
	%{buildroot}%{_datadir}/pixmaps

# menu
install -dm 755 %{buildroot}%{_datadir}/applications
cat > %{name}-sdl.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=D2x (SDL version)
Comment=The port of Descent 2 for Linux
Exec=%{_prefix}/games/d2x-rebirth-sdl
Icon=%{name}
Categories=Game;ActionGame;
EOF
install -m 644 %{name}-sdl.desktop \
	%{buildroot}%{_datadir}/applications

cat > %{name}-gl.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=D2x (OpenGL version)
Comment=The port of Descent 2 for Linux
Exec=%{_prefix}/games/d2x-rebirth-gl
Icon=%{name}
Categories=Game;ArcadeGame;
EOF
install -m 644 %{name}-gl.desktop \
	%{buildroot}%{_datadir}/applications

%files
%doc *.txt *.plist *.ini
%dir %{_datadir}/games/descent2
%{_datadir}/games/descent2/*.txb
%{_datadir}/games/descent2/*.txt
%dir %{_datadir}/games/descent2/missions
%{_mandir}/man1/*
%{_datadir}/pixmaps/%{name}.png

%files sdl
%doc COPYING*
%{_prefix}/games/d2x-rebirth-sdl
%{_datadir}/applications/%{name}-sdl.desktop

%files gl
%doc COPYING*
%{_prefix}/games/d2x-rebirth-gl
%{_datadir}/applications/%{name}-gl.desktop

