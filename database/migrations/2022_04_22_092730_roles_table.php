<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class RolesTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {

        Schema::create('roles_tbl', function (Blueprint $table) {
            $table->increments('role_id');
            $table->string('role_title');
            $table->string('role_desc');
            $table->timestamp('date_created');
            $table->timestamp('date_updated');
            $table->string('role_status');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        //
        Schema::dropIfExists('roles_tbl');

    }
}
