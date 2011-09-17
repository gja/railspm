Name: simple-app
Version: 20110918014901
Summary: The %{name} rails application
Release: 1%{?dist}
License: MIT
Group: Development/Tools
URL: https://github.com/gja
Source0: http://nowhere.com/%{name}-%{version}.tar.gz
Requires: holidays-code-%{version} = %{version}-%{release}
Requires: httpd

%description
%{name} application

%package code-%{version}
Summary: The Actual Code
Group: Development/Tools

%description code-%{version}
The code directory. Feel free to deploy multiple of these

%define deploydir %{_localstatedir}/www/rails/%{name}
%define current_dir %{deploydir}/current
%define release_dir %{deploydir}/releases/%{version}
%define logdir %{_localstatedir}/log/%{name}
%define latest_migration 20110913031254_create_foos.rb


%prep
%setup -q

%build
# How does this get handled cleanly? Without rvm/rbenv, etc?
export RBENV_VERSION=1.9.2-p290

export RAILS_ENV=production
bundle --without development test

# FIXME: for some reason, rails 3.1.0 need db for assets migrate. Hack
bundle exec rake assets:precompile

bundle --binstubs --deployment --without development test assets

find config -name *.example | while read i; do
  ln -s %{deploydir}/shared/`dirname $i`/`basename $i .example` `dirname $i`/`basename $i .example`
done

rm -rf tmp log
ln -s ../shared/tmp tmp
ln -s %{logdir} log

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
mv config/app.conf %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

mkdir -p %{buildroot}%{logdir}
mkdir -p %{buildroot}%{release_dir}
mkdir -p %{buildroot}%{deploydir}/shared/tmp
mkdir -p %{buildroot}%{deploydir}/shared/config
ln -s %{logdir} %{buildroot}%{deploydir}/shared/log

mv .bundle * %{buildroot}%{release_dir}

ln -s %{release_dir} %{buildroot}%{current_dir}

%pre
export RAILS_ENV=production
echo "Migrating Database"
if [ -L %{current_dir} ]; then
  cd %{current_dir}
  if [ -f db/migrate/%{latest_migration} ]; then
    ./bin/rake db:migrate VERSION=%{latest_migration}
  fi
fi
cd %{release_dir}
./bin/rake db:migrate

%post
echo "Restarting Passenger"
cd %{current_dir}
touch tmp/restart.txt

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{deploydir}/current
%{_sysconfdir}/httpd/conf.d/%{name}.conf

%files code-%{version}
%defattr(-,root,root,-)
%{deploydir}/shared
%{deploydir}/releases
%{logdir}
