/* exported plot_donut */

function plot_donut(config) {

  let selector = config.selector || "body",
    margin = config.margin || { top: 10, right: 25, bottom: 10, left: 25 },
    width = config.width || $(selector).width(),
    height = config.height || $(selector).height(),
    radius = width / 4,
    data = config.data ||
      [
        { name: 'positive', count: 3, percentage: 2, color: '#000000' },
        { name: 'negative', count: 10, percentage: 8, color: '#f8b70a' },
        { name: 'neutral', count: 17, percentage: 15, color: '#6149c6' },
      ];

  var _max_txt = _.maxBy(data, 'percentage')['name']
  // let color = d3.scaleOrdinal(d3.schemeCategory20c)
  // let color = d3.scaleOrdinal(d3.schemeCategory10)
  let color = d3.scaleOrdinal(['#9ACD32', '#ABADE4', '#ED4433'])
    .domain(['positive', 'neutral', 'negative'])



  var arc = d3.arc()
    .outerRadius(radius - 32)
    .innerRadius(100);

  var pie = d3.pie()
    .sort(null)
    .value(function (d) {
      return d.count;
    });

  $(selector).empty()
    .data("chart-data", data)

  var svg = d3.selectAll(selector)
    .append("svg")
    .attr("viewBox", `0 0 ${(width + margin.left + margin.right)} ${(height + margin.top + margin.bottom)}`)
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("preserveAspectRatio", "xMidYMid")

  var g = svg
    .append("g")
    .attr("transform", `translate(${(width + margin.left + margin.right) / 2} , ${(height - margin.top - margin.bottom) / 2})`)
    .selectAll(".arc")
    .data(pie(data))
    .enter().append("g");

  g.append("path")
    .attr("d", arc)
    .style('fill', d => color(d.data.name))
    .transition().delay(function (d, i) { return (i + 1) * 500; }).duration(500)
    .attrTween('d', function (d) {
      var i = d3.interpolate(d.startAngle + 0.1, d.endAngle);
      return function (t) {
        d.endAngle = i(t);
        return arc(d);
      }
    })


  g.append("text")
    .attr("transform", function (d) {
      var _d = arc.centroid(d);
      _d[0] *= 1;	//multiply by a constant factor
      _d[1] *= 1;	//multiply by a constant factor
      return "translate(" + _d + ")";
    })
    .attr("dy", ".50em")
    .style("text-anchor", "middle")
    .text(function (d) {
      if (d.data.percentage < 8) {
        return '';
      }
      return parseInt(d.data.percentage) + '%';
    });

  g.append("text")
    .attr("text-anchor", "middle")
    .attr('font-size', '2em')
    .attr('y', 20)
    .text(_max_txt)

  svg.append("g")
    .attr("class", "legendSequential")
    .attr("transform", `translate(${margin.left} , ${height - margin.bottom - margin.top})`)

  var legendSequential = d3.legendColor()
    .shapeWidth(width / data.length)
    .cells(data.length)
    .orient("horizontal")
    .scale(color)

  svg.select(".legendSequential")
    .call(legendSequential);

}
