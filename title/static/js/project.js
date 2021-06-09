let results = []
let title = document.getElementById("title")
let rating = document.getElementById("rating")
let suggest = document.getElementById("suggest")

//localStorage.setItem("titles", "Старые заголовки");
//document.getElementById("titles").innerHTML = localStorage.getItem("titles");

$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_title();
});


function create_title() {
  $.ajax({
    url : "create_title/", // the endpoint
    type : "POST", // http method
    data : { text : $('#title-text').val() }, // data sent with the post request

    success : function(json) {
        // $('#title-text').val(''); // remove the value from the input
        results.push(json)
        r = results[results.length-1]     
        rating.innerHTML = r['rating_html']
        title.innerHTML = r['title_html']
        suggest.innerHTML = r['suggest_html']
        console.log(results); // log the returned json to the console
    },

    error : function(xhr,errmsg,err) {
        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
};


