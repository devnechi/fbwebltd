<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Notifications\Notifiable;

use Auth;

class Role extends Model
{
    use HasFactory, Notifiable;
    protected $primaryKey = "role_id";
    protected $table = 'roles_tbl';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'role_title',
        'role_desc'
    ];

}
