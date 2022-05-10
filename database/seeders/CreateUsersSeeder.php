<?php

namespace Database\Seeders;

use App\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Faker\Factory as Faker;


class CreateUsersSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {

        $faker = Faker::create();
        $gender = [1, 2];
        $wrktype = ['full-time', 'part-time', 'consulting'];
        $sts_id = ['active', 'suspended', 'deleted'];
        $usraccstatus = ['pending verification', 'verified', 'suspended'];
        $userroles = [1, 2, 3, 4];



        foreach(range(1, 10) as $index){
          DB::table('users')->insert([
            'email'    => $faker->firstName.'@fbc.co.tz',
            'fname'     => $faker->firstName,
            'mname' => $faker->userName,
            'lname' => $faker->lastName,
            'phonenumber'    => $faker->phoneNumber,
            'dob'          => now(),
            'role_id' => $faker->randomElement($userroles),
            'gender_id'               => $faker->randomElement($gender),
            'job_title'       => 'Developer',
            'job_desc'       => Str::random(200),
            'acc_status'       => 1,
            'user_photo_id'       => Str::random(10),
            'user_contract_id'  => Str::random(10),
            'type_of_employee' => 'full-time',
            'created_by'       => 1,
            'last_active'       => now(),
            'email_verified_at' => now(),
            'password' => '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', // password
            'remember_token' => Str::random(10),
            'created_at' => now(),
            'updated_at' => now()
          ]);

          }
   }
}
