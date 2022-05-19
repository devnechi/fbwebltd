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

 Route::get('/home', [App\Http\Controllers\HomeController::class, 'index']);
// Route::get('/admin', [App\Http\Controllers\HomeController::class, 'adminHome'])->name('admin');

//email
//to html view
//Route::get('/mailsend',[App\Http\Controllers\MailController::class, 'mailsend']);

//sending the email
//Route::post('/sendmail',[App\Http\Controllers\MailController::class, 'sendmail'])->name('sendmail');

 Route::get('/contact-sem', [App\Http\Controllers\ContactController::class, 'getContact'])->name('contact-sem');
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
// Route::get('/our-services', [App\Http\Controllers\PublicPagesController::class, 'singelservice'])->name('our-services');
Route::get('/contact-us', [App\Http\Controllers\PublicPagesController::class, 'contactus'])->name('contact-us');

Route::get('/coming-soon', [App\Http\Controllers\PublicPagesController::class, 'comingsoon'])->name('coming-soon');

Route::get('/our-services', [App\Http\Controllers\PublicPagesController::class, 'generalServices'])->name('our-services');
Route::get('/all-graphic-designs-services', [App\Http\Controllers\PublicPagesController::class, 'graphicAllservices'])->name('all-graphic-designs-services');
Route::get('/graphic-design-service-details', [App\Http\Controllers\PublicPagesController::class, 'graphicServicesDetails'])->name('graphic-design-service-details');

Route::get('/all-prototyping-services', [App\Http\Controllers\PublicPagesController::class, 'protoAllservices'])->name('all-prototyping-services');
Route::get('/prototyping-service-details', [App\Http\Controllers\PublicPagesController::class, 'protoServicesDetails'])->name('prototyping-service-details');

Route::get('/all-software-development-services', [App\Http\Controllers\PublicPagesController::class, 'softDevAllservices'])->name('all-software-development-services');
Route::get('/software-development-service-details', [App\Http\Controllers\PublicPagesController::class, 'softDevServicesDetails'])->name('software-development-service-details');

Route::get('/all-data-science-services', [App\Http\Controllers\PublicPagesController::class, 'alldataScienceservices'])->name('all-data-science-services');
Route::get('/data-science-service-details', [App\Http\Controllers\PublicPagesController::class, 'dataScienceServicesDetails'])->name('data-science-service-details');


//careers
Route::get('/careers-with-us', [App\Http\Controllers\PublicPagesController::class, 'careersWithUs'])->name('careers-with-us');
Route::get('/career-details', [App\Http\Controllers\PublicPagesController::class, 'jobDetails'])->name('career-details');

//developers pool forms
Route::get('/collection-of-innovators', [App\Http\Controllers\PublicPagesController::class, 'alldevPoolForms'])->name('collection-of-innovators');
Route::get('/developers-info-entery-form', [App\Http\Controllers\PublicPagesController::class, 'devRecruitForm'])->name('developers-info-entery-form');
Route::get('/designers-info-entery-form', [App\Http\Controllers\PublicPagesController::class, 'designersRecruitForm'])->name('designers-info-entery-form');


// Route::get('/about', 'PublicPagesController@about')->name('about');

// Route::get('/business', 'PublicPagesController@business')->name('business');


Route::get('forget-password', [App\Http\Controllers\Auth\ForgotPasswordController::class, 'showForgetPasswordForm'])->name('forget.password.get');
Route::post('forget-password', [App\Http\Controllers\Auth\ResetPasswordController::class, 'submitForgetPasswordForm'])->name('forget.password.post');
Route::get('reset-password/{token}', [App\Http\Controllers\Auth\ForgotPasswordController::class, 'showResetPasswordForm'])->name('reset.password.get');
Route::post('reset-password', [App\Http\Controllers\Auth\ResetPasswordController::class, 'submitResetPasswordForm'])->name('reset.password.post');
Route::get('/changePassword', [App\Http\Controllers\Auth\ResetPasswordController::class, 'showChangePasswordGet'])->name('changePasswordGet');
Route::post('/changePassword', [App\Http\Controllers\Auth\ResetPasswordController::class, 'changePasswordPost'])->name('changePasswordPost');

// Route::get('/about', 'PublicPagesController@about')->name('about');

// Route::get('/business', 'PublicPagesController@business')->name('business');


//member redirection routes
//super admin

//adminstator/admin/nomarl admin
//nuser/normaluser
// Route::get('/main-admin', 'SuperAdminController@index')->name('main-admin')->middleware('main-admin');
// Route::get('/fbc-admin', 'NormalAdminController@index')->name('fbc-admin')->middleware('fbc-admin');
// Route::get('/fbc-user', 'NormalUserController@index')->name('fbc-user')->middleware('fbc-user');
// //previous/old controller below
// Route::get('/admin', 'AdminController@index')->name('admin')->middleware('admin');


// Route::get('/main-admin', 'SuperAdminController@index')->name('main-admin');
Route::get('/main-admin', [App\Http\Controllers\SuperAdminController::class, 'index'])->name('main-admin');
//super admin routes
Route::get('/manage-users', [App\Http\Controllers\SuperAdminController::class, 'navManageUsers'])->name('manage-users');
Route::get('/add-new-user', [App\Http\Controllers\SuperAdminController::class, 'navCreateNewUser'])->name('add-new-user');
Route::post('create-new-user', [App\Http\Controllers\SuperAdminController::class, 'storeNewUser'])->name('create-new-user');



Route::get('/manage-projects', [App\Http\Controllers\SuperAdminController::class, 'navManageProjects'])->name('manage-projects');
Route::get('/add-new-project', [App\Http\Controllers\SuperAdminController::class, 'navCreateNewProject'])->name('add-new-project');
Route::get('/manage-human-resource-activities', [App\Http\Controllers\SuperAdminController::class, 'navManageHRactivities'])->name('manage-human-resource-activities');
Route::get('/manage-financial-activities', [App\Http\Controllers\SuperAdminController::class, 'navManageFMactivities'])->name('manage-financial-activities');
Route::get('/create-new-payment-voucher', [App\Http\Controllers\SuperAdminController::class, 'navCreateNewPV'])->name('create-new-payment-voucher');
Route::get('/manage-careers-opportunities', [App\Http\Controllers\SuperAdminController::class, 'navManageDevPool'])->name('manage-careers-opportunities');
Route::get('/create-new-career-opportunity', [App\Http\Controllers\SuperAdminController::class, 'navCreateTalentPoster'])->name('create-new-career-opportunity');



Route::get('/fbc-admin', [App\Http\Controllers\NormalAdminController::class, 'index'])->name('fbc-admin');
Route::get('/fbc-user', [App\Http\Controllers\NormalUserController::class, 'index'])->name('fbc-user');


Route::get('/fbc-admin', 'NormalAdminController@index')->name('fbc-admin');
Route::get('/fbc-user', 'NormalUserController@index')->name('fbc-user');
