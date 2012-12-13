#!build-env/bin/python

import os, os.path, re, vagrant, pprint
from contextlib import contextmanager
from fabric.api import parallel, env, execute, task, sudo, put, get, local, settings, run
from fabric.context_managers import cd, lcd, hide, show
from fabric.contrib import console
from cuisine import *

v = vagrant.Vagrant()

def provision(settings):
    if not provision_packages(settings['packages'],settings['package_provider']):
        print "Unable to provision!"
        return False
    if not provision_gems(settings['gems']):
        print "Unable to provision gems!"
        return False 
    return True

def provision_packages(packages='',provider=None):
    if provider is None:
        return False

    with mode_sudo():
        select_package(provider)
        package_ensure(packages,update=True)

    return True

def provision_gems(gems=''):
    with mode_sudo():
        for gem in gems:
            if not gem in run('gem list %s' % (gem,)):
                run('gem install %s' % (gem,))

    return True

def get_target():
    targetName = env.hosts_to_targets[env.host_string]
    s = env.targets[targetName] if targetName in env.targets else {}
    return targetName,s

def set_target(s):
    targetName = env.hosts_to_targets[env.host_string]
    env.targets[targetName] = s

def bootstrap(*targets):
    env.hosts = []
    env.targets = {}
    env.hosts_to_targets = {}
    env.disable_known_hosts = True

    for target in targets:
        print "Bringing up %s..." % (target,)
        v.up(no_provision=True,vm_name=target)
        host = v.user_hostname_port(vm_name=target)
        env.hosts.append(host)
        env.hosts_to_targets[host] = target
        env.targets[target] = {}
        print "%s is up..." % (target,) 
        env.key_filename = v.keyfile(vm_name=target)
    return True
    
def config_openresty():
    avail_targets = {
        'precise_64': {
            'package_provider': 'apt',
            'packages': 'ruby1.9.1 rubygems build-essential libreadline-dev libncurses5-dev libpcre3-dev libssl-dev perl',
            'gems': ['fpm'],
            'fpm': {
                'deps': ['libreadline6 >= 6.2-8','libpcre3 >= 8'],
                'target': 'deb',
                'platform': 'precise',
                'files': {
                    'contrib/openresty-initd.debian': 'buildoutput/etc/init.d/openresty',
                    'contrib/openresty-preinstall.debian': 'openresty-preinstall.sh',
                    'contrib/openresty-postinstall.debian': 'openresty-postinstall.sh'
                }
            }
        },
        'precise_32': {
            'package_provider': 'apt',
            'packages': 'ruby1.9.1 rubygems build-essential libreadline-dev libncurses5-dev libpcre3-dev libssl-dev perl',
            'gems': ['fpm'],
            'fpm': {
                'deps': ['libreadline6 >= 6.2-8','libpcre3 >= 8'],
                'target': 'deb',
                'platform': 'precise',
                'files': {
                    'contrib/openresty-initd.debian': 'buildoutput/etc/init.d/openresty',
                    'contrib/openresty-preinstall.debian': 'openresty-preinstall.sh',
                    'contrib/openresty-postinstall.debian': 'openresty-postinstall.sh'
                }
            }
        },
        'sl63_64': {
            'package_provider': 'yum',
            'packages': 'rpm-build ruby ruby-devel rubygems readline-devel pcre-devel openssl-devel perl make gcc',
            'gems': ['fpm'],
            'fpm': {
                'deps': ['readline >= 5','pcre >= 6.6-6'],
                'target': 'rpm',
                'platform': 'sl6',
                'files': {
                    'contrib/openresty-initd.rhel': 'buildoutput/etc/init.d/openresty',
                    'contrib/openresty-preinstall.rhel': 'openresty-preinstall.sh',
                    'contrib/openresty-postinstall.rhel': 'openresty-postinstall.sh'
                }
            },
        }
    }

    targetName,s = get_target()
    env.targets[targetName] = avail_targets[targetName]

@parallel
def prereqs_openresty():
    provision(get_target()[1])


