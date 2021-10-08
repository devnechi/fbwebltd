@extends('layouts.admin-app-layout')

@section('content')
<div class="container-fluid">
    <div class="row">
        <div class="col-lg-12">
            <div class="card">
                <div class="card-header">
                    <h1 style="color: #a7a4a2;"> {{ __('Company projects') }} </h1>
                </div>

                <div class="card-body">
                    @if (session('status'))
                    <div class="alert alert-success" role="alert">
                        {{ session('status') }}
                    </div>
                    @endif

                    <div class="container">
                    <ul class="nav navbar-nav justify-content-end" style="display: contents;">
                        <li><a href="#">Listed are
                             <strong style="color: #a7a4a2;">
                                {{ __('Projects') }}
                                </strong>
                                 undertaken by Future Basics.
                            </a>
                        </li>
                    </ul>
                    <div class="row">
                        <div class="col-lg-10">
                            <br />
                            <a class="btn btn-primary" href="{{ route('add-new-project') }}" role="button">create a new project</a>
                            <br />
                        </div>
                    </div>
                    <br />
                </div>

                    <div class="container">
                        <div class="row">
                            <div class="col-lg-10">
                                <div class="container">
                                    <table class="table table-hover">
                                        <thead>
                                            <tr>
                                                <th scope="col">#</th>
                                                <th scope="col">Project Name</th>
                                                <th scope="col">Project Desc</th>
                                                <th scope="col">Domain</th>
                                                <th scope="col"></th>
                                                <th scope="col"></th>

                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <th scope="row">1</th>
                                                <td>Wakala +</td>
                                                <td>Otto</td>
                                                <td>wakala-plus.com</td>
                                                <td>
                                                 <button type="button" class="btn btn-success">project details</button>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">2</th>
                                                <td>Smart risiti</td>
                                                <td>Thornton</td>
                                                <td>smartrisiti.com</td>
                                                <td>
                                                    <button type="button" class="btn btn-success">project details</button>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">3</th>
                                                <td colspan="2">Livestoka</td>
                                                <td>livestoka.com</td>
                                                <td>
                                                    <button type="button" class="btn btn-success">project details</button>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">3</th>
                                                <td colspan="2">Radarmile</td>
                                                <td>radarmile.com</td>
                                                <td>
                                                    <button type="button" class="btn btn-success">project details</button>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">3</th>
                                                <td colspan="2">Inspektor</td>
                                                <td>inspektor.com</td>
                                                <td>
                                                    <button type="button" class="btn btn-success">project details</button>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">3</th>
                                                <td colspan="2">Nakwalify</td>
                                                <td>nakwalify.com</td>
                                                <td>
                                                    <button type="button" class="btn btn-success">project details</button>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">3</th>
                                                <td colspan="2">Domoni</td>
                                                <td>domoni.com</td>
                                                <td>
                                                    <button type="button" class="btn btn-success">project details</button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    {{-- end of table --}}
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
