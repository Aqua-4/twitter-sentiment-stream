# $.template

`$.template()` renders HTML templates with JavaScript mixed inside them.

Example:

```html
<script type="text/html">Your platform is <%= navigator.userAgent %></script>
<script>
  $('body').template()
</script>
```

renders all `script[type="text/html"]` as [lodash templates](https://lodash.com/docs/#template).
This displays `Your platform is ...` and shows the userAgent just below the script tag.

- Anything inside `<% ... %>` is executed as Javascript.
- Anything inside `<%= ... %>` is evaluated and rendered in-place.

The template can use all global variables. You can pass additional variables
using as `.template({var1: value, var2: value, ...})`. For example:

```html
<script type="text/html">
  <% list.forEach(function(item) { %>
    <div><%= item %></div>
  <% }) %>
</script>
<script>
  $('body').template({list: ['a', 'b', 'c']})
</script>
```

To re-render the template, run `.template(data)` again with different data.


## $.template animation

When using `type="text/html"`, templates are re-rendered. To *update* existing
elements, use `data-engine="vdom"` instead. This only changes attributes or
elements that need change. This allows us to animate attributes via CSS.

You need to include [morphdom](https://github.com/patrick-steele-idem/morphdom)
for this to work.

For example, this shows a circle in SVG bouncing around smoothly.

```html
<style>
  circle { transition: all 1s ease; }
</style>
<script src="../node_modules/morphdom/dist/morphdom-umd.min.js"></script>
<script type="text/html">
  <svg width="100" height="100">
    <circle cx="<%= x %>" cy="<%= y %>" r="5" fill="red"/>
  </svg>
</script>
<script>
  setInterval(function() {
    var x = Math.random() * 100
    var y = Math.random() * 100
    $('body').template({x: x, y: y})    // Update the template to animate
  }, 1000)
</script>
```

You can also specify a `data-engine` via an option. For example:

```js
$('script.animate').template(data, {engine: 'vdom'})
```


## $.template targets

To re-use the template or render the same template on a different DOM node,
run `.template(data, {target: selector})`. This allows you to declare templates
once and apply them across the body. For example:

```js
$('script.chart')
    .template({heading: 'Dashboard 1'}, {target: '.dashboard1'})
    .template({heading: 'Dashboard 2'}, {target: '.dashboard2'})
    .template({}, {target: '.no-heading'})
```

The target can also be specified via a `data-target=".dashboard1"` on the script
template. This is the same as specifying `{target: '.dashboard'}`. For example:

```html
<script class="chart" data-target=".dashboard1">...</script>
<script class="chart" data-target=".dashboard2">...</script>
```


## $.template append

To append instead of replacing, run `.template(data, {append: true})`. Every
time `.template` is called, it appends rather than replaces. For example:

```js
$('script.list')
    .template({heading: 'Item 1'}, {append: true}),   // Appends the heading
    .template({heading: 'Item 2'}, {append: true}),   // instead of replacing it
```

You can also specify this as `<script data-append="true">`. This helps append to
an existing target. For example:

```html
<script class="list" data-append="true" data-target=".existing-list">...</script>
<ul class="existing list">
  <li>Existing item</li>
  <!-- Every time .template() is called, the result is added as a list item here -->
</ul>
```


## $.template external source

Template containers can have an `src=` attribute that loads the template from a file:

```html
<script type="text/html" src="template.html"></script>
<script>
  $('body').template()
</script>
```

If the `src=` URL returns a HTTP error, the HTML *inside* the script is rendered
as a template. The template can use:

- all data passed by the `$().template()` function, and
- an [xhr](http://api.jquery.com/Types/#jqXHR) object - which has error details.

For example:

```html
<script type="text/html" src="missing.html">
  Template returned error code: <%= xhr.status %>.
  Data is <%= data %>
</script>
<script>
  $('body').template({data: data})
</script>
```

## $.template selector

`$().template()` renders all `script[type="text/html"]` nodes in or under the
selected node. Use `data-selector=` attribute to change the selector. For
example:

```html
<section data-selector="script.lodash-template">
  <script class="lodash-template">...</script>
</section>
<script>
  $('section').template()
</script>
```

You can also render a template by selecting it directly. For example:

```html
<script>
  $('script.lodash-template').template()
</script>
```


## $.template events

- `template` is fired on the source when the template is rendered. Attributes:
    - `templatedata`: the passed data
    - `target`: the target nodes rendered, as a jQuery object

For example:

```js
$('script[type="text/html"]')
  .on('template', function(e) {       // Returns nodes rendered by the template
    e.target                          // Get the target nodes
      .filter('div')                  // Filter all <div> elements inside
      .attr('class', 'item')          // Change their class
  })
  .template()                         // Trigger the template AFTER binding the event handler
```
