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
        package_ensure(packages,update=False)

    return True

def provision_gems(gems=''):
    with mode_sudo():
        for gem in gems:
            if not gem in run('gem list %s' % (gem,)):
                run('gem install --no-ri --no-rdoc %s' % (gem,))

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
        'trusty_64': {
            'package_provider': 'apt',
            'packages': 'ruby ruby-dev build-essential libreadline-dev libncurses5-dev libpcre3-dev libssl-dev perl',
            'gems': ['fpm'],
            'fpm': {
                'deps': ['libreadline6 >= 6.2-8','libpcre3 >= 8'],
                'target': 'deb',
                'platform': 'trusty',
                'iteration': '2.openresty',
                'files': {
                    'conf/nginx.conf': 'buildoutput/etc/nginx/nginx.conf',
                    'conf/conf.d/default.conf': 'buildoutput/etc/nginx/conf.d/default.conf',
                    'conf/conf.d/virtual.conf': 'buildoutput/etc/nginx/conf.d/virtual.conf',
                    'conf/conf.d/ssl.conf': 'buildoutput/etc/nginx/conf.d/ssl.conf',
                    'conf/logrotate.d/nginx': 'buildoutput/etc/logrotate.d/nginx',
                    'contrib/openresty-initd.debian': 'buildoutput/etc/init.d/nginx',
                    'contrib/openresty-preinstall.debian': 'openresty-preinstall.sh',
                    'contrib/openresty-postinstall.debian': 'openresty-postinstall.sh'
                }
            }
        },
        'trusty_32': {
            'package_provider': 'apt',
            'packages': 'ruby1.9.1 rubygems build-essential libreadline-dev libncurses5-dev libpcre3-dev libssl-dev perl',
            'gems': ['fpm'],
            'fpm': {
                'deps': ['libreadline6 >= 6.2-8','libpcre3 >= 8'],
                'target': 'deb',
                'platform': 'trusty',
                'iteration': '2.openresty',
                'files': {
                    'conf/nginx.conf': 'buildoutput/etc/nginx/nginx.conf',
                    'conf/conf.d/default.conf': 'buildoutput/etc/nginx/conf.d/default.conf',
                    'conf/conf.d/virtual.conf': 'buildoutput/etc/nginx/conf.d/virtual.conf',
                    'conf/conf.d/ssl.conf': 'buildoutput/etc/nginx/conf.d/ssl.conf',
                    'conf/logrotate.d/nginx': 'buildoutput/etc/logrotate.d/nginx',
                    'contrib/openresty-initd.debian': 'buildoutput/etc/init.d/nginx',
                    'contrib/openresty-preinstall.debian': 'openresty-preinstall.sh',
                    'contrib/openresty-postinstall.debian': 'openresty-postinstall.sh'
                }
            }
        },
        'sl65_64': {
            'package_provider': 'yum',
            'packages': 'rpm-build ruby ruby-devel rubygems readline-devel pcre-devel openssl-devel perl make gcc',
            'gems': ['fpm'],
            'fpm': {
                'deps': ['readline >= 5','pcre >= 7.8-6'],
                'target': 'rpm',
                'platform': 'el6',
                'iteration': '1.openresty.el6',
                'files': {
                    'conf/nginx.conf': 'buildoutput/etc/nginx/nginx.conf',
                    'conf/conf.d/default.conf': 'buildoutput/etc/nginx/conf.d/default.conf',
                    'conf/conf.d/virtual.conf': 'buildoutput/etc/nginx/conf.d/virtual.conf',
                    'conf/conf.d/ssl.conf': 'buildoutput/etc/nginx/conf.d/ssl.conf',
                    'conf/logrotate.d/nginx': 'buildoutput/etc/logrotate.d/nginx',
                    'contrib/openresty-initd.rhel': 'buildoutput/etc/init.d/nginx',
                    'contrib/openresty-preinstall.rhel': 'openresty-preinstall.sh',
                    'contrib/openresty-postinstall.rhel': 'openresty-postinstall.sh'
                }
            },
        },
        'ct7_64': {
            'package_provider': 'yum',
            'packages': 'rpm-build ruby ruby-devel rubygems readline-devel pcre-devel openssl-devel perl make gcc',
            'gems': ['fpm'],
            'fpm': {
                'deps': ['readline >= 5','pcre >= 7.8-6'],
                'target': 'rpm',
                'platform': 'el7',
                'iteration': '1.openresty.el7',
                'files': {
                    'conf/nginx.conf': 'buildoutput/etc/nginx/nginx.conf',
                    'conf/conf.d/default.conf': 'buildoutput/etc/nginx/conf.d/default.conf',
                    'conf/conf.d/virtual.conf': 'buildoutput/etc/nginx/conf.d/virtual.conf',
                    'conf/conf.d/ssl.conf': 'buildoutput/etc/nginx/conf.d/ssl.conf',
                    'conf/logrotate.d/nginx': 'buildoutput/etc/logrotate.d/nginx',
                    'contrib/openresty-initd.rhel': 'buildoutput/etc/init.d/nginx',
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
    './configure --with-luajit --prefix=/usr/share '
    '--sbin-path=/usr/sbin/nginx '
    '--conf-path=/etc/nginx/nginx.conf '
    '--error-log-path=/var/log/nginx/error.log '
    '--http-log-path=/var/log/nginx/access.log '
    '--pid-path=/var/run/nginx.pid '
    '--lock-path=/var/run/nginx.lock '
    '--http-client-body-temp-path=/var/cache/nginx/client_temp '
    '--http-proxy-temp-path=/var/cache/nginx/proxy_temp '
    '--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp '
    '--http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp '
    '--http-scgi-temp-path=/var/cache/nginx/scgi_temp '
    '--user=nginx --group=nginx '
    '--with-pcre-jit '
    '--with-http_ssl_module --with-http_realip_module '
    '--with-http_addition_module --with-http_sub_module '
    '--with-http_dav_module --with-http_flv_module '
    '--with-http_mp4_module --with-http_gunzip_module '
    '--with-http_gzip_static_module --with-http_random_index_module '
    '--with-http_secure_link_module --with-http_stub_status_module '
    '--with-http_auth_request_module '
    '--with-mail --with-mail_ssl_module '
    '--with-file-aio --with-ipv6 --with-http_spdy_module '
    '--with-cc-opt="-O2 -g -pipe -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m64 -mtune=generic"'
)

@parallel(pool_size=2)
def build_openresty(version='1.9.7.3',configure_cmd=default_configure_cmd):

    make_cmd = 'make -j4'
    install_cmd = 'make all install DESTDIR=$PWD/buildoutput'

    source_file = 'ngx_openresty-%s.tar.gz' % (version,)
    source_url = 'http://openresty.org/download' #'http://10.131.237.143/openresty'

    ensure_local_dir('build-temp')

    with lcd('./build-temp'):
        if not local_file_exists(source_file):
            local('wget -O %s %s/%s' % (source_file,source_url,source_file))
            local('wget https://github.com/pintsized/lua-resty-http/archive/a730f90.tar.gz -O lua-resty-http.tar.gz')

        #console.confirm('Do you want to continue?', default=True)
        ensure_remote_dir('build-temp')
        put(source_file,'build-temp')
        put('lua-resty-http.tar.gz', 'build-temp')
        with cd('build-temp'):
            run('tar xzf %s' % (source_file,))
            run('tar xzf lua-resty-http.tar.gz')
            with cd('ngx_openresty-%s' % (version,)):
                # add lua-resty-http
                run('mv ../lua-resty-http-* bundle/lua-resty-http-0.06')
                run("sed -i 's/for my $key (qw(/for my $key (qw(http /g' configure")
                run('ls -la bundle/')
                # build
                run('%s && %s && %s' % (configure_cmd,make_cmd,install_cmd))


@parallel
def package_openresty(version='1.9.7.3'):

    fpm_command = (
        "fpm -v '%(version)s' --iteration '%(iteration)s' %(deps)s "
        "--url 'https://github.com/amuraru/ngx-openresty-build' "
        "--description 'OpenResty LUA application server, bundling nginx.' "
        "--vendor 'OSS' --license '2-clause BSD-like license' -m 'amuraru@adobe.com' "
        "--provides 'nginx' "
        "%(scripts)s "
        "--rpm-os 'linux-gnu' -a 'native' "
        "--rpm-user root --rpm-group root --deb-user root --deb-group root "
        "--config-files /etc/nginx/nginx.conf "
        "--directories /var/cache/nginx --directories /etc/nginx --directories /etc/nginx/conf.d --directories /usr/share/nginx  --directories /var/log/nginx "
        "-n nginx -s dir -t %(target)s -- *"
    )

    targetName,s = get_target()

    ext = s['fpm']['target']

    args = {
        'version': version,
        'iteration': s['fpm']['iteration'],
        'deps': ' '.join(["-d '%s'" % (dep,) for dep in s['fpm']['deps']]),
        'scripts': [],
        'target': ext
    }

    ensure_local_dir('build-out')

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
                ensure_remote_dir('var/cache/nginx')
                ensure_remote_dir('etc/nginx/conf.d')
                result = run(fpm_command % args)

        with cd('buildoutput'), lcd('build-out'):
            get('*.%s' % (ext,),'.')
            run('rm -f *.%s' % (ext,))

@parallel
def build_clean():
    local('rm -rf build-temp')
    with cd('~'):
        run('rm -rf build-temp')

@parallel
def shutdown():
    v.halt(vm_name=get_target()[0])

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

