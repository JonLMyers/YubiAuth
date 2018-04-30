function register(){
    var response;
    var username = $('#usr').val();
    var password = $('#pwd').val();
    var otp = $('#otp').val();
    var data = {'username': username, 'password': password, 'yubikey': otp};

    $.ajax({
        type: "POST",
        url: "/registration",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(data) {
            response = data;
            alert(response.message);
        }
    });
}

function login(){
    var response;
    var username = $('#usr').val();
    var password = $('#pwd').val();
    var otp = $('#otp').val();
    var data = {'username': username, 'password': password, 'yubikey': otp};

    $.ajax({
        type: "POST",
        url: "/login",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(data) {
            response = data;
            if(response.access_token){
                sessionStorage['token'] = response.access_token;
                sessionStorage['refresh_token'] = response.refresh_token;
                window.location.href = 'security';
            }
            else{
                alert(response.message)
            }
        }
    });
}

function command(){
    var command = $('#cmd').val();
    data = {'command': command};
    $.ajax({
        type: "POST",
        url: "/command",
        data: JSON.stringify(data),
        dataType : 'application/json',
        beforeSend : function(xhr) {
          // set header if JWT is set
            xhr.setRequestHeader("Authorization", "Bearer " +  sessionStorage.token);
        },
        error : function(data) {
          alert(data.message);
        },
        success: function(data) {
            alert(data.message);
        }
    });
}

function logout(){
    $.ajax({
        url: "/logout",
        dataType : 'application/json',
        beforeSend : function(xhr) {
          // set header if JWT is set
          if ($window.sessionStorage.token) {
              xhr.setRequestHeader("Authorization", "Bearer " +  $window.sessionStorage.token);
          }
    
        },
        error : function(data) {
          alert(data)
        },
        success: function(data) {
            alert("Logged out")
            window.location.href = '/';
        }
    });
}

function register_device(){
    var response;
    var username = $('#usr').val();
    var password = $('#pwd').val();
    var data = {'username': username, 'password': password};

    $.ajax({
        type: "POST",
        url: "/registration",
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function(data) {
            response = data;
            alert(response.message);
        }
    });
}

function get_role(role_title) {
    var response;
    $.ajax({
        type: "GET",
        url: "/api/get_role/" + role_title,
        function(data) {
            response = jQuery.parseJSON(data);
        }
    });

    // TODO: Do something with response
    return response;
}

function verify(option_data) {
    var response;

    $.ajax({
        type: "POST",
        url: "/api/verify",
        data: JSON.stringify(option_data),
        contentType: 'application/json',
        success: function(data) {
            response = data;
            $.each(data.additional_roles, function(i, option) {
                $('#exampleFormControlSelect2').append($('<option/>').attr("value", option).text(option));
             });
        }
    });

    // TODO: Do something with response
    return response;
}

function os_list() {
    $.getJSON("/api/os_list", function(data){
        $.each(data.operating_systems, function(i, option) {
           $('#exampleFormControlSelect1').append($('<option/>').attr("value", option).text(option));
        });
    })
     return;
}

function build() {
    var os_values = $('#exampleFormControlSelect1').val();
    var vuln_values = $('#exampleFormControlSelect2').val();
    var data = {'selected_os': os_values, 'selected_roles': vuln_values}
    
    console.log(data);

    var response;
    $.ajax({
        type: "POST",
        url: "/api/build",
        data:  JSON.stringify(data),
        contentType: 'application/json',
        success: function(data) {
            response = data;
            console.log(data.responseJSON.description);
            alert("Succesfully built!");
        },
        error: function(data) {
            alert("Build did not complete: "+data.responseJSON.description);
        }
    });

    // TODO: Do something with response
    return response;
}

function picked_os(option){
    var data = {'selected_os': option};
    console.log(data)
    verify(data); 
}