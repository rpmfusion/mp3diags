%global  oname  MP3Diags

Name:           mp3diags
Version:        1.4.01
Release:        2%{?dist}
License:        GPLv2
Summary:        Find and fix Problems in MP3 Files
URL:            http://mp3diags.sourceforge.net
Source:         https://github.com/mciobanu/mp3diags/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         %{name}-system-lib.patch
Patch1:         %{name}-literal.patch

BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-linguist
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
%autosetup -p0 -n %{name}-%{version}
./AdjustMt.sh

%build
# Create translation files.
lrelease-qt5 src/translations/%{name}_*.ts
%{qmake_qt5}
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
%doc README.md changelog.txt
%license COPYING
%{_bindir}/%{name}
%{_bindir}/%{oname}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{oname}.png


%changelog
* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 25 2024 Martin Gansser <martinkg@fedoraproject.org> - 1.4.01-1
- Update to 1.4.01

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.03-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.03-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 02 2023 Leigh Scott <leigh123linux@gmail.com> - 1.2.03-18
- Rebuild for new boost

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.03-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.03-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 19 2021 Leigh Scott <leigh123linux@gmail.com> - 1.2.03-15
- Rebuild for new boost

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.03-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.03-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.03-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 1.2.03-11
- Rebuilt for Boost 1.73

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.03-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.03-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.03-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.03-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.2.03-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

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
