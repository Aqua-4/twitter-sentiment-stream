# g1

`g1` is library of interaction patterns in [Gramex](https://learn.gramener.com/guide/g1/).

Install using:

```bash
yarn install g1
# ... OR ...
npm install --save g1
```

To use all features, add this to your HTML:

```html
<script src="node_modules/g1/dist/g1.min.js"></script>
<script src="node_modules/g1/dist/mapviewer.min.js"></script>
```

## Interactions

- [$.urlfilter](docs/urlfilter.md) changes URL query parameters when clicked. Used to filter data.
- [$.urlchange](docs/urlchange.md) listens to hash changes and routes events
- [$.search](docs/search.md) highlights elements as you type in a search box
- [$.highlight](docs/highlight.md) toggles classes on elements when clicked or hover

## Components

- [$.formhandler](docs/formhandler.md) renders a HTML table from a [FormHandler URL](https://learn.gramener.com/guide/formhandler/)
- [$.template](docs/template.md) renders lodash templates. Requires [lodash](https://lodash.com/)
- [$.dropdown](docs/dropdown.md) renders a Bootstrap dropdown. Requires [Bootstrap](https://getbootstrap.com/docs/4.2/)
- [$.translate](docs/translate.md) translates text to other languages using [Gramex translate](https://learn.gramener.com/guide/translate/)
- [g1.sanddance](docs/sanddance.md) moves DOM elements smoothly based on data
- [g1.mapviewer](docs/mapviewer.md) renders leaflet maps and simplifies adding layers from data.
    - Note: Mapviewer is not included in [g1.min.js](dist/g1.min.js). Include [mapviewer.min.js](dist/mapviewer.min.js)

## Utilities

- [g1.url.parse](docs/url.md) parses a URL into a structured object
    - [url.join](docs/url.md#urljoin) joins two URLs
    - [url.update](docs/url.md#urlupdate) updates a URL's query parameters
- [$.ajaxchain](docs/ajaxchain.md) chains AJAX requests, loading multiple items in sequence
- [L.TopoJSON](docs/topojson.md) loads TopoJSON files just like GeoJSON. Requires [topojson](https://github.com/topojson/topojson)
- [$.dispatch](docs/dispatch.md) is like [trigger](https://api.jquery.com/trigger/) but sends a native event (triggers non-jQuery events too)
- [g1.datafilter](docs/datafilter.md) filters the data based on the options
- [g1.types](docs/types.md) returns the data types of columns in a DataFrames

## Libraries

You can import either [g1.min.js](dist/g1.min.js) -- which has all of these functions --
or one of the individual libraries below:

- [ajax.min.js](dist/ajax.min.js)
- [datafilter.min.js](dist/datafilter.min.js)
- [event.min.js](dist/event.min.js)
- [formhandler.min.js](dist/formhandler.min.js)
- [highlight.min.js](dist/highlight.min.js)
- [leaflet.min.js](dist/leaflet.min.js)
- [sanddance.min.js](dist/sanddance.min.js)
- [search.min.js](dist/search.min.js)
- [template.min.js](dist/template.min.js)
- [translate.min.js](dist/translate.min.js)
- [types.min.js](dist/types.min.js)
- [urlchange.min.js](dist/urlchange.min.js)
- [urlfilter.min.js](dist/urlfilter.min.js)

[mapviewer.min.js](dist/mapviewer.min.js) is not part of [g1.min.js](dist/g1.min.js).

For debugging, use [dist/g1.js](dist/g1.js) -- an un-minified version.

## Releases

[CHANGELOG](CHANGELOG.md) mentions all release changes.

Brief notes with examples are described in Gramex releases. For example:

- [v0.12](https://learn.gramener.com/guide/release/1.49/#g1-animated-templates)
- [v0.11](https://learn.gramener.com/guide/release/1.47/#g1)
- [v0.10.1](https://learn.gramener.com/guide/release/1.45/#g1)
- [v0.10.0](https://learn.gramener.com/guide/release/1.44/#g1)
- [v0.9.0](https://learn.gramener.com/guide/release/1.41/#g1)

## Browser support

Every release is tested on the current versions of Chrome, Edge and Firefox.
Internet Explorer is not explicitly tested, but many components work on IE.

## Contributing

- [Add an issue](https://code.gramener.com/cto/g1/issues)
- [Browse the source code](https://code.gramener.com/cto/g1)
- [Set up g1 for development locally](CONTRIBUTING.md#set-up)
- [Release g1 on npm](CONTRIBUTING.md#release)
