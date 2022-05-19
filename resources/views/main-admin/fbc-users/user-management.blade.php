{{-- @extends('layouts.app') --}}
@extends('layouts.admin-app-layout')
@section('content')
<div class="container-fluid">
  <!--contact us form start-->
  <section class="contact-us-form pt-60 pb-120" style="background: url('img/shape/contact-us-bg.svg')no-repeat center bottom">
    <div class="container">

        <div class="row justify-content-lg-between align-items-center">
            <div class="col-lg-12 col-md-8">
                <div class="section-heading">
                    <h2>All Users of the Platform</h2>
                    <p>We are always available anytime for coffee, a quick chat, phone call or a meeting. just reach out to us and We will contact you.</p>
                </div>

                <div class="col-lg-12 col-md-8">
                <a href="{{ route('add-new-user') }}" class="btn btn-primary">Add New User</a>
                </div>
                <br />
                {{-- <div class="clearfix"></div> --}}

                  <table class="table">
                    <thead class="thead-light">
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">User</th>
                        <th scope="col">Name</th>
                        <th scope="col">Email</th>
                        <th scope="col">Role id</th>
                        <th scope="col">Job Title</th>
                        <th scope="col">account status</th>
                        <th scope="col">Last Active</th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                    </tr>
                    </thead>
                    <tbody>
                        @foreach($fbcusers as $fbcuser)
                      <tr>
                        <th scope="row">{{ $fbcuser->user_id }}</th>
                        <td><img src="/{{$fbcuser->user_photo_id }}" style="height: 50px; width: 50px; border-radius: 50%;"> </td>
                        <td class="text-center">{{ $fbcuser->fname }}</td>
                        <td>{{ $fbcuser->email }}</td>
                        <td>{{ $fbcuser->role_id }}</td>
                        <td>{{ $fbcuser->job_title }}</td>
                        <td>{{ $fbcuser->acc_status }}</td>
                        <td>{{ $fbcuser->last_active }}</td>
                        <td>
                            <ul class="list-group list-group-horizontal">
                                <li class="list-group-item">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-arrow-up-square-fill" viewBox="0 0 16 16">
                                        <path d="M2 16a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2zm6.5-4.5V5.707l2.146 2.147a.5.5 0 0 0 .708-.708l-3-3a.5.5 0 0 0-.708 0l-3 3a.5.5 0 1 0 .708.708L7.5 5.707V11.5a.5.5 0 0 0 1 0z"/>
                                      </svg>
                                </li>
                                <li class="list-group-item">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-eye" viewBox="0 0 16 16">
                                        <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                                        <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                                      </svg>
                                </li>
                                <li class="list-group-item">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                                      </svg>
                                </li>
                              </ul>
                            </td>
                      </tr>
                      @endforeach
                    </tbody>
                  </table>
            </div>

        </div>
    </div>
</section>
<!--contact us form end-->
@endsection
