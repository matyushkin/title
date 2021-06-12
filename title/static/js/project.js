let results = []
let current_string = ''
let title = document.getElementById('title')
let suggest = document.getElementById('suggest')
let explanation = document.getElementById('explanation')
let titles = document.getElementById('titles')
let link_titles = document.getElementById('link-titles')
let tag_buttons = document.querySelectorAll('.entity')
let tags

// для простейшей группировки запросов
let group_id = localStorage.getItem('group_id');
let cashed = JSON.parse(localStorage.getItem('cashed'));

if (group_id === null) {
  group_id = Math.floor(Math.random() * 2147483647)
  localStorage.setItem('group_id', group_id)
}

if (cashed === null) {
  cashed = {}
  localStorage.setItem('cashed', JSON.stringify(cashed))
}

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


function update_cash() {
  if (Object.keys(cashed).length !== 0) {
    titles.hidden = true
    link_titles.hidden = false
    show_cash()
  } else {
    link_titles.hidden = true
  }
}


function add_cash_removing() {
  let clear_titles = document.getElementById('clear-titles')
  clear_titles.onclick = function() {
    cashed = {}
    localStorage.setItem('cashed', JSON.stringify(cashed))
    titles.hidden = true
    link_titles.hidden = true 
  }
}


function show_cash() {
  titles.innerHTML = ''
  link_titles.onclick = function() {
    if (titles.hidden === true) {
      if (titles.childElementCount > 0) {
        titles.removeChild(ul)
      }
      ul = document.createElement('ul')
      for (key in cashed) {
        li = document.createElement('li')
        li.innerHTML = `${key}, <b>${cashed[key][1].toFixed(1)}</b>`
        ul.appendChild(li)
      }
      li = document.createElement('li')
      li.innerHTML = '<a id="clear-titles" href="#">Очистить список</a>'
      ul.appendChild(li)
      titles.appendChild(ul)
      add_cash_removing()
      titles.hidden = false
    } else {
      titles.hidden = true
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
        titles.hidden = true
        results.push(json)
        r = results[results.length-1]     
        title.innerHTML = r['title_html']
        suggest.innerHTML = r['suggest_html']
        tags = r['tags']
        i = Object.keys(cashed).length
        cashed[r['text']] = [i, r['rating']]
        localStorage.setItem('cashed', JSON.stringify(cashed))
        explanation.innerHTML = '<div class="explanation"><p>Нажмите на любой из тегов, чтобы увидеть пояснение.</p></div>'
        tag_buttons = document.querySelectorAll('.entity')
        add_explanation(tag_buttons)
        update_cash()
    },

    error : function(xhr,errmsg,err) {
        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more cashed about the error to the console
    }
  });
};

update_cash()