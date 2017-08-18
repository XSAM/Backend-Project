var bindEventTodoButtonAdd = function () {
    var addButton = e('#todo-button-add')
    addButton.addEventListener('click', function (event) {
        var input = e('#todo-form-add').querySelector('.mdl-textfield__input')
        var title = input.value
        log('add value:', title)
        var data = {
            title: title,
            token: getToken(),
        }
        apiTodoAdd(data, function (r) {
            reloadPageIfSuccess(r)
        })
    })
}

var bindEventTodoButtonEdit = function () {
    var addButton = e('#todo-button-edit')
    addButton.addEventListener('click', function (event) {
        var id = e('#todo-form-edit').dataset.id
        log('id', id)
        if (id !== undefined){
            var input = e('#todo-form-edit').querySelector('.mdl-textfield__input')
            var title = input.value
            var data = {
                id: id,
                title: title,
                token: getToken(),
            }
            apiTodoEdit(data, function (r) {
                reloadPageIfSuccess(r)
            })
        }
    })
}

var bindEventTodoComplete = function () {
    var todoList = document.getElementsByClassName('todo-list')
    for (var i = 0; i < todoList.length; i++) {
        todoList[i].addEventListener('click', function (event) {
            var self = event.target
            if (self.classList.contains('mdl-checkbox__input')) {
                var todoCell = self.closest('.todo-list')
                var id = todoCell.dataset.id
                log('id', id)
                // 因为早于处理的JS，所以是相反的
                if (todoCell.classList.contains('is-selected')) {
                    var data = {
                        id: id,
                        token: getToken(),
                        complete: false
                    }
                    apiTodoComplete(data, function (r) {
                        log('not complete')
                    })
                }
                else {
                    var data = {
                        id: id,
                        token: getToken(),
                        complete: true
                    }
                    apiTodoComplete(data, function (r) {
                        log('complete')
                    })
                }
            }
        })
    }
}

var bindEventTodoEdit = function () {
    var todoList = document.getElementsByClassName('todo-list')
    for (var i = 0; i < todoList.length; i++) {
        todoList[i].addEventListener('click', function (event) {
            var self = event.target
            if (self.classList.contains('todo-edit')) {
                var todoCell = self.closest('.todo-list')
                log(todoCell.querySelector('.todo-title'))
                var title = todoCell.querySelector('.todo-title').innerText
                var id = todoCell.dataset.id
                var form = e('#todo-form-edit')
                form.dataset.id = id

                // prompt material animation
                var edit_div = form.querySelector('.mdl-textfield')
                edit_div.className += ' is-dirty is-focused'

                var input = form.querySelector('.mdl-textfield__input')
                input.value = title
                input.focus()
            }
        })
    }
}

var bindEventTodoDelete = function () {
    var todoList = document.getElementsByClassName('todo-list')
    for (var i = 0; i < todoList.length; i++) {
        todoList[i].addEventListener('click', function (event) {
            var self = event.target
            if (self.classList.contains('todo-delete')) {
                var todoCell = self.closest('.todo-list')
                var id = todoCell.dataset.id
                var data = {
                    id: id,
                    token: getToken()
                }
                apiTodoDelete(data, function (r) {
                    reloadPageIfSuccess(r)
                })
            }
        })
    }
}

var checkCompleted = function () {
    var todoList = document.getElementsByClassName('todo-list')
    for (var i = 0; i < todoList.length; i++) {
        log(todoList[i])
        if (todoList[i].dataset.completed === 'True') {
            var checkbox = todoList[i].querySelector('.mdl-checkbox')
            log(checkbox)
            checkbox.click()
            // tye to clear focus, but not working
            //checkbox.blur()
        }
    }
}

var clearFocus = function () {
    document.activeElement.blur();
}

var getToken = function () {
    var self = e('#csrf-token')
    return self.dataset.token
}

var reloadPageIfSuccess = function(r) {
    if (r === 'success') {
        log('added')
        location.reload()
    }
}

// I hate this checkbox
var removeSelectAllCheckbox = function () {
    var checkbox = e('.mdl-checkbox')
    checkbox.remove()
}

var bindEvents = function () {
    bindEventTodoButtonAdd()
    bindEventTodoButtonEdit()
    bindEventTodoComplete()
    bindEventTodoEdit()
    bindEventTodoDelete()
}

var __main = function () {
    removeSelectAllCheckbox()
    checkCompleted()
    clearFocus()
    bindEvents()
}

// I need rendered page, but the render JS cost too much time
$(window).on("load", function(){
  // Handler when all assets (including images) are loaded
    __main()
});

// not working
// window.onload = function() {
//     //dom not only ready, but everything is loaded
//     __main()
// };

// simple but magic
// setTimeout(__main, 1000)
