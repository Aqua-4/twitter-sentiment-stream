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
      url: "../get_pie",
      method: "POST",
      dataType: 'json'
    })
      .done(function (data) {

        $("#pie_chart_holder").attr("src", data.img)
      })
  )
    .then(function () {
      $(".loader").addClass("d-none");
    })

}
