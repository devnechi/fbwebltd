<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Notifications\Notifiable;

use Auth;

class Gender extends Model
{
    use HasFactory, Notifiable;

    protected $primaryKey = "gender_id";
    protected $table = 'genders_tbl';

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'gender_title'
    ];

}
