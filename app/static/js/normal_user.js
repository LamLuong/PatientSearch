$("#authUser").click(function() {
  url = window.location.origin + '/api/v1/login';

  $.post(url,
  {
    username: $('#username').val(),
    password: $('#password').val()
  },
  function(data, status) {
    window.location.replace(window.location.origin);

  }).fail(function(){
    alert("Wrong username or password");
  });
});


$("#search-patient").click(function() {
  let url = window.location.origin + '/get-patient';
  let doc_id = $('#search-with-id').val();

  if (!doc_id) {
    alert("Trường tìm kiếm không được để trống");
    return false;
  }
  $.get(url, { document_id :  doc_id},
  function(data, status) {
  
    $('#not-found-search-result').hide();
    $('#child-name').text(data.name);
    $('#mother-name').text(data.mother_name);
    $('#mother-phone').text(data.phone);

    doc_url = window.location.origin + '/patient-doc/?document_name=' + doc_id + ".pdf";
    $('#document-name-url').attr("href", doc_url);

    $("#search-result").css("visibility", "visible");

  }).fail(function(){
    $("#search-result").css("visibility", "hidden");
    $('#not-found-search-result').show();
  });
});
