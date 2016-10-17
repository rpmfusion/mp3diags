%global oname   MP3Diags

Name:           mp3diags
Version:        1.2.03
Release:        2%{?dist}
License:        GPLv2
Summary:        Find and fix Problems in MP3 Files
URL:            http://mp3diags.sourceforge.net
Source:         http://prdownloads.sourceforge.net/mp3diags/MP3Diags-%{version}.tar.gz
Patch0:         mp3diags-system-lib.patch

BuildRequires:  boost-devel
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
%autosetup -p0 -n "MP3Diags-%{version}"
./AdjustMt.sh

%build
# Create translation files.
lrelease-qt4 src/translations/mp3diags_*.ts
%{qmake_qt4}
%make_build

%install
# main executable
install -D -m0755 bin/%{oname} %{buildroot}%{_bindir}/%{oname}
ln -s MP3Diags "%{buildroot}%{_bindir}/mp3diags"

install -D -m0644 desktop/MP3Diags.desktop "%{buildroot}%{_datadir}/applications/%{name}.desktop"

# icons
for i in "16" "22" "24" "32" "36" "40" "48"; do
        mkdir -p "%{buildroot}/%{_datadir}/icons/hicolor/${i}x${i}/apps"
        install -p -m644 "desktop/MP3Diags${i}.png" "%{buildroot}/%{_datadir}/icons/hicolor/${i}x${i}/apps/MP3Diags.png"
done

mkdir -p %{buildroot}/usr/share/%{name}/translations
install -p -m644 src/translations/*.qm %{buildroot}/%{_datadir}/%{name}/translations
%find_lang %{name} --with-qt

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%doc README.TXT changelog.txt
%license license.boost.* COPYING
%{_bindir}/mp3diags
%{_bindir}/MP3Diags
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/MP3Diags.png
%dir %{_datadir}/%{name} 
%dir %{_datadir}/%{name}/translations

%changelog
* Thu Oct 13 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.2.03-2
- remove BR make gcc-c++

* Sat Jul 30 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.2.03-1
- initial build