// The following example will show a balloon toolbar on any selection change. The toolbar is anchored to the
// last element in the selection, assuming that the editor variable is an instance of CKEDITOR.editor.

editor.on('instanceReady', function () {
    var toolbar = new CKEDITOR.ui.balloonToolbar(editor);

    toolbar.addItems({
        copy: new CKEDITOR.ui.button({
            command: 'copy'
        }),
        cut: new CKEDITOR.ui.button({
            command: 'cut'
        }),
        paste: new CKEDITOR.ui.button({
            command: 'paste'
        }),
        link: new CKEDITOR.ui.button({
            command: 'link'
        }),
        unlink: new CKEDITOR.ui.button({
            command: 'unlink'
        }),
        bold: new CKEDITOR.ui.button({
            command: 'bold'
        }),
        italic: new CKEDITOR.ui.button({
            command: 'italic'
        }),
        superscript: new CKEDITOR.ui.button({
            command: 'superscript'
        }),
        underline: new CKEDITOR.ui.button({
            command: 'underline'
        }),
        strike: new CKEDITOR.ui.button({
            command: 'strike'
        }),
        removeformat: new CKEDITOR.ui.button({
            command: 'removeformat'
        })
    });

    editor.on('selectionChange', function (evt) {
        var lastElement = evt.data.path.lastElement;

        if (lastElement) {
            toolbar.attach(lastElement);
        }
    });
});