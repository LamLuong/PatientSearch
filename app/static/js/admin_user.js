var current_paging = 1;
var total_page;
const default_record_perpage = 100;

$("#menu-patient-data-page").click(function() {
  $('#menu-search-page').removeClass('active');
  $('#menu-patient-data-page').addClass('active');
  $("#search").css("display", "none");
  $("#add-patient-doc").css("display", "block");
  $("#update-patient-doc").css("display", "block");
});

$("#menu-search-page").click(function() {
  $('#menu-search-page').addClass('active');
  $('#menu-patient-data-page').removeClass('active');

  $("#add-patient-doc").css("display", "none");
  $("#update-patient-doc").css("display", "none");
  $("#search").css("display", "block");
});

$("#logout").click(function() {
  url = window.location.origin + '/api/v1/logout';

  $.post(url, { foo : null },
  function(data, status) {
    window.location.replace(window.location.origin);
  }).fail(function(){
    alert("Invalid token");
  });
});

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
  url = window.location.origin + '/create-patient';
  $.ajax({
      url: url,
      type: 'POST',
      data: formData,
      success: function (data) {
          alert("Thêm thông tin bệnh nhân thành công");
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) { 
        alert("Error: Không được trùng mã bệnh án");
      },
      cache: false,
      contentType: false,
      processData: false
  });
});

function getPatientsByFilter(offset=1) {
  var getJustNotViewed = $("#admin-get-viewed").is(":checked");
  var inputName = document.getElementById("admin-filter-name").value;
  
  var filterNotViewed = null, filterName = null;
  if (getJustNotViewed) filterNotViewed = false;
  if (inputName) filterName = inputName;

  getPatients(filterName, filterNotViewed, offset);
}

function UpdateViewByFilter() {
  current_paging = 1;
  getPatientsByFilter();
}

function goToPaging(obj, direct=true) {
  
  if (obj !== null) {
    current_paging = $(obj).text();
  } else {
    if (!direct)
      current_paging = parseInt(current_paging) - 1;

    if (direct)
      current_paging = parseInt(current_paging) + 1;
  }
  
  if (current_paging < 1) {
    current_paging = 1;
    return;
  }
  
  if (current_paging > total_page) {
    current_paging = total_page;
    return;
  }
  
  getPatientsByFilter(current_paging);
}

function dropDownGotoPage() {
  input_page = document.getElementById('goto-page-dropdown-menu').children[0].children[0];
  if (input_page.reportValidity()) {
    current_paging = input_page.value;
    getPatientsByFilter(current_paging);
  }
}

function deletePatient(obj) {
  doc_id = $(obj).parent().parent().children(':first-child').text();
  url = window.location.origin + '/delete-patient/' + doc_id;
  $.ajax({
    url: url,
    type: 'DELETE',
    data: {},
    success: function (data) {
      getPatientsByFilter(current_paging);
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) { 
      alert("Error: " + errorThrown); 
    },
    cache: false,
    contentType: false,
    processData: false
  });
}

function showGotoPageDropdown() {
  let x = document.getElementById("goto-page-dropdown-menu");

  if($('#goto-page-dropdown-menu').css('display') == 'none') {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}

function getPatients(name = null, seen = null, offset = 1) {
  url = window.location.origin + '/get-patients?';
  if (name !== null) {  
    url = url + 'name=' + name;
  }
  if (seen !== null) {  
    url = url + '&seen=' + seen;
  }

  url = url + '&offset=' + offset;
  
  $.ajax({
      url: url,
      type: 'GET',
      data: {},
      success: function (data) {
        $('#list-patients').empty();
        $('#data-paging-idx').empty();

        $.each(data.patients, function (key, value) {
          var status = "Chưa xem";
          if (value.is_downloaded) {
            status = "Đã xem";
          }

          let utc_time = value.created_at + "+00:00";
          let theDate = (new Date(utc_time)).toLocaleString('en-GB');
          // var theDate = new Date(Date.parse(value.created_at));

          $('#list-patients').append('<tr>\
                <td>'+value.document_id+'</td>\
                <td>'+value.name+'</td>\
                <td>'+value.mother_name+'</td>\
                <td>'+value.phone+'</td>\
                <td>'+theDate+'</td>\
                <td>'+status+'</td>\
                <td> <a class="delete-patient" onClick="deletePatient(this)">Xóa</a></td>\
                </tr>');
        });


        $('#data-paging-idx').append('<li class="page-item">\
                                        <a class="page-link" onClick="goToPaging(null, false)" style="cursor: default" aria-label="Previous">\
                                          <span aria-hidden="true">&laquo;</span>\
                                        </a>\
                                      </li>');
        // $('#data-paging-idx').append('<li class="page-item"><a class="page-link active" onClick=goToPaging(this) style="cursor: pointer">'+i+'</a></li>');
        total_page = Math.ceil(data.total / default_record_perpage);
        if (current_paging > total_page) {
          current_paging = total_page;
        }

        for (i = 1; i <= total_page; i++) {
          if (i < 4 || i == total_page) {
            if (i == current_paging) {
              $('#data-paging-idx').append('<li class="page-item"><a class="page-link active" onClick=goToPaging(this) style="cursor: pointer">'+i+'</a></li>');
            } else {
              $('#data-paging-idx').append('<li class="page-item"><a class="page-link" onClick=goToPaging(this) style="cursor: pointer">'+i+'</a></li>');
            }
          } else if (i == 4) {
            if (current_paging >= 4 && current_paging < total_page) {
              $('#data-paging-idx').append('<li class="page-item"><a class="page-link active" style="cursor: default">' + current_paging + '</a></li>');
            }
            $('#data-paging-idx').append('<li class="page-item">\
                                            <a class="page-link" style="cursor: default; margin-bottom: 12px" onClick=showGotoPageDropdown()>...</a>\
                                            <div class="goto-page-dropdown-content arrow-top" id="goto-page-dropdown-menu">\
                                              <div class="input-group popup-wrapper">\
                                                <input type="number" class="form-control" min="1" max="'+total_page+'" placeholder="Tới trang">\
                                                <button type="button" class="btn btn-success" onClick=dropDownGotoPage()> Đi </button>\
                                              </div>\
                                            </div>\
                                          </li>');
          }
        }

        $('#data-paging-idx').append('<li class="page-item">\
                                        <a class="page-link" onClick="goToPaging(null, true)" style="cursor: default" aria-label="Next">\
                                          <span aria-hidden="true">&raquo;</span>\
                                        </a>\
                                      </li>');
        
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) { 
        alert("Error: " + errorThrown); 
      },
      cache: false,
      contentType: false,
      processData: false
  });
}

// A $( document ).ready() block.
$(document).ready(function() {
  url = window.location.origin + '/get-patients';
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
