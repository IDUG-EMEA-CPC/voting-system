

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

function isNumber(value) {
    if (value == "") {
        return true
    } else {
        return !isNaN(value);
    }
}

function check_data(reset=false){
    var result = true;

    //    checking mandatory value
    var filled = $('#sessioncode').val() != ""
    if (!filled) {
        $('#sessioncode').addClass('error')
        alertify.error('Session Code must be filled')
    } else {
        $('#sessioncode').removeClass('error')
    }
    result = result && filled

    //    checking rates between 1 and 5 if filled
    single_values = {
        'overall' : 'Overall Session Rating',
        'speaker': 'Speaker Rating',
        'material' : 'Presentation Material Rating',
        'expectation':'Expectation Rating'
    }

    for (id in single_values) {
        key = single_values[id]
        value = $('#' + id).val()
        if (!isNumber(value)) {
            $('#' + id).addClass('error')
            alertify.error(key + ' must be numeric')
            filled = false
        } else {
            if (value != "") {
                if (value < 1 || value > 5) {
                    $('#' + id).addClass('error')
                    alertify.error(key + ' must be between 1 and 5')
                    filled = false
                } else {
                    $('#' + id).removeClass('error')
                    filled = true
                }
            }
        }
        result = result && filled
    }


    //    checking that something is filled
    if ($('#overall').val() == "" &&
        $('#speaker').val() == "" &&
        $('#material').val() == "" &&
        $('#expectation').val() == "") {
        alertify.error('Everything is empty')
        filled = false
        result = result && filled
    }

    return result;

}



function save_value() {
    var data_complete = check_data()
    if (data_complete) {
        save_data()
    }
}


function save_data() {
    console.log('overall', $('#overall').val());
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "add_values",
        type : "POST",
        data : get_data(),
        success : function(data) {
            console.log("success");
            alertify.success('New vote inserted.')
            refresh_value_table();

            reset();

            return true;
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator'
            }

            alertify.error(error);
            //refresh_value_table();
            return false;

        }
    });}


function get_data() {

    return {
            sessioncode : $('#sessioncode').val(),
            overall : $('#overall').val(),
            speaker : $('#speaker').val(),
            material : $('#material').val(),
            expectation : $('#expectation').val(),
            comments : $('#comments').val(),

            url : window.location.href

        }
}

function reset(){
   console.log('resetting');

   $('#overall').val('');
   $('#speaker').val('');
   $('#material').val('');
   $('#expectation').val('');
   $('#comments').val('');

   $('#overall').focus();

}

function check_session(){
    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "check_sessioncode",
        type : "POST",
        data : {
                sessioncode : $('#sessioncode').val(),
        },

       success : function(data) {
            if (data.exists) {
                $('#session-title-display').text(data.title);

                $('#speakers').text(data.speaker);

                $('#attendees').val(data.attendees);
                $('#attendees20').val(data.attendees20);
                updateSessionInfo(data.title);
                enableRatingInputs();
                $('#overall').focus();
                refresh_value_table();
            } else {
                $('#session-title-display').text('');

                $('#speakers').text('');

                $('#attendees').val('');
                $('#attendees20').val('');
                updateSessionInfo("");
                disableRatingInputs();
                refresh_value_table();
            }

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            $('#session-title').text('Error checking session');
            disableRatingInputs();

            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                if(err == "Forbidden") {
                    error = 'You do not have the rights to execute this operation. Please contact the administrator.'
                }
                else {
                    error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator.'
                }

            }

            alertify.error(error);
            return false;
        }
    });

}


function updateAttendeeCounts() {
    const sessionCode = $('#sessioncode').val();
    const attendees = $('#attendees').val();
    const attendees20 = $('#attendees20').val();

    if (sessionCode === '') {
        alertify.error("Session code is required.");
        return;
    }

    $.ajax({
        beforeSend: function (request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url: 'update_attendees',
        type: 'POST',
        data: {
            sessioncode: sessionCode,
            attendees: attendees,
            attendees20: attendees20
        },

        success: function (data) {
            alertify.success('Attendee counts updated');
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            $('#session-title').text('Error checking session');
            disableRatingInputs();

            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                if(err == "Forbidden") {
                    error = 'You do not have the rights to execute this operation. Please contact the administrator.'
                }
                else {
                    error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator.'
                }

            }

            alertify.error(error);
            return false;
        }
    });



}




function refresh_value_table() {
    console.log('refresh')

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "refresh_values",
        type : "POST",
        data : get_data(),

        success : function(data) {
            console.log("success");
            $("#results").html(data);
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                if(err == "Forbidden") {
                    error = 'You do not have the rights to execute this operation. Please contact the administrator.'
                }
                else {
                    error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator.'
                }

            }

            alertify.error(error);
            return false;
        }
    });
}




