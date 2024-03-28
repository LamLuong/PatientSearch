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