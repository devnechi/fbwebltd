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
                    <h2>Manage Dev Pool Career</h2>
                    <p>We are always available anytime for coffee, a quick chat, phone call or a meeting. just reach out to us and We will contact you.</p>
                </div>

                <div class="col-lg-12 col-md-8">
                <a href="{{ route('create-new-dev-pool-opportunity') }}" class="btn btn-primary">Add </a>
                </div>
                <br />
                {{-- <div class="clearfix"></div> --}}
                <table class="table">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Image</th>
                        <th scope="col">Title</th>
                        <th scope="col">Category</th>
                        <th scope="col">Short Description</th>
                        <th scope="col">Date created</th>
                        <th scope="col">Date updated</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th scope="row">1</th>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>@mdo</td>
                      </tr>
                      <tr>
                        <th scope="row">2</th>
                        <td>Jacob</td>
                        <td>Thornton</td>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>@fat</td>
                      </tr>
                      <tr>
                        <th scope="row">3</th>
                        <td colspan="2">Larry the Bird</td>
                        <td>Mark</td>
                        <td>Otto</td>
                        <td>@twitter</td>
                      </tr>
                    </tbody>
                  </table>
            </div>

        </div>
    </div>
</section>
<!--contact us form end-->
@endsection
