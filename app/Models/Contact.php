<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Notifications\Notifiable;


class Contact extends Model
{
    use Notifiable;
    use HasFactory;

    protected $primaryKey = "cid";
    protected $table = 'contacts';

     /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'fname',
        'lname',
        'phone',
        'email',
        'message',
        'subject'
    ];

}
