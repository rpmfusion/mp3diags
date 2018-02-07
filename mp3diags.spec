%global  oname  MP3Diags

Name:           mp3diags
Version:        1.2.03
Release:        5%{?dist}
License:        GPLv2
Summary:        Find and fix Problems in MP3 Files
URL:            http://mp3diags.sourceforge.net
Source:         http://prdownloads.sourceforge.net/%{name}/%{oname}-%{version}.tar.gz
Patch0:         %{name}-system-lib.patch
Patch1:         %{name}-literal.patch

BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  qt4-devel
BuildRequires:  zlib-devel
BuildRequires:  glibc-devel
BuildRequires:  lame-devel
Requires:       hicolor-icon-theme
Requires:       mp3gain

%description
MP3 Diags finds problems in MP3 files and helps the user fix many of them. It
looks at both the audio part (VBR info, quality, normalization) and the tags
containing track information (ID3). It has a tag editor, which can download
album information (including cover art) from MusicBrainz and Discogs, as well
as paste data from the clipboard. Track information can also be extracted from
a file's name. Another component is the file renamer, which can rename files
based on the fields in their ID3V2 tag (artist, track number, album, genre,
etc.).

%prep
%autosetup -p0 -n %{oname}-%{version}
./AdjustMt.sh

%build
# Create translation files.
lrelease-qt4 src/translations/%{name}_*.ts
%{qmake_qt4}
%make_build

%install
install -D -m0755 bin/%{oname} %{buildroot}%{_bindir}/%{oname}
ln -s MP3Diags %{buildroot}%{_bindir}/%{name}

install -D -m0644 desktop/%{oname}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

# icons
for i in "16" "22" "24" "32" "36" "40" "48"; do
        mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
        install -p -m644 desktop/%{oname}${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{oname}.png
done

mkdir -p %{buildroot}%{_datadir}/%{name}/translations
install -p -m644 src/translations/*.qm %{buildroot}%{_datadir}/%{name}/translations
%find_lang %{name} --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{name}.lang
%doc README.TXT changelog.txt
%license license.*.txt COPYING
%{_bindir}/%{name}
%{_bindir}/%{oname}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{oname}.png
%{_datadir}/%{name}/


%changelog
* Wed Feb 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.2.03-5
- Rebuild for boost-1.66
- Remove scriptlets

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.2.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 24 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.2.03-3
- Add %%{name}-literal.patch

* Thu Oct 13 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.2.03-2
- Remove BR make gcc-c++

* Sat Jul 30 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.2.03-1
- Initial build
