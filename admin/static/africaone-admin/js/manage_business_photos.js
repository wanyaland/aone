
var africaOneManagePhotos = {
  businessID : 0,
  urls : {
    businessPhotosURL : '/manager/upload_business_photos/',
    deletePhotoURL : '/manager/delete_business_photo/',
    editCaptionURL : '/manager/edit_business_caption/',
    uploadBannerURL : '/manager/upload_banner_image/',
    deleteBannerURL : '/manager/delete_business_banner/',
    uploadLogoURL : '/manager/upload_business_logo/',
    deleteLogoURL : '/manager/delete_business_logo/'
  }
};

/**
 * initiate uploading business photos
 */
africaOneManagePhotos.initiateUploadingBusinessPhotos = function() {

  //make HTML element
  var $businessPhotosWrapper = $('.business-photos-list.business-photos-managed .x_content .isotope-list');
  var addNewPhoto = function (imgURL, photoID) {
    var html = '<div class="col-md-55 isotope-item">';
    html += '<div class="thumbnail"><div class="image view view-first" data-photo-type="BusinessPhoto" data-photo-id="' + photoID + '">';
    html += '<img src="' + imgURL + '">';
    html += '<div class="mask"><p>Edit</p><div class="tools tools-bottom"><a href="#" class="view-image"><i class="fa fa-link"></i></a><a href="#" class="edit-caption"><i class="fa fa-pencil"></i></a><a href="#" class="delete-image"><i class="fa fa-trash"></i></a></div></div></div>';
    html += '<div class="caption"><p></p></div>';
    html += '</div></div>';
    var $photoElem = $(html);
    $businessPhotosWrapper.prepend($photoElem).isotope('prepended', $photoElem);
    africaOneManagePhotos.activatePhotoElemFunctionality($photoElem);
  };

  //business images counter
  var businessImagesCounter = 1;

  //business photos uploader
  var businessPhotosUploader = new Dropzone('#upload-business-photos', {
    url : africaOneManagePhotos.urls.businessPhotosURL,
    addRemoveLinks : true,
    maxFilesize: 1, //in MB
    acceptedFiles: 'image/*',
    paramName: 'photos',
    uploadMultiple: false,
    headers: {
      'X-CSRFToken': africaone.getCookie('csrftoken')
    },
    accept: function(file, done) {
      if (businessImagesCounter++ < 5) {
        done();
      } else {
        done('Maximum 10 photos for each business.');
      }
    }
  });
  businessPhotosUploader.on("sending", function(file, xhr, formData) {
    formData.append("business_id", africaOneManagePhotos.businessID);
    formData.append("photo_type", 'BusinessPhoto');
  });
  businessPhotosUploader.on("complete", function(file) {
    if (file.status == "success") {
      businessPhotosUploader.removeFile(file);
      var responseObj = $.parseJSON(file.xhr.responseText);
      var imgURL = responseObj.business_photos[0];
      var photoID = responseObj.photo_ids[0];
      addNewPhoto(imgURL, photoID);
    } else {
    }
  });

};


/**
 * manage banner photo
 */
africaOneManagePhotos.manageBusinessSinglePhoto = function(type) {
  var $photoColWrapper = (type == 'banner') ? $('.banner-photo-col') : $('.logo-photo-col');
  var $uploaderDiv = $('.dropzone', $photoColWrapper);
  var $imgWrapper = $('.business-img-preview', $photoColWrapper);
  var photoType = (type == 'banner') ? 'BannerPhoto' : 'LogoPhoto';
  var uploaderID = (type == 'banner') ? '#upload-business-photos-banner' : '#upload-business-photos-logo';
  var uploadURL = (type == 'banner') ? africaOneManagePhotos.urls.uploadBannerURL : africaOneManagePhotos.urls.uploadLogoURL;
  var deleteURL = (type == 'banner') ? africaOneManagePhotos.urls.deleteBannerURL : africaOneManagePhotos.urls.deleteLogoURL;

  //uploader
  var photoUploader = new Dropzone(uploaderID, {
    url : uploadURL,
    addRemoveLinks : true,
    maxFilesize: 1, //in MB
    acceptedFiles: 'image/*',
    maxFiles: 1,
    paramName: 'image',
    uploadMultiple: false,
    headers: {
      'X-CSRFToken': africaone.getCookie('csrftoken')
    }
  });
  photoUploader.on("sending", function(file, xhr, formData) {
    formData.append("business_id", africaOneManagePhotos.businessID);
    formData.append("photo_type", photoType);
  });
  photoUploader.on("complete", function(file) {
    if (file.status == 'success') {
      photoUploader.removeFile(file);
      var response = $.parseJSON(file.xhr.responseText);
      var imgURL = response.img_url;
      $('img', $imgWrapper).attr('src', imgURL);
      $uploaderDiv.addClass('invisible');
      $photoColWrapper.addClass('with-img');
    }
  });

  //delete photo
  $('.delete-photo', $imgWrapper).click( function() {
    if (confirm('Are you sure you want to delete this photo?')) {
      var businessID = africaOneManagePhotos.businessID;
      $photoColWrapper.addClass('show-loading');
      $.post(
          deleteURL,
          {
            business_id: businessID
          },
          function (data) {
            if (data.success) {
              $uploaderDiv.removeClass('invisible');
              $photoColWrapper.removeClass('with-img');
              $photoColWrapper.removeClass('show-loading');
            }
          },
          'json'
      );
    }
    return false;
  });

  //view photo
  $('.view-photo', $imgWrapper).click( function() {
    var url = $('img', $imgWrapper).attr('src');
    window.open(url, '_blank');
  });

};


