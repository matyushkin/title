let results = []
let current_string = ''
let title = document.getElementById('title')
let suggest = document.getElementById('suggest')
let explanation = document.getElementById('explanation')

let tag_buttons = document.querySelectorAll('.entity')
let tags


// для простейшей группировки запросов между обновлениями страницы
let group_id = Math.floor(Math.random() * 2147483647)

//localStorage.setItem("titles", "Старые заголовки");
//document.getElementById("titles").innerHTML = localStorage.getItem("titles");

$('#post-form').on('submit', function(event){
    event.preventDefault()
    let new_string = $('#title-text').val()
    if (new_string == current_string)
    {
      explanation.innerHTML = '<p style="color:Tomato;">Для получения новой оценки измените заголовок.'
      console.log('Для получения новой оценки поменяйте заголовок.')
    } else {
      console.log('Отправлена форма заголовка.')
      current_string = new_string
      create_title()
    }    
})


function render_explanation(tag_name) {
  let description = tags[tag_name]
  let definition = description['definition']
  let examples = description['examples']
  s = '<div class="explanation">'
  s += `<p><button class="entity">${tag_name}</button></p>`
  s += `<p>${definition}.</p>`
  s += `<p>Примеры: <i>${examples.join('</i>, <i>')}</i>.</p>`
  s += '</div>'
  explanation.innerHTML = s
}


function add_explanation(tag_buttons) {
  for (const btn of tag_buttons) {
    btn.onclick = function() {
      render_explanation(btn.value)
    }
  }
}


function create_title() {
  $.ajax({
    url: "create_title/",
    type: "POST",
    data: {
      text : $('#title-text').val(),
      group_id: group_id,
    },

    success : function(json) {
        // $('#title-text').val('');
        console.log('Получен новый результат.')
        results.push(json)
        r = results[results.length-1]     
        title.innerHTML = r['title_html']
        suggest.innerHTML = r['suggest_html']
        tags = r['tags']
        explanation.innerHTML = '<div class="explanation"><p>Нажмите на любой из тегов, чтобы увидеть пояснение.</p></div>'
        tag_buttons = document.querySelectorAll('.entity')
        add_explanation(tag_buttons)
    },

    error : function(xhr,errmsg,err) {
        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
};




