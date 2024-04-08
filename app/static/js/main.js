$("#authUser").click(function() {
  url = window.location.origin + '/api/v1/login'

  $.post(url,
  {
    username: $('#username').val(),
    password: $('#password').val()
  },
  function(data, status) {
    window.location.replace(window.location.origin)

  }).fail(function(){
    alert("Wrong username or password")
  });
});

$("#logout").click(function() {
  url = window.location.origin + '/api/v1/logout'

  $.post(url, { foo : null },
  function(data, status) {
    window.location.replace(window.location.origin)
  }).fail(function(){
    alert("Invalid token")
  });
});

$("#search-patient").click(function() {
  var url = window.location.origin + '/get-patient'
  var doc_id = $('#search-with-id').val()

  if (!doc_id) {
    alert("Trường tìm kiếm không được để trống")
    return false;
  }
  $.get(url, { document_id :  doc_id},
  function(data, status) {
    console.log(data.mother_name)
    $('#not-found-search-result').hide();
    $('#child-name').text(data.name)
    $('#mother-name').text(data.mother_name)
    $('#mother-phone').text(data.phone)

    doc_url = window.location.origin + '/patient-doc/?document_name=' + data.document_path
    $('#document-name-url').attr("href", doc_url);

    $("#search-result").css("visibility", "visible");

  }).fail(function(){
    $("#search-result").css("visibility", "hidden");
    $('#not-found-search-result').show();
  });
});

$("#menu-patient-data-page").click(function() {
  $('#menu-search-page').removeClass('active');
  $('#menu-patient-data-page').addClass('active');
})

// $('input[type="file"]').on('change', function() {
//   Object.values(this.files).forEach(function(file) {
//     console.log(`Type: ${file.type}`);
//     if (file.type == 'application/pdf') {
//       console.log('Huzzah!')
//     }
//   })
// })

// var form = $("#add-patient-doc");
// e.preventDefault();
// var formData = new FormData(form[0]);
// url = window.location.origin + '/create-patient'

$("form#create-new-patient").submit(function(e) {
  e.preventDefault();    
  var formData = new FormData(this);
  url = window.location.origin + '/create-patient'
  $.ajax({
      url: url,
      type: 'POST',
      data: formData,
      success: function (data) {
          alert("Thêm thông tin bệnh nhân thành công")
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) { 
        alert("Error: " + errorThrown); 
      },
      cache: false,
      contentType: false,
      processData: false
  });
});

function getPatients(name = null, seen = null, offset = 0) {
  url = window.location.origin + '/get-patients?'
  if (name !== null) {  
    url = url + 'name=' + name
  }
  if (seen !== null) {  
    url = url + '&seen=' + seen
  }
  
  $.ajax({
      url: url,
      type: 'GET',
      data: {},
      success: function (data) {
        $('#list-patients').empty();
        console.log(data.total)

        $.each(data.patients, function (key, value) {
          var status = "Chưa xem"
          if (value.is_downloaded) {
            status = "Đã xem"
          }

          var utc_time = value.created_at + "+00:00";
          var theDate = (new Date(utc_time)).toLocaleString('en-GB')
          // var theDate = new Date(Date.parse(value.created_at));

          $('#list-patients').append("<tr>\
                <td>"+value.document_id+"</td>\
                <td>"+value.name+"</td>\
                <td>"+value.mother_name+"</td>\
                <td>"+value.phone+"</td>\
                <td>"+theDate+"</td>\
                <td>"+status+"</td>\
                <td>"+"Xóa"+"</td>\
                </tr>");
        })
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) { 
        alert("Error: " + errorThrown); 
      },
      cache: false,
      contentType: false,
      processData: false
  });
}

function getPatientsByFilter() {
  var getJustNotViewed = $("#admin-get-viewed").is(":checked");
  var inputName = document.getElementById("admin-filter-name").value
  
  var filterNotViewed = null, filterName = null;
  if (getJustNotViewed) filterNotViewed = false;
  if (inputName) filterName = inputName;

  getPatients(filterName, filterNotViewed);
}

// A $( document ).ready() block.
$(document).ready(function() {
  url = window.location.origin + '/get-patients'
  getPatients();
});


// function createPatient() {
//   if ($('#doc-pdf').prop('files')[0].type != 'application/pdf') {
//     return false
//   }
//   url = window.location.origin + '/create-patient'
//   console.log($('#create-doc-id').val(), $('#create-child-name').val())
//   $.post(url, 
//     {
//       document_id :  $('#create-doc-id').val(),
//       name        :  $('#create-child-name').val(),
//       mother_name :  $('#create-mother-name').val(),
//       phone       :  $('#create-phone').val(),
//       file        :  $('#doc-pdf').prop('files')[0]
//     },
//     function(data, status) {
//       alert('Ngu')

  
//     }).fail(function(){
//       alert('Khon')
//     });
 

//   // return false
// }
