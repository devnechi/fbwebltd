<?php

use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Auth;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Auth::routes();

 Route::get('/home', [App\Http\Controllers\HomeController::class, 'index'])->name('home');
// Route::get('/admin', [App\Http\Controllers\HomeController::class, 'adminHome'])->name('admin');

//email
//to html view
//Route::get('/mailsend',[App\Http\Controllers\MailController::class, 'mailsend']);

//sending the email
//Route::post('/sendmail',[App\Http\Controllers\MailController::class, 'sendmail'])->name('sendmail');

 Route::get('/contact-em', [App\Http\Controllers\ContactController::class, 'getContact'])->name('contact-em');
 Route::post('/contact-em', [App\Http\Controllers\ContactController::class, 'saveContact'])->name('contact-em');




//ADMIN
Route::get('/admin', [App\Http\Controllers\AdminController::class, 'index'])->name('admin');
Route::get('/manage-projects', [App\Http\Controllers\AdminController::class, 'manageprojects'])->name('manage-projects');
Route::get('/add-new-project', [App\Http\Controllers\AdminController::class, 'addnewproject'])->name('add-new-project');
Route::get('/register-new-user', [App\Http\Controllers\AdminController::class, 'toregisternewuser'])->name('register-new-user');
Route::get('/user-management', [App\Http\Controllers\AdminController::class, 'tousermanagement'])->name('user-management');



//public pages
Route::get('/about', [App\Http\Controllers\PublicPagesController::class, 'about'])->name('about');
Route::get('/business', [App\Http\Controllers\PublicPagesController::class, 'business'])->name('business');
Route::get('/our-services', [App\Http\Controllers\PublicPagesController::class, 'singelservice'])->name('our-services');
Route::get('/contact-us', [App\Http\Controllers\PublicPagesController::class, 'contactus'])->name('contact-us');
Route::get('/coming-soon', [App\Http\Controllers\PublicPagesController::class, 'comingsoon'])->name('coming-soon');
Route::get('/our-services', [App\Http\Controllers\PublicPagesController::class, 'generalServices'])->name('our-services');

//generalServices



// Route::get('/about', 'PublicPagesController@about')->name('about');

// Route::get('/business', 'PublicPagesController@business')->name('business');


