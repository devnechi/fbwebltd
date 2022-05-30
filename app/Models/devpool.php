<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class devpool extends Model
{
    use HasFactory, Notifiable;

    protected $primaryKey = "dev_pool_id";
    protected $table = 'tbldev-pool';

      /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'category',
        'title',
        'company',
        'added_by',
        'job-position',
        'type-of-offer',
        'upload-banner-photo',
        'job_desc',
        'min-monthly-salary',
        'max-monthly-salary',
        'job-icon',
        'location',
        'type-of-offer',
        'job-position'

    ];


}
