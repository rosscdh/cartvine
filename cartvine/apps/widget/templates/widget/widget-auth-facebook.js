$.ajax({
    url: 'http://localhost:8001/',   // Hard Coded for now
    type: 'GET',
})
.done(function(data, textStatus, jqXHR) {
    data = data.replace('/static/', 'http://localhost:8001/static/')
    $('body').append(data)
})
.fail(function() { 
    console.log("error"); 
})
.always(function() {
});
