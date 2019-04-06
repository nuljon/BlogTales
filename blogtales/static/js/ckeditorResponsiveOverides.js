// For responsive autoembed iframes in CKEditor 4 while in edit view,
// use the following code to:
// Listen for editor input
// Identify oEmbed elements created by autoembed plugin (array of divs)
// for each oEmbed
// get child iframe (first child of div)
// Calculate aspect ratio from the iframe width and height attributes
// check width and height attributes were valid
// Apply style to parent div {vertical padding; width: 100 % ;height: 0}
// Delete iframe width and height attributes
// Set inline - style values {width: 100 %; height: 100%}

// Listen for editor input
CKEDITOR.on('instanceReady', function (event) {
    var editor = event.editor,
        element = editor.element;
    editor.on('change', function (){
        console.log(element);
        console.log(element.atributes);
        console.log(editor.getData());
        // identify oEmbed elements by autoembed plugin (div with child iframe).
        var my_oEmbeds = Array.prototype.slice.call(editor.querySelectorAll('iframe'));
        // iterate array
        for (var i = 0; i < my_oEmbeds.length; ++i) {

            var oE = my_oEmbeds[i];
            // get parent of iframe
            var parent = oE[0];
            // check if it is an embed widget

            // default padding
            var vp = '56%';
            // check for element dimensions are html attributes or css styles
            if (parent.attributes.height) {
                //calculate padding (height/width) from attributes
                vp = toString(parent.attributes.height / parent.attributes.width * 100) + "%";
                //remove width and height attributes from iframe
                delete oE.attributes.width;
                delete oE.attributes.height;
            }
            else {
                var style = parent.attributes.style;
                if (style) {
                    // Get the width from the style.
                    var match = /(?:^|\s)width\s*:\s*(\d+)px/i.exec(style);
                    var width = match && match[1];

                    // Get the height from the style.
                    match = /(?:^|\s)height\s*:\s*(?:(\d+)px|calc(?:100vw|(\.\d+))\s*\*\s*(?:100vw|(\.\d+))\));/i.exec(style);
                    var height = match && match[1];
                    //calculate padding (height/width) from styles
                    vp = toString(height / width * 100) + "%";
                }
                //set the responsive styles for the parent div tag
                oE.attributes.cssText = 'width:100%;height:0;padding-bottom:var(--' + vp + ', 56%)';
                //set the responsive styles for the iframe element
                oE.attributes.cssText = "position:absolute; top:0; left:0; width:100%; height:100%";
            }
        }
    });
});