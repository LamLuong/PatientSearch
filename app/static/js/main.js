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
    alert("ngu")
  });
});
