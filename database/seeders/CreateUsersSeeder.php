<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;


class CreateUsersSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $user = [
            [
                'username' => 'Admin',
                'email' => 'admin@futurebasics.co.tz',
                'usertype_id' => '1',
                'password' => bcrypt('123456'),
            ],
            [
                'username' => 'User',
                'email' => 'user@futurebasics.co.tz',
                'usertype_id' => '0',
                'password' => bcrypt('123456'),
            ],
        ];

        foreach ($user as $key => $value) {
            User::create($value);
        }
    }
}
