/**
* responsive loader plugin
*   a dedicated loader type for django-ckeditor-responsive
* 	- a loader type to facilitate HTML5 image size and source-set attribute creation 
*	- extends CKEDITOR.fileTools.fileLoader
*   - designed as an alternative to ckeditor cloudservice for Easy Image Upload */

( function() {
	'use strict';

	CKEDITOR.plugins.add( 'responsiveloader', {
		requires: 'filetools,ajax',
		onLoad: function() {
			var FileLoader = CKEDITOR.fileTools.fileLoader;

			/**
			 * Note that this type is defined in the {@link CKEDITOR.pluginDefinition#onLoad plugin.onLoad} method, thus is
			 * guaranteed to be available in dependent plugin's {@link CKEDITOR.pluginDefinition#beforeInit beforeInit},
			 * {@link CKEDITOR.pluginDefinition#init init} and {@link CKEDITOR.pluginDefinition#afterInit afterinit} methods.
			 *
			 * @since 4.11
			 * @class CKEDITOR.plugins.responsiveloader
			 * @extends CKEDITOR.fileTools.fileLoader
			 * @constructor
			 * @inheritdoc
			 * @param {CKEDITOR.editor} editor The editor instance. Used only to get the language data.
			 * @param {Blob/String} fileOrData A [blob object](https://developer.mozilla.org/en/docs/Web/API/Blob) or a data
			 * string encoded with Base64.
			 * @param {String} [fileName] The file name. If not set and the second parameter is a file, then its name will be used.
			 * If not set and the second parameter is a Base64 data string, then the file name will be created based on
			 * the {@link CKEDITOR.config#fileTools_defaultFileName} option.
			 */
			function ResponsiveLoader( editor, fileOrData, fileName ) {
				FileLoader.call(this, editor, fileOrData, fileName);
				// can add parameters and functionaluty here for cloudinary,  etc.
			}

			ResponsiveLoader.prototype = CKEDITOR.tools.extend( {}, FileLoader.prototype );

			/**
			 * @param {	String } [url] The upload URL. 
			 * If not provided in config.responsiveLoader_uploadUrl and settings.CKEDITOR_UPLOAD_PATH,
			 * "uploads/" will be used.
			 * @param {Object} [additionalRequestParameters]
			 * Additional data that would be passed to the
			 * {@link CKEDITOR.editor#fileUploadRequest} event.
			 */
			ResponsiveLoader.prototype.upload = function( url="/upload/", additionalRequestParameters ) {
				url = url || this.editor.config;

				if ( !url ) {
					CKEDITOR.error( 'ResponsiveLoader-no-upload-url' );
					return;
				}

				FileLoader.prototype.upload.call( this, url, additionalRequestParameters );
			};


			CKEDITOR.plugins.responsiveloader.responsiveLoader = ResponsiveLoader;
		},

		beforeInit: function (editor) {
			;
			//this is where additional code should gor for cloudinary, etc.
			

		     // overide FileLoader to process  JSON response 
			editor.on( 'fileUploadResponse', function( evt ) {
				var fileLoader = evt.data.fileLoader,
					xhr = fileLoader.xhr,
					response;
				
				// this is the importnat part
				if ( fileLoader instanceof CKEDITOR.plugins.responsiveloader.responsiveLoader ) {
					evt.stop();

					try {
						response = JSON.parse( xhr.responseText );

						evt.data.response = response;
					} catch ( e ) {
						CKEDITOR.warn( 'filetools-response-error', { responseText: xhr.responseText } );
					}
				}
			} );
		}
	} );

	CKEDITOR.plugins.responsiveloader = {
		// Note this type is loaded on runtime.
		responsiveLoader: null
	};

} )();