function value_edit(sessioneval_id) {

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "get_modal_edit_value",
        type : "POST",
        data : {
            sessioneval_id : sessioneval_id

        },

        success : function(data) {
            console.log("success");
            $("#modal-view").html(data);
            $("#modal-view").show();

            var modal = document.getElementById("modal-view");

            window.onclick = function(event) {
                if (event.target == modal) {
                    close_modal()
                }
            }

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alertify.error(errmsg)
        }
    });

}


function save_edit_value(sessioneval_id) {

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "update_modal_edit_value",
        type : "POST",
        data : {
            sessioneval_id : sessioneval_id,
            overall : $('#modal-content #overall').val(),
            speaker : $('#modal-content #speaker').val(),
            material : $('#modal-content #material').val(),
            expectation : $('#modal-content #expectation').val(),
            comments : $('#modal-content #comments').val()

        },

        success : function(data) {
            console.log("success");
            alertify.success('Vote Updated')
            close_modal()
            refresh_value_table()
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator'
            }

            alertify.error(error);

        }
    });

}


function value_delete(sessioneval_id) {

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "get_modal_delete_value",
        type : "POST",
        data : {
            sessioneval_id : sessioneval_id

        },

        success : function(data) {
            console.log("success");
            $("#modal-view").html(data);
            $("#modal-view").show();

            var modal = document.getElementById("modal-view");

            window.onclick = function(event) {
                if (event.target == modal) {
                    close_modal()
                }
            }

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alertify.error(errmsg)
        }
    });

}


function delete_edit_value(sessioneval_id) {

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "delete_modal_edit_value",
        type : "POST",
        data : {
            sessioneval_id : sessioneval_id,
            overall : $('#modal-content #overall').val(),
            speaker : $('#modal-content #speaker').val(),
            material : $('#modal-content #material').val(),
            expectation : $('#modal-content #expectation').val(),
            comments : $('#modal-content #comments').val()

        },

        success : function(data) {
            console.log("success");
            alertify.success('Vote Deleted')
            close_modal()
            refresh_value_table()
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator'
            }

            alertify.error(error);

        }
    });

}


function refresh_session_table() {
    console.log('refresh')

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "refresh_sessions",
        type : "POST",
        data : {
                url : window.location.href
        },

        success : function(data) {
            console.log("success");
            $("#results_sessions").html(data);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                if(err == "Forbidden") {
                    error = 'You do not have the rights to execute this operation. Please contact the administrator.'
                }
                else {
                    error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator.'
                }

            }

            alertify.error(error);
            return false;
        }
    });
};


function refresh_moderator() {
    console.log('refresh')

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "refresh_moderator",
        type : "POST",
        data : {
            sessioncode : $('#sessioncode').val()
        },

        success : function(data) {
            console.log("success");
            $('#moderator').val(data['moderator']);
            $("#speaker").val(data['speaker']);
            $("#attendees").val(data['startcount']);
            $("#attendees20").val(data['midcount']);

            $("#attendees").focus();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                if(err == "Forbidden") {
                    error = 'You do not have the rights to execute this operation. Please contact the administrator.'
                }
                else {
                    error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator.'
                }

            }

            alertify.error(error);
            return false;
        }
    });
};



function session(session_code) {

    console.log(session_code)

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "session",
        type : "GET",
        data : {
            sessioncode : session_code
        },

        success : function(data) {
            console.log("success");
            $("#results").html(data);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {

            data = xhr.responseJSON
            if (data !== undefined) {
                console.log(data)
                if ('message' in data) {
                    error = data['message']
                } else {
                    error = errmsg
                }
            } else {
                if(err == "Forbidden") {
                    error = 'You do not have the rights to execute this operation. Please contact the administrator.'
                }
                else {
                    error = 'An unexpected error occured. Please retry. If the issue still occurs, contact your administrator.'
                }

            }

            alertify.error(error);
            return false;
        }
    });

};





function import_xls_modal() {
    console.log('import xls')

    showLoader();

    $.ajax({
        beforeSend: function(request) {
            request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        url : "import_xls_modal",
        type : "POST",
        data : {
            code : "",
            type : "",
            tag_qualification_name: ""
        },

        success : function(data) {
            console.log("success");
            console.log(data);
            $("#modal-view").html(data);
            $("#modal-view").show();

            var modal = document.getElementById("modal-view");

            window.onclick = function(event) {
                if (event.target == modal) {
                    close_modal()
                }
            }

            hideLoader();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            hideLoader();
            alertify.error(errmsg)
        }
    });

}






