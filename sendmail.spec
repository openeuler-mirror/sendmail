Name:          sendmail
Version:       8.16.1
Release:       8
Summary:       A classic mail transfer agent from the Unix world
License:       Sendmail
URL:           http://www.sendmail.org/
Source0:       http://ftp.sendmail.org/sendmail.%{version}.tar.gz
Source1:       sendmail.service
Source2:       sendmail.nm-dispatcher
Source3:       sendmail.etc-mail-make
Source4:       sendmail.sysconfig
Source5:       sendmail.etc-mail-Makefile
Source6:       sm-client.service
Source7:       sendmail.pam
Source8:       Sendmail-sasl2.conf
Source9:       sendmail-redhat.mc
Source10:      sendmail-etc-mail-virtusertable
Source11:      sendmail-etc-mail-access
Source12:      sendmail-etc-mail-domaintable
Source13:      sendmail-etc-mail-local-host-names
Source14:      sendmail-etc-mail-mailertable
Source15:      sendmail-etc-mail-trusted-users

BuildRequires: openssl-devel openldap-devel libnsl2-devel gdbm-devel
BuildRequires: cyrus-sasl-devel groff ghostscript m4 systemd setup >= 2.5.31-1
Requires:      bash >= 2.0 setup >= 2.5.31-1 %{_sbindir}/saslauthd 
Requires:      procmail
Requires(pre): shadow-utils
Requires(post): systemd systemd-sysv coreutils %{_sbindir}/alternatives openssl
Requires(preun): systemd %{_sbindir}/alternatives
Requires(postun): systemd coreutils %{_sbindir}/alternatives

Provides:      MTA smtpdaemon server(smtp)
Provides:      sendmail-cf
Obsoletes:     sendmail-cf

Patch0:        sendmail-8.14.4-makemapman.patch
Patch1:        sendmail-8.14.9-pid.patch
Patch2:        sendmail-8.15.1-manpage.patch
Patch3:        sendmail-8.16.1-dynamic.patch
Patch4:        sendmail-8.13.0-cyrus.patch
Patch5:        sendmail-8.16.1-aliases_dir.patch
Patch6:        sendmail-8.14.9-noversion.patch
Patch7:        sendmail-8.15.2-localdomain.patch
Patch8:        sendmail-8.14.3-sharedmilter.patch
Patch9:        sendmail-8.15.2-switchfile.patch
Patch10:       sendmail-8.14.8-sasl2-in-etc.patch
Patch11:       sendmail-8.16.1-qos.patch
Patch12:       sendmail-8.15.2-libmilter-socket-activation.patch
Patch13:       sendmail-8.15.2-openssl-1.1.0-fix.patch
Patch14:       sendmail-8.15.2-format-security.patch

%description
Sendmail is a general purpose internetwork email routing facility that
supports many kinds of mail-transfer and delivery methods, including
the Simple Mail Transfer Protocol (SMTP) used for email transport over
the Internet. It also includes the configuration files you need to generate
the sendmail.cf file distributed with the sendmail package.

%package   help
Summary:   Help document for the Sendmail Mail Transport Agent program
BuildArch: noarch
Requires:  sendmail = %{version}-%{release}
Provides:  sendmail-doc
Obsoletes: sendmail-doc

%description help
This package contains the Sendmail Installation and Operation Guide,
text files containing configuration documentation, plus a number of
scripts and tools for using with Sendmail.

%package   -n libmilter
Summary:   The sendmail milter library
Provides:  sendmail-milter sendmail-devel = %{version}-%{release}
Obsoletes: sendmail-milter sendmail-devel < 8.15.2-8

%description -n libmilter
The Sendmail Content Management API (Milter) is designed to allow third-party
programs access to mail messages as they are being processed in order to
filter meta-information and content. It includes the milter shared library.

%package   -n libmilter-devel
Summary:   Sendmail milter development libraries and headers
Requires:  libmilter = %{version}-%{release}
Provides:  sendmail-milter-devel
Obsoletes: sendmail-milter-devel

%description -n libmilter-devel
Include development libraries and headers for the milter add-ons as part of sendmail.

