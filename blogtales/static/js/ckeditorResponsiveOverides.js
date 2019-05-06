// For responsive autoembed iframes in CKEditor 4 while in edit view,
// use the following code to:
// start script once the editor has loaded
// Listen for editor input
// get the editor content
// split string into an array
// for each array element
// identify oembed url element
//
// get child iframe(first child of div)
// Calculate aspect ratio from the iframe width and height attributes
// check width and height attributes were valid
// Apply style to parent div {vertical padding; width: 100 % ;height: 0}
// Delete iframe width and height attributes
// Set inline - style values {width: 100 %; height: 100%}

// listen for the editor instance ready event
// initialize a flag for tracking conversions
var done = false;

// function to convert oembed data to responsive
var responsive_oembed = function oembedResponsive(oe_string) {
    // initialize oembed location start
    let oembed_location = null;
    oembed_location = oe_string.indexOf("data-oembed-url");
    // buffer the oembed data
    let buffer = oe_string.slice(oembed_location, oe_string.length - 1);
    // trim buffer not part of oembed content
    buffer = buffer.slice(0, buffer.indexOf("</iframe>") + 9);
    // debug output
    console.log(buffer);
    // get start position of the remainder of editor data
    let remainder = oembed_location + buffer.length;
    // get locations for height and width attributes
    let heightLocation = buffer.indexOf("height=");
    let widthLocation = buffer.indexOf("width=");
    // get values of height and width
    let height = parseInt(buffer.slice(heightLocation + 8, heightLocation + 9 + 4), 10);
    let width = parseInt(buffer.slice(widthLocation + 7, widthLocation + 8 + 4), 10);
    // calculate vertcal padding
    let vp = parseInt(height / width * 100, 10) + "%";
    // the responsive styles for the parent oembed element
    let oembed_cssText = ('style="position:relative; width:100%; height:0;padding-bottom:' + vp + ';" ');
    // insert the oembed styles
    buffer = insert_string(buffer, oembed_cssText, 0);
    // the responsive styles for the iframe tag
    let iframe_cssText = (' style="position:absolute; left:0; top:0; width:100%; height:100%"');
    // find insertion point for iframe styles
    let result = buffer.match(/><\/iframe>/i);
    // insert the iframe styles
    buffer = insert_string(result.input, iframe_cssText, result.index);
    // delete the iframe height and width attributes
    let regex = /width\s*=\s*"\s*\d+"/;
    buffer = buffer.replace(regex, '');
    regex = /height\s*=\s*"\s*\d+"/;
    buffer = buffer.replace(regex, '');
    // debug output
    console.log(buffer);
    // replace the old oe_string with the new
    oe_string = oe_string.slice(0, oembed_location) + buffer + oe_string.slice(remainder);
    // debug output
    console.log(oe_string);
    return oe_string;
};
// a function to insert a string inside a string
var insert_string = function insert(main_string, ins_string, pos) {
    if (typeof (pos) == "undefined") {
        pos = 0;
    }
    if (typeof (ins_string) == "undefined") {
        ins_string = '';
    }
    let str = main_string.slice(0, pos) + ins_string + main_string.slice(pos);
    console.log(str);
    return str;
};

CKEDITOR.on('instanceReady', function (event) {
    //assign vars to the editor object and the textarea element
    var editor = event.editor,
        element = editor.element;
    //initialize a var to capture data
    var data = "";

    // post a Listener for editor input
    editor.on('change', function () {
        // debug output
        console.log(element);
        // debug output
        console.log(element.attributes);
        // get the data
        data = editor.getData();
        // debug output
        console.log(data);
        // verify oembed in data and only once
        /*  if (oembed_location == data.lastIndexOf("data-oembed-url")) */
        // verify oembed tag is in the data
        if (data.includes("data-oembed-url") && !done) {
            let newData = responsive_oembed(data);
            editor.setData(newData, {
                callback: function () {
                    /* this.checkDirty(); */
                    this.updateElement();
                   /*  alert(document.getElementById('cke_1').value); */
                }, noSnapshot: true
            });
            $('#cke_1').html(newData);
            done = true;
            console.log('did we update?');
            data = editor.getData();
            console.log(data);
        }

    });

});

/* Update Editor

To update editor content:
    var editor = CKEDITOR.instances['TEXTAREA-ID'];
    var newHtml = '<p>Hello World!</p>";
    editor.setData(newHtml, {
        callback: function () {
            this.updateElement();
        }
    });
    $('textarea#TEXTAREA-ID').html(newHtml);

Here, we first retrieve editor and then update its content via setData() API. At last, the textarea itself is updated in the DOM
*/


// identify oEmbed elements by autoembed plugin (div with child iframe).
/* <div data-oembed-url="https://youtu.be/I4vjq46gCUQ"><iframe allowfullscreen="allowfullscreen" frameborder="0" height="270" src="https://www.youtube.com/embed/I4vjq46gCUQ?feature=oembed" tabindex="-1" width=" 480"></iframe></div> */


// var my_oEmbeds = Array.prototype.slice.call(editor.querySelectorAll('iframe'));
// iterate array
/*
        for (var i = 0; i < my_oEmbeds.length; ++i) {

            var oE = my_oEmbeds[i];
            // get parent of ifraA
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
*/