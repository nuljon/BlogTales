


(function () {

    // Object to hold widgets because there could be multiple instances/editors on the same page.
    var niftyWidgets = {};

    var currentEditorID = '';

    // Default Config
    var defaultConfig = {
        widgetKey: '00000000-0000-0000-0000-000000000000',
        userID: 'CKEditor User',
        imageName: 'CKEditor Image Name',
        theme: 'light',
        appendTo: '',
        fields: null,
        title: 'Personalized Image',
        onError: function (errorObj) {

            alert(errorObj.message);

            // Get the current widget instance and close it
            var currentWidget = niftyWidgets[currentEditorID];
            if (currentWidget != null && typeof currentWidget != 'undefined') {
                currentWidget.close();
            }

        }
    };

    // Check to see if the NiftyImage script has already been loaded from another plugin
    function loadNiftyScript(callback) {

        // Does the NiftyImages object exist?
        if (typeof NiftyImages != 'undefined') {
            callback();
            return;
        }

        CKEDITOR.scriptLoader.load('https://widget.niftyimages.com/js/niftywidget.js', function (success) {
            callback();
        });

    }

    CKEDITOR.plugins.add('niftyimages', {
        icons: 'niftyimages',
        init: function (editor) {

            editor.addCommand('personalizeImage', {
                exec: function (editor) {

                    // Note the editor that is being used for the widget
                    currentEditorID = editor.id;

                    // Get the selected element
                    var selection = editor.getSelection();

                    // Make sure it's an element
                    if (selection.getType() !== CKEDITOR.SELECTION_ELEMENT) {
                        return;
                    }

                    // Ensure that the element is not null and it's not an anchor image
                    var selectedElement = selection.getSelectedElement();
                    if (selectedElement == 'null' || selectedElement.hasClass('cke_anchor')) {
                        return;
                    }

                    // This is the dom img that is being updated
                    var img = selectedElement.$;

                    // Get the Widget associated with this plugin
                    var widget = niftyWidgets[currentEditorID];

                    if (typeof widget == 'undefined') {

                        // Make sure the widget script is loaded
                        loadNiftyScript(function () {

                            // Apply config defaults
                            var niftyConfig = CKEDITOR.tools.extend(defaultConfig, editor.config.niftyPlugin || {}, true);

                            // Instantiate the widget
                            niftyWidgets[currentEditorID] = new NiftyImages.NiftyWidget({
                                widgetKey: niftyConfig.widgetKey,
                                userID: niftyConfig.userID,
                                imageName: niftyConfig.imageName,
                                appendTo: niftyConfig.appendTo,
                                theme: niftyConfig.theme,
                                fields: niftyConfig.fields,
                                title: niftyConfig.title,
                                onLoad: function () {
                                    // Now that it's loaded, execute it again
                                    editor.execCommand('personalizeImage');
                                },
                                onSave: function (newURL) {

                                    // Make sure the Widget Key was updated
                                    if (niftyConfig.widgetKey == '00000000-0000-0000-0000-000000000000') {
                                        alert('The image was not created.\nYou must set the editor.config.niftyPlugin.widgetKey value. \n\nMore Information At: https://widget.niftyimages.com/Plugins/CKEditor');
                                        niftyWidgets[currentEditorID].close();
                                        return;
                                    }

                                    // Update the image with the new URL
                                    selectedElement.$.src = newURL;
                                    selectedElement.data('cke-saved-src', newURL);
                                    selectedElement.$.attributes['data-cke-saved-src'] = newURL;

                                },
                                onError: niftyConfig.onError
                            });

                        });

                        return;

                    }

                    // Start personalizing
                    widget.personalize(img.src);

                },
                refresh: function (editor, path) {

                    // Make sure selected item is an element
                    if (editor.getSelection().getType() !== CKEDITOR.SELECTION_ELEMENT) {
                        this.setState(CKEDITOR.TRISTATE_DISABLED);
                        return;
                    }

                    var element = path.lastElement && path.lastElement.getAscendant('img', true);

                    if (element && element.getName() == 'img') {
                        this.setState(CKEDITOR.TRISTATE_OFF);
                    } else {
                        this.setState(CKEDITOR.TRISTATE_DISABLED);
                    }

                },

                // Starts disabled so we can toggle when an image is selected
                startDisabled: true,

                // Context sensitive, so the refresh is triggered
                contextSensitive: 1,

                // Only available in WYSIWYG mode
                modes: { wysiwyg: 1 },

                // This command is async because NiftyImage servers need to be contacted via AJAX to create the personalized
                // and return the new image source
                async: true
            });

            // Add button to the toolbar
            editor.ui.addButton('NiftyImages', {
                label: 'Personalize Image',
                command: 'personalizeImage'
            });

            // Add context menu group for personalizing images
            if (editor.contextMenu) {

                // Create group
                editor.addMenuGroup('niftyGroup');

                // Add the item to the context menu
                editor.addMenuItem('personalizeItem', {
                    label: 'Personalize Image',
                    icon: this.path + 'icons/niftyimages.png',
                    command: 'personalizeImage',
                    group: 'niftyGroup'
                });

                // Only show if there is an image selected
                editor.contextMenu.addListener(function (element) {
                    if (element.getAscendant('img', true)) {
                        return { personalizeItem: CKEDITOR.TRISTATE_OFF };
                    }
                });

            }

        }
    });

})();
