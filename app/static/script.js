function loadData() {

    var $body = $('#body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    var streetStr = $("#street").val()
    var cityStr = $("#city").val()
    var stateStr = $("#state").val()
    var address = streetStr + ", " + cityStr + ", " + stateStr;
    
    if($("img").length <= 0) {
        $greeting.text("Here is some information about " + address + ".");
        var streetviewUrl = "https://maps.googleapis.com/maps/api/streetview?size=400x200&location=" + address + "&key=AIzaSyDOnmHKt4bMXj-QL8pKeHd4yCyTL8-IzUc";
        $body.append("<img class='thumbnail center-block' src='"+ streetviewUrl + "'>");
    } else {
        console.log("do nothing")
    }

    
    var API = "https://api.nytimes.com/svc/search/v2/articlesearch.json?q="
    var KEY = "&sort=newest&api-key=b2f92fb98088b256316d8584e1aaca61:13:70248560"
    var URL = API + cityStr + KEY
    $.getJSON(URL, function( data ) {
         $nytHeaderElem.text("New York Times Articles About " + cityStr + ", " + stateStr);
            var articles = data.response.docs;
            for (var i = 0; i < articles.length; i++ ) {
                var article = articles[i];
                $nytElem.append("<li class='thumbnail bg-thumb'>" + "<a href='"+ article.web_url +"' target='_blank'>" + article.headline.main +"</a>" + "<p>" + article.snippet + "</p></li>");
         };
    }).error(function(e) {
        $nytElem.text("Ny Times Couldn't be loaded at this time")
    });

    var wikiRequestTimeout = setTimeout(function(){
        $wikiElem.text("failed to get wikipedia resources"); 
    }, 8000);

    var wikiURL = "https://en.wikipedia.org/w/api.php?action=opensearch&search=" + cityStr + "&format=json&callback=wikiCallback";
    $.ajax({
        url: wikiURL,
        dataType: "jsonp",
        success: function ( data ) {
            var articleList = data[1]
            for (var i = 0; i < articleList.length; i++) {
                articleStr = articleList[i]
                var url = "https://en.wikipedia.org/wiki/" + articleStr;
                $wikiElem.append("<li><a href='" + url + "' target='_blank'>" + articleStr + "</a></li>");
            }; 
            clearTimeout(wikiRequestTimeout);
        }
    })
    return false;
};

$('#form-container').submit(loadData);
