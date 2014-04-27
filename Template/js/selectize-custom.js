// <select id="select-to"></select>

var REGEX_EMAIL = '([a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@' +
                  '(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)';

var formatName = function(item) {
    return $.trim((item.first_name || '') + ' ' + (item.last_name || ''));
};

$('#select-to').selectize({
    persist: false,
    maxItems: null,
    valueField: 'email',
    labelField: 'name',
    searchField: ['first_name', 'last_name', 'email'],
    sortField: [
        {field: 'first_name', direction: 'asc'},
        {field: 'last_name', direction: 'asc'}
    ],
    options: [
        {email: 'nikola@tesla.com', first_name: 'Nikola', last_name: 'Tesla'},
        {email: 'brian@thirdroute.com', first_name: 'Brian', last_name: 'Reavis'},
        {email: 'someone@gmail.com'}
    ],
    render: {
        item: function(item, escape) {
            var name = formatName(item);
            return '<div>' +
                (name ? '<span class="name">' + escape(name) + '</span>' : '') +
                (item.email ? '<span class="email">' + escape(item.email) + '</span>' : '') +
            '</div>';
        },
        option: function(item, escape) {
            var name = formatName(item);
            var label = name || item.email;
            var caption = name ? item.email : null;
            return '<div>' +
                '<span class="label">' + escape(label) + '</span>' +
                (caption ? '<span class="caption">' + escape(caption) + '</span>' : '') +
            '</div>';
        }
    },
    create: function(input) {
        if ((new RegExp('^' + REGEX_EMAIL + '$', 'i')).test(input)) {
            return {email: input};
        }
        var match = input.match(new RegExp('^([^<]*)\<' + REGEX_EMAIL + '\>$', 'i'));
        if (match) {
            var name       = $.trim(match[1]);
            var pos_space  = name.indexOf(' ');
            var first_name = name.substring(0, pos_space);
            var last_name  = name.substring(pos_space + 1);

            return {
                email: match[2],
                first_name: first_name,
                last_name: last_name
            };
        }
        alert('Invalid email address.');
        return false;
    }
});

$('#input-tags').selectize({
  delimiter: ',',
  persist: false,
  createOnBlur: true,
  create: function(input) {
    return {
      value: input,
      text: input
    }
  }
});


$('#select-beast').selectize({
  create: true,
  sortField: {
    field: 'text',
    direction: 'asc'
  },
  dropdownParent: 'body'
});

$('#select-beast-disabled').selectize({
  create: true,
  sortField: {field: 'text'}
});

$('#select-state').selectize({
          maxItems: 3
        });

$('#select-country').selectize();

$('#select-state-disabled').selectize({
          maxItems: 3
        });


        $('#confirm-delete').selectize({
    delimiter: ',',
    persist: false,
    onDelete: function(values) {
        return confirm(values.length > 1 ? 'Are you sure you want to remove this ' + values.length + ' item?' : 'Are you sure you want to remove "' + values[0] + '"?');
    }
});


// <select id="select-repo"></select>
$('#select-repo').selectize({
    theme: 'repositories',
    valueField: 'url',
    labelField: 'name',
    searchField: 'name',
    options: [],
    create: false,
    render: {
        option: function(item, escape) {
            return '<div>' +
                '<span class="title">' +
                    '<span class="name"><i class="icon ' + (item.fork ? 'fork' : 'source') + '"></i>' + escape(item.name) + '</span>' +
                    '<span class="by">' + escape(item.username) + '</span>' +
                '</span>' +
                '<span class="description">' + escape(item.description) + '</span>' +
                '<ul class="meta">' +
                    (item.language ? '<li class="language">' + escape(item.language) + '</li>' : '') +
                    '<li class="watchers"><span>' + escape(item.watchers) + '</span> watchers</li>' +
                    '<li class="forks"><span>' + escape(item.forks) + '</span> forks</li>' +
                '</ul>' +
            '</div>';
        }
    },
    score: function(search) {
        var score = this.getScoreFunction(search);
        return function(item) {
            return score(item) * (1 + Math.min(item.watchers / 100, 1));
        };
    },
    load: function(query, callback) {
        if (!query.length) return callback();
        $.ajax({
            url: 'https://api.github.com/legacy/repos/search/' + encodeURIComponent(query),
            type: 'GET',
            error: function() {
                callback();
            },
            success: function(res) {
                callback(res.repositories.slice(0, 10));
            }
        });
    }
});

$('.input-tags').selectize({
    plugins: ['remove_button'],
    delimiter: ',',
    persist: false,
    create: function(input) {
        return {
            value: input,
            text: input
        }
    },
    render: {
        item: function(data, escape) {
            return '<div>"' + escape(data.text) + '"</div>';
        }
    },
    onDelete: function(values) {
        return confirm(values.length > 1 ? 'Are you sure you want to remove these ' + values.length + ' items?' : 'Are you sure you want to remove "' + values[0] + '"?');
    }
});