/**
 * photo element functionality
 */
africaOneManagePhotos.activatePhotoElemFunctionality = function($imageWrapper) {
  var $colWrapper = $imageWrapper.closest('.col-md-55');
  var $captionDiv = $('.caption', $colWrapper);
  var $isotopeWrapper = $colWrapper.closest('.isotope-list');
  var $thumbnailWrapper = $('.thumbnail', $colWrapper);

  //view image
  $('.view-image', $imageWrapper).click( function() {
    var url = $('img', $imageWrapper).attr('src');
    window.open(url, '_blank');
    return false;
  });

  //delete image
  $('.delete-image', $imageWrapper).click( function() {
    if (confirm('Are you sure you want to delete this photo?')) {
      var $imageElem = $('.image.view', $colWrapper);
      var photoID = $imageElem.data('photo-id');
      var photoType = $imageElem.data('photo-type');

      $thumbnailWrapper.addClass('show-loading');
      $.post(
          africaOneManagePhotos.urls.deletePhotoURL,
          {
            file_id: photoID,
            photoType: photoType
          },
          function (data) {
            if (data.success) {
              $isotopeWrapper.isotope('remove', $colWrapper).isotope('layout');
              $(window).trigger('debouncedresize');
            }
          },
          'json'
      );
    }
    return false;
  });

  //edit caption
  $('.edit-caption', $imageWrapper).click( function() {
    if ($('textarea', $captionDiv).length <= 0) {
      prepareCaptionTextarea();
    }
    return false;
  });

  //caption form
  var prepareCaptionTextarea = function() {
    var originalText = $captionDiv.text();
    $captionDiv.html('<textarea class="form-control">' + $.trim(originalText) + '</textarea><div class="error caption-form-info">Enter a caption to save</div><div class="hint caption-form-info">ESC - Cancel and ENTER - Save</div><div class="loading">Saving ...</div>');
    var $textarea = $('textarea', $captionDiv).focus();
    $(window).trigger('debouncedresize');

    //cancel or enter keys
    $textarea.keydown( function(event) {
      if (event.keyCode == 27) {
        $captionDiv.html('<p>' + originalText + '</p>');
        $(window).trigger('debouncedresize');
        return false;
      } else if (event.keyCode == 13) {
        if ($.trim($textarea.val()) == '') {
          $('.error', $captionDiv).show();
          $(window).trigger('debouncedresize');
        } else {
          $('.loading', $captionDiv).show();
          $('.error', $captionDiv).hide();
          $(window).trigger('debouncedresize');
          saveCaption();
        }
        return false;
      }
    });

    //autogrow textarea
    autosize($textarea);
    $textarea.on('autosize:resized', function() {
      $(window).trigger('debouncedresize');
    });
    autosize.update($textarea);

  };

  //save caption
  var saveCaption = function() {
    var $textarea = $('textarea', $captionDiv);
    var $imageElem = $('.image.view', $colWrapper);
    var photoID = $imageElem.data('photo-id');
    var photoType = $imageElem.data('photo-type');

    $thumbnailWrapper.addClass('show-loading');
    $.post(
        africaOneManagePhotos.urls.editCaptionURL,
        {
          file_id: photoID,
          photo_type: photoType,
          caption: $.trim($textarea.val())
        },
        function (data) {
          if (data.file_id) {
            $captionDiv.html('<p>' + data.caption + '</p>');
            $thumbnailWrapper.removeClass('show-loading');
            $(window).trigger('debouncedresize');
          }
        },
        'json'
    );
  };

};


/**
 * manage photos and captions
 */
africaOneManagePhotos.managePhotosAndCaptions = function () {
  $('.business-photos-list').each( function(index, elem) {
    var $photosList = $(elem);
    var $photosWrapper = $('.x_content', $photosList);
    africaone.initiateIsotope($photosWrapper);
    $('.image', $photosList).each( function(index, elem) {
      africaOneManagePhotos.activatePhotoElemFunctionality($(elem));
    });
  });
};


$(window).ready( function() {
  if ($('.business-photos-content').length <= 0) return;

  Dropzone.autoDiscover = false;

  africaOneManagePhotos.businessID = $('input#business-id').val();
  africaOneManagePhotos.initiateUploadingBusinessPhotos();
  africaOneManagePhotos.manageBusinessSinglePhoto('banner');
  africaOneManagePhotos.manageBusinessSinglePhoto('logo');
  africaOneManagePhotos.managePhotosAndCaptions();

});