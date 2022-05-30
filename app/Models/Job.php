<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Job extends Model
{
    use HasFactory, Notifiable;

    protected $primaryKey = "job_id";
    protected $table = 'tbl_job_career';

      /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'addedby',
        'category-type',
        'title',
        'company',
        'job-icon',
        'job_desc'
    ];


}
