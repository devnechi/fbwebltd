@extends('layouts.admin-app-layout')

@section('content')
<div class="container-fluid">
    <div class="row">
        <div class="col-lg-12">
            <div class="card">
                <div class="card-header">
                    <h1 style="color: #a7a4a2;"> {{ __('Add a new project') }} </h1>
                </div>

                <div class="card-body">
                    @if (session('status'))
                    <div class="alert alert-success" role="alert">
                        {{ session('status') }}
                    </div>
                    @endif

                    <div class="container">
                    <ul class="nav navbar-nav justify-content-end" style="display: contents;">
                        <li><a href="#">Register New
                             <strong style="color: #a7a4a2;">
                                {{ __('user') }}
                                </strong>
                                details.
                            </a>
                        </li>
                    </ul>
                    <div class="row">
                        <div class="col-lg-10">
                            <br />
                            {{-- <a class="btn btn-primary" href="#" role="button">Link</a> --}}
                            <br />
                        </div>
                    </div>
                    <br />
                </div>

                    <div class="container">
                        <div class="row">
                            <div class="col-lg-6">
                                <div class="container">
                                    <form>
                                        <div class="form-group">
                                          <label for="exampleFormControlInput1">Email address</label>
                                          <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
                                        </div>
                                        <div class="form-group">
                                          <label for="exampleFormControlSelect1">Example select</label>
                                          <select class="form-control" id="exampleFormControlSelect1">
                                            <option>1</option>
                                            <option>2</option>
                                            <option>3</option>
                                            <option>4</option>
                                            <option>5</option>
                                          </select>
                                        </div>
                                        <div class="form-group">
                                          <label for="exampleFormControlSelect2">Example multiple select</label>
                                          <select multiple class="form-control" id="exampleFormControlSelect2">
                                            <option>1</option>
                                            <option>2</option>
                                            <option>3</option>
                                            <option>4</option>
                                            <option>5</option>
                                          </select>
                                        </div>
                                        <div class="form-group">
                                          <label for="exampleFormControlTextarea1">Example textarea</label>
                                          <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
                                        </div>
                                      </form>
                                </div>

                            </div>
                            {{-- end of div --}}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
