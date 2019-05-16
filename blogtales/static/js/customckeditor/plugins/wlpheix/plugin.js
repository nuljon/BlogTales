/*
 * WlPheix plugin. Version Version: 1.0.4
 * Wlpheix - simple Gallery browser in CKEditor 4, used by different modules of CMS Pheix.
 * It adds Gallery button, that provides access to internal galleries.
 * Official repository: https://gitlab.com/pheix-ckeditor-plugins/wlpheix
 * Distributed under MIT license. Please check out: https://opensource.org/licenses/MIT
 * Have a question?! Please visit: https://pheix.org.
 */

CKEDITOR.plugins.add( 'wlpheix', {
    icons: 'wlpheix',
    init: function( editor ) {
        editor.addCommand( 'wlpheix', new CKEDITOR.dialogCommand( 'wlpheixDialog' ) );
        editor.ui.addButton( 'Wlpheix', {
            label: 'Вставить изображение из системной галереи Pheix',
            command: 'wlpheix',
            toolbar: 'insert'
        });
        CKEDITOR.dialog.add( 'wlpheixDialog', CKEDITOR.plugins.getPath('wlpheix') + 'dialogs/wlpheix-dialog.js' );
        editor.on( 'afterCommandExec', function(event) {
            var commandName = event.data.name;
            if (commandName == 'wlpheix') {
                console.log( "CKEditor: wlpheixDialog init done, path: "+ CKEDITOR.plugins.getPath('wlpheix') );
            }
        });
        console.log( "CKEditor: wlpheix init done, path: " + this.path + ' / ' + CKEDITOR.plugins.getPath('wlpheix') );
    }
});
