function init() {
    $('#form-inline').submit(function(e) {
        e.preventDefault();
        var query = $('#query').val();
        search(query);        
    });

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('q')) {
        $('#query').val(urlParams.get('q'));
        $('#form-inline').submit();
    }
    
    $("#im-feeling-lucky").click(function() {
        alert('Please do not click this button.');
        $(this).unbind('click').click(function() {
            alert('Please DO NOT click this button.');
            $(this).unbind('click').click(function() {
                alert("Seriously. Don't.");
                $(this).css({'position': 'relative', 'left': 200, 'top': 40});                
                $(this).unbind('click').click(function() {
                    $(this).css({'position': 'relative', 'left': 400, 'top': -200});       
                    $(this).unbind('click').click(function() { 
                        $(this).css('visibility', 'hidden');
                        alert(':)');
                        window.location.href = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
                    });
                });
            });
        });
    });
}

function search(query) {
    $('#results').css('opacity', 0.2);
    $.get('search', {q: query}).done(function(response) {    
        $('#loading').hide();
        if (response.hasOwnProperty('error')) {
            window.alert(response['error']);
            $('#results').html('');
            $('#query').focus();
            return;
        }

        $('#results').html('');
        $('#results').append('<p id="info">Około ' + response.results_count + ' wyników (' + response.search_time.toFixed(2).toString().replace('.', ',') + ' s)</p>');
        $("#results").append('<img src="correlations.png?' + Math.floor(Math.random() * 1e9) + '" alt="" id="correlations_plot">');
        response.results.forEach(function(result) {
            var elem = $('<div id="result"></div>').appendTo('#results');
            elem.append('<h2 class="name"><a href="' + result.url + '" target="_blank">' + highlight(result.name, query) + '</a></h2>');
            elem.append('<span class="url">' + result.url + '</span>');
            elem.append('<span class="correlation">' + (result.correlation * 100).toFixed(2) + '%</span>');
            elem.append('<p class="content"`>' + highlight(truncate(result.content, 300), query) + '</p>');
        });
        $('#results').css('opacity', 1);

        var url = '?q=' + encodeURIComponent(query).replace(/%20/g, '+');
        document.title = query + ' – AGHoogle';
        window.history.pushState(null, null, url);
    });
}

function truncate(string, maxlength) {
    if (maxlength >= string.length) {
        return string;
    }
    var i_max = 0;
    var hellip = false;
    while (true) {
        var i = string.indexOf(' ', i_max+1);
        if (i == -1 || i > maxlength) {
            hellip = true;
            break;
        }
        i_max = i;
    }
    return string.substring(0, i_max) + (hellip ? '&hellip;' : '');
}

function highlight(where, what) {
    what.split(' ').filter(function(term) {
        return term.length > 0;
    }).forEach(function(term) {
        var re = new RegExp('(^|[^a-z])(' + term.replace(/[^a-zA-Z0-9]/, '') + ')([^a-z]|$)', 'gi');
        where = where.replace(re, '$1<strong>$2</strong>$3');
    });
    return where;
}

$(init);