%prep
%setup -q
cp devtools/M4/UNIX/library.m4 devtools/M4/UNIX/sharedlibrary.m4
%autopatch -p1

%build
export CFLAGS="${RPM_OPT_FLAGS}"

cat << EOF > config.m4
define(\`confMAPDEF', \`-DNDBM -DNIS -DMAP_REGEX -DSOCKETMAP -DNAMED_BIND=1')
define(\`confOPTIMIZE', \`\`\`\`${RPM_OPT_FLAGS}'''')
define(\`confLIBS', \`-lgdbm -lgdbm_compat -lnsl -lcrypt -lresolv')
define(\`confSTDIR', \`%{_localstatedir}/log/mail')
define(\`confLDOPTS', \`-Xlinker -z -Xlinker relro -Xlinker -z -Xlinker now')
define(\`confMANOWN', \`root')
define(\`confMANGRP', \`root')
define(\`confENVDEF', \`-I/usr/kerberos/include -Wall -DXDEBUG=0')
define(\`confLIBDIRS', \`-L/usr/kerberos/%{_lib}')
define(\`confMANMODE', \`644')
define(\`confMAN1SRC', \`1')
define(\`confMAN5SRC', \`5')
define(\`confMAN8SRC', \`8')
define(\`STATUS_FILE', \`%{_localstatedir}/log/mail/statistics')
define(\`confLIBSEARCH', \`resolv 44bsd')
EOF
#'

cat << EOF  >> config.m4
APPENDDEF(\`confLIBS', \`-pie')
APPENDDEF(\`confLIBS', \`-lsasl2 -lcrypto')dnl
APPENDDEF(\`confLIBS', \`-lldap -llber -lssl -lcrypto')dnl
APPENDDEF(\`confENVDEF', \`-DNETINET6 -DHES_GETMAILHOST -DUSE_VENDOR_CF_PATH=1 -D_FFR_LINUX_MHNLi')dnl
APPENDDEF(\`confENVDEF', \`-D_FFR_QOS -D_FILE_OFFSET_BITS=64')dnl
APPENDDEF(\`confENVDEF', \`-DSASL=2')dnl
APPENDDEF(\`confENVDEF', \`-D_FFR_MILTER_CHECK_REJECTIONS_TOO')dnl
APPENDDEF(\`confMAPDEF', \`-DLDAPMAP -DLDAP_DEPRECATED')dnl
APPENDDEF(\`confENVDEF', \`-DSM_CONF_LDAP_MEMFREE=1')dnl
APPENDDEF(\`confOPTIMIZE', \`')
APPENDDEF(\`confOPTIMIZE', \`-fpie')
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DMILTER')dnl
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DSTARTTLS -D_FFR_TLS_1 -D_FFR_TLS_EC -D_FFR_TLS_USE_CERTIFICATE_CHAIN_FILE')dnl
APPENDDEF(\`conf_sendmail_LIBS', \`-lssl -lcrypto')dnl
EOF

for dir in libsmutil sendmail mailstats rmail praliases smrsh makemap editmap libmilter; do
    cd $dir
    sh ./Build -f ../config.m4
    cd ..
done

make -C doc/op op.pdf

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mail
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/mail
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sendmail-cf
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man{1,5,8}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/spool/{clientmqueue,mqueue}
mkdir -p $RPM_BUILD_ROOT%{_docdir}/sendmail/contrib
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/{smrsh,sysconfig,pam.d,sasl2}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher.d
mkdir -p $RPM_BUILD_ROOT%{_includedir}/libmilter

%define USER  `id -nu`
%define GROUP `id -ng`
sendmail_make()  {
   make  $@ \
       DESTDIR=$RPM_BUILD_ROOT           \
       LIBDIR=%{_libdir}                 \
       MANROOT=%{_mandir}/man            \
       LIBMODE=0755    INCMODE=0644      \
       MSPQOWN=%{USER} CFMODE=0644       \
       CFOWN=%{USER}   CFGRP=%{GROUP}    \
       SBINOWN=%{USER} SBINGRP=%{GROUP}  \
       UBINOWN=%{USER} UBINGRP=%{GROUP}  \
       MANOWN=%{USER}  MANGRP=%{GROUP}   \
       INCOWN=%{USER}  INCGRP=%{GROUP}   \
       LIBOWN=%{USER}  LIBGRP=%{GROUP}   \
       GBINOWN=%{USER} GBINGRP=%{GROUP}
}

MAKEDIR=obj.$(uname -s).$(uname -r).$(uname -m)

sendmail_make -C $MAKEDIR/rmail force-install
for dir in sendmail mailstats praliases smrsh makemap editmap libmilter ; do
    sendmail_make -C $MAKEDIR/$dir install
done
ln -sf ../sbin/makemap           $RPM_BUILD_ROOT%{_bindir}/makemap
ln -sf ../sbin/sendmail.sendmail $RPM_BUILD_ROOT/usr/lib/sendmail.sendmail

for dir in hoststat mailq newaliases purgestat ; do
    ln -sf ../sbin/sendmail.sendmail $RPM_BUILD_ROOT%{_bindir}/$dir
done

install -p -m 644 {FAQ,KNOWNBUGS,LICENSE,RELEASE_NOTES}    $RPM_BUILD_ROOT%{_docdir}/sendmail
install -p -m 644 {README,doc/op/op.pdf,sendmail/SECURITY} $RPM_BUILD_ROOT%{_docdir}/sendmail

install -p -m 644 sendmail/README   $RPM_BUILD_ROOT%{_docdir}/sendmail/README.sendmail
install -p -m 644 smrsh/README      $RPM_BUILD_ROOT%{_docdir}/sendmail/README.smrsh
install -p -m 644 libmilter/README  $RPM_BUILD_ROOT%{_docdir}/sendmail/README.libmilter
install -p -m 644 cf/README         $RPM_BUILD_ROOT%{_docdir}/sendmail/README.cf
install -p -m 644 contrib/*         $RPM_BUILD_ROOT%{_docdir}/sendmail/contrib
gzip -9                             $RPM_BUILD_ROOT%{_docdir}/sendmail/RELEASE_NOTES

cp -ar cf/* $RPM_BUILD_ROOT%{_datadir}/sendmail-cf
rm -rf      $RPM_BUILD_ROOT%{_datadir}/sendmail-cf/cf/{README,Build.*}
rm -rf      $RPM_BUILD_ROOT%{_datadir}/sendmail-cf/*/*.m{c,4}.*

install -p -m 644 cf/cf/submit.mc $RPM_BUILD_ROOT%{_sysconfdir}/mail/submit.mc
install -p -m 644 %{SOURCE1}      $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 %{SOURCE6}      $RPM_BUILD_ROOT%{_unitdir}
install -p -m 755 %{SOURCE2}      $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/dispatcher.d/10-sendmail
install -p -m 644 %{SOURCE4}      $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sendmail
install -p -m 644 %{SOURCE7}      $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/smtp.sendmail
install -p -m 644 %{SOURCE8}      $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/Sendmail.conf
install -p -m 755 %{SOURCE3}      $RPM_BUILD_ROOT%{_sysconfdir}/mail/make
install -p -m 644 %{SOURCE5}      $RPM_BUILD_ROOT%{_sysconfdir}/mail/Makefile
install -p -m 644 %{SOURCE9}      $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.mc
install -p -m 644 %{SOURCE10}     $RPM_BUILD_ROOT%{_sysconfdir}/mail/virtusertable
install -p -m 644 %{SOURCE11}     $RPM_BUILD_ROOT%{_sysconfdir}/mail/access
install -p -m 644 %{SOURCE12}     $RPM_BUILD_ROOT%{_sysconfdir}/mail/domaintable
install -p -m 644 %{SOURCE13}     $RPM_BUILD_ROOT%{_sysconfdir}/mail/local-host-names
install -p -m 644 %{SOURCE14}     $RPM_BUILD_ROOT%{_sysconfdir}/mail/mailertable
install -p -m 644 %{SOURCE15}     $RPM_BUILD_ROOT%{_sysconfdir}/mail/trusted-users

sed -i -e 's|@@PATH@@|%{_datadir}/sendmail-cf|' $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.mc
sed -i -e 's|@@PATH@@|cf|'     %{SOURCE9}
m4 %{SOURCE9} > $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.cf
chmod 644       $RPM_BUILD_ROOT%{_sysconfdir}/mail/sendmail.cf

for map in virtusertable access domaintable mailertable ; do
    touch     $RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}.db
    chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/mail/${map}.db
done

touch $RPM_BUILD_ROOT%{_sysconfdir}/mail/aliasesdb-stamp
touch $RPM_BUILD_ROOT%{_localstatedir}/spool/clientmqueue/sm-client.st

chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/mail/helpfile
chmod 755 $RPM_BUILD_ROOT%{_sbindir}/{mailstats,makemap,editmap,praliases,sendmail,smrsh}
chmod 755 $RPM_BUILD_ROOT%{_bindir}/rmail

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/sasl2

mv    $RPM_BUILD_ROOT%{_sbindir}/sendmail         $RPM_BUILD_ROOT%{_sbindir}/sendmail.sendmail
mv    $RPM_BUILD_ROOT%{_sbindir}/makemap          $RPM_BUILD_ROOT%{_sbindir}/makemap.sendmail
mv    $RPM_BUILD_ROOT%{_sbindir}/editmap          $RPM_BUILD_ROOT%{_sbindir}/editmap.sendmail
mv    $RPM_BUILD_ROOT%{_bindir}/mailq             $RPM_BUILD_ROOT%{_bindir}/mailq.sendmail
mv    $RPM_BUILD_ROOT%{_bindir}/rmail             $RPM_BUILD_ROOT%{_bindir}/rmail.sendmail
mv    $RPM_BUILD_ROOT%{_bindir}/newaliases        $RPM_BUILD_ROOT%{_bindir}/newaliases.sendmail
touch $RPM_BUILD_ROOT%{_sbindir}/sendmail
touch $RPM_BUILD_ROOT%{_sbindir}/makemap
touch $RPM_BUILD_ROOT%{_sbindir}/editmap
touch $RPM_BUILD_ROOT%{_bindir}/mailq
touch $RPM_BUILD_ROOT%{_bindir}/rmail
touch $RPM_BUILD_ROOT%{_bindir}/newaliases

mv    $RPM_BUILD_ROOT%{_mandir}/man1/mailq.1      $RPM_BUILD_ROOT%{_mandir}/man1/mailq.sendmail.1
mv    $RPM_BUILD_ROOT%{_mandir}/man1/newaliases.1 $RPM_BUILD_ROOT%{_mandir}/man1/newaliases.sendmail.1
mv    $RPM_BUILD_ROOT%{_mandir}/man5/aliases.5    $RPM_BUILD_ROOT%{_mandir}/man5/aliases.sendmail.5
mv    $RPM_BUILD_ROOT%{_mandir}/man8/sendmail.8   $RPM_BUILD_ROOT%{_mandir}/man8/sendmail.sendmail.8
mv    $RPM_BUILD_ROOT%{_mandir}/man8/rmail.8      $RPM_BUILD_ROOT%{_mandir}/man8/rmail.sendmail.8
mv    $RPM_BUILD_ROOT%{_mandir}/man8/makemap.8    $RPM_BUILD_ROOT%{_mandir}/man8/makemap.sendmail.8
mv    $RPM_BUILD_ROOT%{_mandir}/man8/editmap.8    $RPM_BUILD_ROOT%{_mandir}/man8/editmap.sendmail.8
touch $RPM_BUILD_ROOT%{_mandir}/man1/mailq.1
touch $RPM_BUILD_ROOT%{_mandir}/man1/newaliases.1
touch $RPM_BUILD_ROOT%{_mandir}/man5/aliases.5
touch $RPM_BUILD_ROOT%{_mandir}/man8/sendmail.8
touch $RPM_BUILD_ROOT%{_mandir}/man8/rmail.8
touch $RPM_BUILD_ROOT%{_mandir}/man8/makemap.8
touch $RPM_BUILD_ROOT%{_mandir}/man8/editmap.8
touch $RPM_BUILD_ROOT/usr/lib/sendmail
touch $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/smtp

for m in man8/hoststat.8 man8/purgestat.8; do
    [ -f %{buildroot}%{_mandir}/$m ] ||
    echo ".so man8/sendmail.8" > %{buildroot}%{_mandir}/$m
done

%check

%pre
getent group  mailnull > /dev/null || %{_sbindir}/groupadd -g 47 -r mailnull > /dev/null 2>&1
getent group  smmsp    > /dev/null || %{_sbindir}/groupadd -g 51 -r smmsp > /dev/null 2>&1

getent passwd mailnull > /dev/null || \
    %{_sbindir}/useradd -u 47 -g mailnull -d %{_localstatedir}/spool/mqueue -r -s /sbin/nologin mailnull > /dev/null 2>&1
getent passwd smmsp    > /dev/null || \
    %{_sbindir}/useradd -u 51 -g smmsp -d %{_localstatedir}/spool/mqueue -r -s /sbin/nologin smmsp > /dev/null 2>&1

[ -h %{_sbindir}/makemap ] || rm -f %{_sbindir}/makemap || :
[ -h %{_mandir}/man8/makemap.8.gz ] || rm -f %{_mandir}/man8/makemap.8.gz || :

exit 0

%preun
%systemd_preun sendmail.service sm-client.service
if [ $1 = 0 ]; then
    %{_sbindir}/alternatives --remove mta %{_sbindir}/sendmail.sendmail
fi
exit 0

%post
%systemd_post sendmail.service sm-client.service

%{_sbindir}/alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.sendmail 90 \
    --slave %{_sbindir}/makemap mta-makemap %{_sbindir}/makemap.sendmail \
    --slave %{_sbindir}/editmap mta-editmap %{_sbindir}/editmap.sendmail \
    --slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.sendmail \
    --slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.sendmail \
    --slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.sendmail \
    --slave /usr/lib/sendmail mta-sendmail /usr/lib/sendmail.sendmail \
    --slave %{_sysconfdir}/pam.d/smtp mta-pam %{_sysconfdir}/pam.d/smtp.sendmail \
    --slave %{_mandir}/man8/sendmail.8.gz mta-sendmailman %{_mandir}/man8/sendmail.sendmail.8.gz \
    --slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man1/mailq.sendmail.1.gz \
    --slave %{_mandir}/man1/newaliases.1.gz mta-newaliasesman %{_mandir}/man1/newaliases.sendmail.1.gz \
    --slave %{_mandir}/man5/aliases.5.gz mta-aliasesman %{_mandir}/man5/aliases.sendmail.5.gz \
    --slave %{_mandir}/man8/rmail.8.gz mta-rmailman %{_mandir}/man8/rmail.sendmail.8.gz \
    --slave %{_mandir}/man8/makemap.8.gz mta-makemapman %{_mandir}/man8/makemap.sendmail.8.gz \
    --slave %{_mandir}/man8/editmap.8.gz mta-editmapman %{_mandir}/man8/editmap.sendmail.8.gz \
    --initscript sendmail > /dev/null 2>&1

{
    chown root \
        %{_sysconfdir}/aliases.db \
        %{_sysconfdir}/mail/access.db \
        %{_sysconfdir}/mail/mailertable.db \
        %{_sysconfdir}/mail/domaintable.db \
        %{_sysconfdir}/mail/virtusertable.db
    SM_FORCE_DBREBUILD=1 %{_sysconfdir}/mail/make
    SM_FORCE_DBREBUILD=1 %{_sysconfdir}/mail/make aliases
} > /dev/null 2>&1

if [ ! -f %{_localstatedir}/spool/clientmqueue/sm-client.st ]; then
    touch %{_localstatedir}/spool/clientmqueue/sm-client.st
    chown smmsp:smmsp %{_localstatedir}/spool/clientmqueue/sm-client.st
    chmod 0660 %{_localstatedir}/spool/clientmqueue/sm-client.st
fi

if [ ! -f %{_sysconfdir}/pki/tls/private/sendmail.key ]; then
    umask 077
    %{_bindir}/openssl genrsa 4096 > %{_sysconfdir}/pki/tls/private/sendmail.key 2> /dev/null
fi

if [ ! -f %{_sysconfdir}/pki/tls/certs/sendmail.pem ]; then
    FQDN=`hostname`
    if [ "x${FQDN}" = "x" ]; then
        FQDN=localhost.localdomain
    fi

    %{_bindir}/openssl req -new -key %{_sysconfdir}/pki/tls/private/sendmail.key -x509 -sha256 \
        -days 365 -set_serial $RANDOM -out %{_sysconfdir}/pki/tls/certs/sendmail.pem \
        -subj "/C=--/ST=SomeState/L=SomeCity/O=SomeOrganization/OU=SomeOrganizationalUnit/CN=${FQDN}/emailAddress=root@${FQDN}"
    chmod 644 %{_sysconfdir}/pki/tls/certs/sendmail.pem
fi

exit 0

%postun
%systemd_postun_with_restart sendmail.service sm-client.service
if [ $1 -ge 1 ] ; then
    mta=`readlink %{_sysconfdir}/alternatives/mta`
    if [ "$mta" == "%{_sbindir}/sendmail.sendmail" ]; then
        %{_sbindir}/alternatives --set mta %{_sbindir}/sendmail.sendmail
    fi
fi
exit 0

%post -n libmilter
/sbin/ldconfig

%postun -n libmilter
/sbin/ldconfig

%files
%doc %{_docdir}/sendmail/{FAQ,KNOWNBUGS,LICENSE,README,RELEASE_NOTES.gz}
%doc %{_datadir}/sendmail-cf/README
%{_bindir}/hoststat
%{_bindir}/makemap
%{_bindir}/purgestat
%{_sbindir}/mailstats
%{_sbindir}/makemap.sendmail
%{_sbindir}/editmap.sendmail
%{_sbindir}/praliases
%{_bindir}/rmail.sendmail
%{_bindir}/newaliases.sendmail
%{_bindir}/mailq.sendmail
%{_sbindir}/smrsh
%attr(2755,root,smmsp) %{_sbindir}/sendmail.sendmail
/usr/lib/sendmail.sendmail

%ghost %attr(0755,-,-) %{_sbindir}/sendmail
%ghost %attr(0755,-,-) %{_sbindir}/makemap
%ghost %attr(0755,-,-) %{_sbindir}/editmap
%ghost %attr(0755,-,-) %{_bindir}/mailq
%ghost %attr(0755,-,-) %{_bindir}/newaliases
%ghost %attr(0755,-,-) %{_bindir}/rmail
%ghost %attr(0755,-,-) /usr/lib/sendmail

%ghost %{_sysconfdir}/pam.d/smtp
%dir %{_localstatedir}/log/mail
%dir %{_sysconfdir}/smrsh
%dir %{_sysconfdir}/mail
%attr(0770,smmsp,smmsp) %dir %{_localstatedir}/spool/clientmqueue
%attr(0700,root,mail) %dir %{_localstatedir}/spool/mqueue

%config(noreplace) %verify(not size mtime md5) %{_localstatedir}/log/mail/statistics
%config(noreplace) %{_sysconfdir}/mail/Makefile
%config(noreplace) %{_sysconfdir}/mail/make
%config(noreplace) %{_sysconfdir}/mail/sendmail.cf
%config(noreplace) %{_sysconfdir}/mail/submit.cf
%config(noreplace) %{_sysconfdir}/mail/helpfile
%config(noreplace) %{_sysconfdir}/mail/sendmail.mc
%config(noreplace) %{_sysconfdir}/mail/submit.mc
%config(noreplace) %{_sysconfdir}/mail/access
%config(noreplace) %{_sysconfdir}/mail/domaintable
%config(noreplace) %{_sysconfdir}/mail/local-host-names
%config(noreplace) %{_sysconfdir}/mail/mailertable
%config(noreplace) %{_sysconfdir}/mail/trusted-users
%config(noreplace) %{_sysconfdir}/mail/virtusertable

%ghost %{_sysconfdir}/mail/aliasesdb-stamp
%ghost %{_sysconfdir}/mail/virtusertable.db
%ghost %{_sysconfdir}/mail/access.db
%ghost %{_sysconfdir}/mail/domaintable.db
%ghost %{_sysconfdir}/mail/mailertable.db

%ghost %{_localstatedir}/spool/clientmqueue/sm-client.st

%{_unitdir}/sendmail.service
%{_unitdir}/sm-client.service
%config(noreplace) %{_sysconfdir}/sysconfig/sendmail
%config(noreplace) %{_sysconfdir}/pam.d/smtp.sendmail
%config(noreplace) %{_sysconfdir}/sasl2/Sendmail.conf
%{_sysconfdir}/NetworkManager/dispatcher.d/10-sendmail

%{_datadir}/sendmail-cf/cf
%{_datadir}/sendmail-cf/domain
%{_datadir}/sendmail-cf/feature
%{_datadir}/sendmail-cf/hack
%{_datadir}/sendmail-cf/m4
%{_datadir}/sendmail-cf/mailer
%{_datadir}/sendmail-cf/ostype
%{_datadir}/sendmail-cf/sendmail.schema
%{_datadir}/sendmail-cf/sh
%{_datadir}/sendmail-cf/siteconfig

%files -n libmilter
%doc LICENSE
%{_docdir}/sendmail/README.libmilter
%{_libdir}/libmilter.so.*

%files -n libmilter-devel
%doc libmilter/docs/*
%{_includedir}/libmilter/*.h
%{_libdir}/libmilter.so

%files help
%{_mandir}/man{8,5,1}
%exclude %{_mandir}/man1/mailq.1.gz
%exclude %{_mandir}/man1/newaliases.1.gz
%exclude %{_mandir}/man5/aliases.5.gz
%exclude %{_mandir}/man8/sendmail.8.gz
%exclude %{_mandir}/man8/rmail.8.gz
%exclude %{_mandir}/man8/makemap.8.gz
%exclude %{_mandir}/man8/editmap.8.gz

%{_docdir}/sendmail/README.cf
%{_docdir}/sendmail/README.sendmail
%{_docdir}/sendmail/README.smrsh
%{_docdir}/sendmail/SECURITY
%{_docdir}/sendmail/op.pdf
%attr(0644,root,root) %{_docdir}/sendmail/contrib/*


%changelog
* Wed Oct 12 2022 yanglu<yanglu72@h-partners.com> - 8.16.1-8
- Type:bugfix
- ID:NA
- SUG:NA
- DESC: fix newaliases command error and postfix service start execption after sendmail install

* Thu Aug 04 2022 yanglu <yanglu72@h-partners.com> - 8.16.1-7
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:Add require procmail, Fix send mail error which no procmail command

* Tue Feb 15 2022 gaihuiying <eaglegai@163.com> - 8.16.1-6
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add ExecStartPost in sendmail.service

* Wed May 12 liulong <liulong20@huawei.com> - 8.16.1-5
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix the sendmail.service startup failure.

* Mon Mar 15 2021 Aichun Li <liaichun@huawei.com> - 8.16.1-4
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:add ExecStartPost in sm-client.service

* Fri Jan 15 2021 gaihuiying <gaihuiying1@huawei.com> - 8.16.1-3
- Type:requirement
- ID:NA
- SUG:NA
- DESC:remove libdb dependency

* Thu Aug 13 2020 gaihuiying <gaihuiying1@huawei.com> - 8.16.1-2
- Type:requirement
- ID:NA
- SUG:NA
- DESC:drop hesiod support

* Mon Aug 10 2020 gaihuiying <gaihuiying1@huawei.com> - 8.16.1-1
- Type:requirement
- ID:NA
- SUG:NA
- DESC:update sendmail to 8.16.1

* Sat Feb 29 2020 openEuler Buildteam <buildteam@openeuler.org> - 8.15.2-33
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:optimization the spec

* Tue Dec 31 2019 openEuler Buildteam <buildteam@openeuler.org> - 8.15.2-32
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:optimization the spec

* Tue Dec 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 8.15.2-31
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:adjust the location of requires

* Sat Sep 21 2019 Huiming Xie <xiehuiming@huawei.com> - 8.15.2-30
- Package init

