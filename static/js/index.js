/* globals tab, */
/* exported parse_url, update_uri, ajax_call */


$('body')
  .tooltip({
    selector: '[data-toggle="tooltip"]',
    container: 'body',
    animation: true,
    html: true,
    sanitize: false,
    boundary: 'window',
    // trigger: "click focus",
    delay: { "show": 100, "hide": 3000 }
  })


$(window).on('load', function () {
  redraw()
})

function redraw() {
  $('[data-toggle="tooltip"]').tooltip('hide')
  const tab_map = {
    home: plot_home,
    // report: plot_report
  }

  $(".loader").removeClass("d-none");
  // funky way to execute stuff
  tab_map[tab]()
}

function ajax_call(url_hit, method = 'GET', bool_async = true) {
  // use get_ajax_call.done(function(data){  <code> })
  return $.ajax({
    url: url_hit,
    async: bool_async,
    method: method,
    dataType: 'json'
  })
}

function parse_url() {
  return g1.url.parse(location.href)
}

function update_uri(obj) {
  var url = g1.url.parse(location.href).update(obj)
  history.pushState({}, '', '?' + url.search);
}

// ___________________________ PLOT Fns___________________________________________

function plot_home() {

  $.when(
    // http://bl.ocks.org/lorenzopub/820bec1dafa6a5cd11aa23c1268edcbf
    $("#word_cloud_holder").fadeTo("slow", 0.05)
    ,
    $.ajax({
      url: "../get_donut",
      method: "POST",
      dataType: 'json'
    })
      .done(function (data) {
        plot_donut({ selector: "#donut_chart_holder", data: data, height: 500 })
      })
    ,
    $.ajax({
      url: "../get_wordcloud",
      method: "POST",
      dataType: 'json'
    })
      .done(function (data) {
        // $("#word_cloud_holder").empty()
        // $("#word_cloud_holder").append(data)
        $("#word_cloud_holder").fadeTo("slow", 1)
        $("#word_cloud_holder").attr("src", data.img)
      })
  )
    .then(function () {
      $(".loader").addClass("d-none");
    })

}