default_configure_cmd = (
    './configure --with-luajit --prefix=/etc/openresty/ '
    '--sbin-path=/usr/sbin/openresty '
    '--conf-path=/etc/openresty/openresty.conf '
    '--error-log-path=/var/log/openresty/error.log '
    '--http-log-path=/var/log/openresty/access.log '
    '--pid-path=/var/run/openresty.pid '
    '--lock-path=/var/run/openresty.lock '
    '--http-client-body-temp-path=/var/cache/openresty/client_temp '
    '--http-proxy-temp-path=/var/cache/openresty/proxy_temp '
    '--http-fastcgi-temp-path=/var/cache/openresty/fastcgi_temp '
    '--http-uwsgi-temp-path=/var/cache/openresty/uwsgi_temp '
    '--http-scgi-temp-path=/var/cache/openresty/scgi_temp '
    '--user=openresty --group=openresty'
)

@parallel(pool_size=2)
def build_openresty(version='1.2.4.11',configure_cmd=default_configure_cmd):

    make_cmd = 'make'
    install_cmd = 'make all install DESTDIR=$PWD/buildoutput'

    source_file = 'ngx_openresty-%s.tar.gz' % (version,)
    source_url = 'http://agentzh.org/misc/nginx'

    ensure_local_dir('build-temp')

    with lcd('./build-temp'):
        if not local_file_exists(source_file):
            local('wget -O %s %s/%s' % (source_file,source_url,source_file))

        #console.confirm('Do you want to continue?', default=True)
        ensure_remote_dir('build-temp')
        put(source_file,'build-temp')
        with cd('build-temp'):
            run('pwd')
            run('tar xzf %s' % (source_file,))
            with cd('ngx_openresty-%s' % (version,)):
                run('%s && %s && %s' % (configure_cmd,make_cmd,install_cmd))


@parallel
def package_openresty(version='1.2.4.11',iteration='1'):

    fpm_command = (
        "fpm -v '%(version)s' --iteration '%(iteration)s' %(deps)s "
        "--url 'https://github.com/organizations/squizuk' "
        "--description 'OpenResty LUA application server, bundling nginx.' "
        "--vendor 'SquizUK' -m 'Ben Agricola <bagricola@squiz.co.uk>' "
        "%(scripts)s "
        "--rpm-os 'linux-gnu' -a 'native' "
        "--rpm-user openresty --rpm-group openresty "
        "--deb-user openresty --deb-group openresty "
        "-n openresty --config-files '/etc/openresty/openresty.conf' -s dir -t %(target)s -- *"
    )

    targetName,s = get_target()

    ext = s['fpm']['target']

    args = {
        'version': version,
        'iteration': iteration,
        'deps': ' '.join(["-d '%s'" % (dep,) for dep in s['fpm']['deps']]),
        'scripts': [],
        'target': ext
    }

    ensure_local_dir('build-out')
    user_ensure('openresty')
    group_ensure('openresty')
    
    with cd('build-temp/ngx_openresty-%s' % (version,)):

        with settings(warn_only=True):
            # Upload all required files to needed directory
            for localpath, remotepath in s['fpm']['files'].items():
                destDir = os.path.dirname(remotepath)
                if destDir:
                    ensure_remote_dir(destDir)

                put('./' + localpath,remotepath,mirror_local_mode=True)

            if remote_file_exists('./openresty-preinstall.sh'):
                args['scripts'].append('--before-install ../openresty-preinstall.sh') 
            if remote_file_exists('./openresty-postinstall.sh'):
                args['scripts'].append('--after-install ../openresty-postinstall.sh') 

            args['scripts'] = ' '.join(args['scripts'])

            with cd('buildoutput'):
                result = run(fpm_command % args)

        with cd('buildoutput'), lcd('build-out'):
            get('*.%s' % (ext,),'.')
            run('rm -f *.%s' % (ext,))

@parallel
def build_clean():
    local('rm -rf build-temp')
    with cd('~'):
        run('rm -rf build-temp')

def local_file_exists(file):
    with settings(warn_only=True, hide=True):
        return local('test -f "%s"' % (file,),capture=True).succeeded

def remote_file_exists(file):
    with settings(warn_only=True, hide=True):
        return run('test -f "%s"' % (file,)).succeeded

def ensure_local_dir(dir):
    with settings(warn_only=True, hide=True):
        if local('test -d "%s"' % (dir,),capture=True).failed:
            local('mkdir -p %s' % (dir,))

def ensure_remote_dir(dir):
    with settings(warn_only=True, hide=True):

        if run('test -d "%s"' % (dir,)).failed:
            run('mkdir -p %s' % (dir,))
