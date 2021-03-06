<?php
namespace Deployer;

require 'recipe/laravel.php';

// Project name
set('application', 'Future-Basics');

// Project repository
set('repository', 'https://github.com/devnechi/fbwebltd.git');

// [Optional] Allocate tty for git clone. Default value is false.
set('git_tty', true);

// Shared files/dirs between deploys
add('shared_files', []);
add('shared_dirs', []);

// Writable dirs by web server
add('writable_dirs', []);


// Hosts

// host('futurebasics.co.tz')
//     ->set('deploy_path', '~/{{application}}');
host('futurebasics.co.tz')
    ->user('deployer')
    ->identityFile('~/.ssh/deployerkey')
    ->set('deploy_path', '/var/www/futurebasics.co.tz/public_html/fb/');
// Tasks
//    ->set('deploy_path', '/var/www/futurebasics.co.tz/public_html/fb');


task('build', function () {
    run('cd {{release_path}} && build');
});

set('composer_options', 'install --verbose --prefer-dist --no-progress --no-interaction --optimize-autoloader');

// [Optional] if deploy fails automatically unlock.
after('deploy:failed', 'deploy:unlock');

// Migrate database before symlink new release.

// before('deploy:symlink', 'artisan:migrate');

