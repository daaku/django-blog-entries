YAHOO.util.Event.onDOMReady(function() {
    YAHOO.util.Dom.addClass(document.body, 'yui-skin-sam');
    var makeRich = function(id, height) {
        (new YAHOO.widget.Editor(id, {height: height, width: '700px', handleSubmit: true})).render();
        window.setTimeout(function() { YAHOO.util.Dom.setStyle(id + '_container', 'margin-left', '108px'); }, 200);
    };
    makeRich('id_excerpt', '200px');
    makeRich('id_body', '500px');
});
