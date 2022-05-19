<?php

namespace Database\Seeders;

use App\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Faker\Factory as Faker;

class UserRolesSeeder extends Seeder
{
        /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {

    $faker = Faker::create();
    $role = ['Super Admin', 'Normal Admin', 'Normal User', 'Employee'];
    $desc = ['Nunc vel risus commodo viverra. Pellentesque diam volutpat commodo sed egestas egestas. Adipiscing elit ut aliquam purus. Libero justo laoreet sit amet cursus sit amet. Pellentesque elit ullamcorper dignissim cras tincidunt lobortis feugiat. Nunc pulvinar sapien et ligula ullamcorper malesuada proin.',
     'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Fringilla phasellus faucibus scelerisque eleifend. Est velit egestas dui id ornare arcu odio. Condimentum id venenatis a condimentum. Proin fermentum leo vel orci porta. Dictum fusce ut placerat orci nulla pellentesque.',
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'];

    foreach(range(1, 4) as $index){
        DB::table('roles_tbl')->insert([
            'role_title' => $faker->randomElement($role),
            'role_desc' => Str::random(200),
            'role_status' => 'active'
            ]);

           }
        }
}
