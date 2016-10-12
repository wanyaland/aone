
var africaOneManageCategories = {
  $wrapper : {},
  $row : {},
  superCategories : new Array(),
  $superCategoryTemplate : {},
  $categoryTemplate : {},
  chooseIcon : {
    activeID : 0,
    $chooseIconDialog : {},
    defaultIcon : 'fa-question-circle'
  },
  urls : {
    listAll : '/manager/get_all_categories/',
    updateCategory : '/manager/edit_sub_category/',
    updateSuperCategory : '/manager/update_parent_category/',
    createCategory : '/manager/create_sub_category/',
    createSuperCategory : '/manager/create_parent_category/',
    deleteCategory : '/manager/delete_sub_category/',
    deleteSuperCategory : '/manager/delete_parent_category/'
  }
};


/**
 * add a category
 */
africaOneManageCategories.SuperCategory = function (superCategoryData) {
  this.id = superCategoryData.id;
  this.name = superCategoryData.name;
  this.categories = new Array();
  this.icon = africaOneManageCategories.chooseIcon.defaultIcon;

  if (superCategoryData.icon)
    this.icon = superCategoryData.icon;

  this.$superCategoryDiv = africaOneManageCategories.$superCategoryTemplate.clone();
  this.$titleDiv = $('.x_title', this.$superCategoryDiv);

  this.$superCategoryDiv.attr('id', 'super-category-' + this.id);

  $('.info-wrapper h2', this.$titleDiv).text(this.name);
  $('.info-wrapper .super-category-icon i.fa', this.$titleDiv).attr('class', 'fa ' + this.icon);

  //initiate
  this.edit();
  this.iconChooser();
  this.delete();
  this.createCategory();
  if (superCategoryData.categories && superCategoryData.categories.length) {
    this.makeCategories(superCategoryData.categories);
  }

  //mark category list with Super Category ID
  $('ul.categories-list', this.$superCategoryDiv).data('super-category-id', this.id);

  //check if new super category creator exists
  var $newSuperCategoryDiv = $('#new-super-category-creator', africaOneManageCategories.$row);
  if ($newSuperCategoryDiv.length > 0) {
    this.$superCategoryDiv.insertBefore($newSuperCategoryDiv);
    africaOneManageCategories.relayout(this.$superCategoryDiv);
  } else {
    this.$superCategoryDiv.appendTo(africaOneManageCategories.$row);
  }

  africaOneManageCategories.superCategories.push(this);

};

//choose icon
africaOneManageCategories.SuperCategory.prototype.iconChooser = function () {
  var thisRef = this;
  var $formIcon = $('.form-wrapper .super-category-icon', this.$titleDiv);
  var $displayIcon = $('.info-wrapper .super-category-icon', this.$titleDiv);
  $displayIcon.click( function() {
    $formIcon.click();
  });
  $formIcon.click( function () {
    thisRef.showForm();
    africaOneManageCategories.chooseIcon.activeID = thisRef.id;
    africaOneManageCategories.chooseIcon.$chooseIconDialog.modal();
  });
  africaOneManageCategories.chooseIcon.$chooseIconDialog.on('africaOneManageCategories:iconChosen', function(e, eventData) {
    if (africaOneManageCategories.chooseIcon.activeID == thisRef.id) {
      thisRef.icon = eventData.iconClass;
      $('i.fa', $formIcon).attr('class', 'fa ' + thisRef.icon);
      $('input[name="icon"]', thisRef.$titleDiv).val(thisRef.icon);
      africaOneManageCategories.chooseIcon.activeID = 0;
    }
  });
};

//delete super category
africaOneManageCategories.SuperCategory.prototype.delete = function () {
  var thisRef = this;
  var $deleteBtn = $('.delete', thisRef.$titleDiv);
  $deleteBtn.click( function() {
    if (thisRef.categories.length > 0) {
      alert('You cannot delete this Super Category because it contains child categories. Please first move or delete all child categories.');
      return false;
    }
    if (confirm('Are you sure you want to delete this Super Category: ' + thisRef.name + '?')) {
      thisRef.$titleDiv.addClass('saving');
      $.getJSON(africaOneManageCategories.urls.deleteSuperCategory, {id: thisRef.id})
          .done(function (jsonResponse) {
            if (jsonResponse.success) {
              $.each(africaOneManageCategories.superCategories, function (index, superCategory) {
                if (superCategory && superCategory.id == thisRef.id) {
                  africaOneManageCategories.superCategories.splice(index, 1);
                }
              });
              africaOneManageCategories.$row.isotope('remove', thisRef.$superCategoryDiv).isotope('layout');
              thisRef = null;
              delete thisRef;
            } else {
            }
          });
    }
    return false;
  });
};

//show form
africaOneManageCategories.SuperCategory.prototype.showForm = function () {
  var $form = $('form', this.$titleDiv);
  $('.form-text', $form).val(this.name);
  if (this.icon == africaOneManageCategories.chooseIcon.defaultIcon) {
    $('input[name="icon"]', $form).val('');
  } else {
    $('input[name="icon"]', $form).val(this.icon);
  }
  $('input[name="id"]', $form).val(this.id);
  $('.super-category-icon i.fa', $form).attr('class', 'fa ' + this.icon);
  $form.removeClass('saving');
  this.$titleDiv.addClass('edit-mode');
  $('.form-text', $form).focus();
};

//edit super category
africaOneManageCategories.SuperCategory.prototype.edit = function () {
  var thisRef = this;
  var $infoWrapper = $('.info-wrapper', this.$titleDiv);
  var $formWrapper = $('.form-wrapper', this.$titleDiv);
  var $form = $('form', $formWrapper);

  //check form
  var checkForm = function() {
    var newVal = $.trim($('.form-text', $form).val()).toUpperCase();

    if (!newVal) {
      alert('Please enter a valid name for this super category');
      return false;
    }

    //check other names
    var namePresent = false;
    $.each(africaOneManageCategories.superCategories, function(index, superCategory) {
      if (newVal == $.trim(superCategory.name).toUpperCase() && superCategory.id != thisRef.id) {
        namePresent = true;
        return false;
      }
    });
    if (namePresent) {
      alert('This name: ' + newVal + ' already exists. Please enter another name for this super category.');
      return false;
    }

    thisRef.$titleDiv.addClass('saving');
    return true;
  };

  //form successfully saved
  var formSuccess = function(jsonResponseData) {
    thisRef.name = jsonResponseData.name;
    thisRef.icon = jsonResponseData.icon;
    $('.super-category-icon i.fa', $infoWrapper).attr('class', 'fa ' + thisRef.icon);
    $('h2', $infoWrapper).text(thisRef.name);
    thisRef.$titleDiv.removeClass('edit-mode').removeClass('saving');;
  };

  //change action URL
  $form.ajaxForm({
    url : africaOneManageCategories.urls.updateSuperCategory,
    type : 'post',
    dataType : 'json',
    beforeSubmit : checkForm,
    success : formSuccess
  });

  //edit button
  $('.edit', $infoWrapper).click( function () {
    thisRef.showForm();
    return false;
  });

  //cancel button
  $('.btn-danger', $formWrapper).click( function () {
    thisRef.$titleDiv.removeClass('edit-mode');
    return false;
  })
};

//create new category
africaOneManageCategories.SuperCategory.prototype.createCategory = function () {
  var $createCategoryDiv = $('.new-category', this.$superCategoryDiv);
  var $form = $('form', $createCategoryDiv);
  var thisRef = this;
  $('input[name="super-category-id"]', $form).val(this.id);

  //on form active
  $form.click( function() {
    $createCategoryDiv.addClass('edit-mode');
  });
  $('.form-text', $createCategoryDiv).focus( function() {
    $createCategoryDiv.addClass('edit-mode');
  });

  //reset form
  var resetForm = function() {
    //$createCategoryDiv.removeClass('edit-mode');
    $createCategoryDiv.removeClass('saving');
    $('.form-text', $form).val('').focus();
  };

  //check form
  var checkForm = function() {
    var newVal = $.trim($('.form-text', $form).val()).toUpperCase();
    if (!newVal) {
      alert('Please enter a valid name for this category');
      return false;
    }

    //check other names
    var namePresent = false;
    $.each(africaOneManageCategories.superCategories, function(index, superCategory) {
      $.each(superCategory.categories, function(index, category) {
        if (newVal == $.trim(category.name).toUpperCase()) {
          namePresent = true;
          return false;
        }
      });
      return !namePresent;
    });
    if (namePresent) {
      alert('This name: ' + newVal + ' already exists. Please enter another name for this category.');
      return false;
    }

    $createCategoryDiv.addClass('saving');
    return true;
  };

  //form successfully saved
  var formSuccess = function(jsonResponseData) {
    var category = new africaOneManageCategories.Category(jsonResponseData, thisRef);
    $('.categories-list', thisRef.$superCategoryDiv).append(category.$categoryDiv);
    thisRef.categories.push(category);
    resetForm();
    africaOneManageCategories.relayout();
  };

  //change action URL
  $form.ajaxForm({
    url : africaOneManageCategories.urls.createCategory,
    type : 'post',
    dataType : 'json',
    beforeSubmit : checkForm,
    success : formSuccess
  });

  //cancel button
  $('.btn-danger', $form).click( function () {
    resetForm();
    return false;
  })
};

//attach categories
africaOneManageCategories.SuperCategory.prototype.makeCategories = function (categories) {
  var thisRef = this;
  var $categoriesWrapper = $('.categories-list', this.$superCategoryDiv);

  $.each(categories, function (index, categoryData) {
    var category = new africaOneManageCategories.Category(categoryData, thisRef);
    $categoriesWrapper.append(category.$categoryDiv);
    thisRef.categories.push(category);
  });
};

//class for a category
africaOneManageCategories.Category = function (categoryData, superCategory) {
  this.name = categoryData.name;
  this.id = categoryData.id;
  this.superCategory = superCategory;
  this.$categoryDiv = africaOneManageCategories.$categoryTemplate.clone();
  this.updateValues();
  this.delete();
  this.edit();
  this.dragDrop();
};

//update div
africaOneManageCategories.Category.prototype.updateValues = function () {
  $('.info-wrapper .name', this.$categoryDiv).text(this.name);
  $('.form-wrapper input[name="id"]', this.$categoryDiv).val(this.id);
  $('.form-wrapper input[name="super-category-id"]', this.$categoryDiv).val(this.superCategory.id);
  $('.form-wrapper input[name="name"]', this.$categoryDiv).val(this.name);
};

//delete category
africaOneManageCategories.Category.prototype.delete = function () {
  var thisRef = this;
  var $deleteBtn = $('.delete', thisRef.$categoryDiv);
  $deleteBtn.click( function() {
    if (confirm('Are you sure you want to delete this Category: ' + thisRef.name + '?')) {
      thisRef.$categoryDiv.addClass('saving');
      $.getJSON(africaOneManageCategories.urls.deleteCategory, {id: thisRef.id})
          .done(function (jsonResponse) {
            if (jsonResponse.success) {
              $.each(thisRef.superCategory.categories, function (index, category) {
                if (category.id == thisRef.id) {
                  thisRef.superCategory.categories.splice(index, 1);
                }
              });
              thisRef.$categoryDiv.remove();
              africaOneManageCategories.relayout();
              thisRef = null;
              delete thisRef;
            } else {
            }
          });
    }
    return false;
  });
};

//edit category
africaOneManageCategories.Category.prototype.edit = function () {
  var thisRef = this;
  var $infoWrapper = $('.info-wrapper', this.$categoryDiv);
  var $formWrapper = $('.form-wrapper', this.$categoryDiv);
  var $form = $('form', $formWrapper);

  //check form
  var checkForm = function() {
    var newVal = $.trim($('.form-text', $form).val()).toUpperCase();
    if (!newVal) {
      alert('Please enter a valid name for this category');
      return false;
    }

    //check other names
    var namePresent = false;
    $.each(africaOneManageCategories.superCategories, function(index, superCategory) {
      $.each(superCategory.categories, function(index, category) {
        if (newVal == $.trim(category.name).toUpperCase() && category.id != thisRef.id) {
          namePresent = true;
          return false;
        }
      });
      return !namePresent;
    });
    if (namePresent) {
      alert('This name: ' + newVal + ' already exists. Please enter another name for this category.');
      return false;
    }

    thisRef.$categoryDiv.addClass('saving');
    return true;
  };

  //form successfully saved
  //form only changes name
  var formSuccess = function(jsonResponseData) {
    thisRef.name = jsonResponseData.name;
    thisRef.updateValues();
    thisRef.$categoryDiv.removeClass('edit-mode').removeClass('saving');;
  };

  //change action URL
  $form.ajaxForm({
    url : africaOneManageCategories.urls.updateCategory,
    type : 'post',
    dataType : 'json',
    beforeSubmit : checkForm,
    success : formSuccess
  });

  //edit button
  $('.edit', this.$categoryDiv).click( function () {
    thisRef.updateValues();
    thisRef.$categoryDiv.addClass('edit-mode');
    $('.form-text', $form).focus();
    return false;
  });

  //cancel button
  $('.btn-danger', this.$categoryDiv).click( function () {
    thisRef.$categoryDiv.removeClass('edit-mode');
    return false;
  })
};

//update super category on drag-drop
africaOneManageCategories.Category.prototype.dragDrop = function () {
  var thisRef = this;

  var resetCategoryDiv = function () {
    var $oldCategoriesList = $('ul.categories-list', thisRef.superCategory.$superCategoryDiv);
    thisRef.$categoryDiv.remove().appendTo($oldCategoriesList);
    alert('Failed to update Super Category for this child category');
  };

  this.$categoryDiv.on('africaOneManageCategories:DroppedCategory', function() {
    var newSuperCategoryID = thisRef.$categoryDiv.closest('ul.categories-list').data('super-category-id');
    var currentSuperCategoryID = thisRef.superCategory.id;

    if (newSuperCategoryID != currentSuperCategoryID) {
      var newSuperCategory, currentSuperCategory;
      $.each(africaOneManageCategories.superCategories, function(index, superCategoryObj) {
        if (newSuperCategoryID == superCategoryObj.id) {
          newSuperCategory = superCategoryObj;
        }
        if (currentSuperCategoryID == superCategoryObj.id) {
          currentSuperCategory = superCategoryObj;
        }
      });

      if (newSuperCategory && currentSuperCategory) {
        thisRef.$categoryDiv.addClass('saving');
        $.post(
            africaOneManageCategories.urls.updateCategory,
            {
              name : thisRef.name,
              id : thisRef.id,
              'super-category-id' : newSuperCategory.id
            },
            function (jsonResponse) {
              if (jsonResponse.id) {

                thisRef.superCategory = newSuperCategory;
                thisRef.updateValues();

                //update arrays
                newSuperCategory.categories.push(thisRef);
                $.each(currentSuperCategory.categories, function (index, category) {
                  if (category && category.id == thisRef.id) {
                    currentSuperCategory.categories.splice(index, 1);
                  }
                });

                thisRef.$categoryDiv.removeClass('saving');
              } else {
                resetCategoryDiv();
              }
            },
            "json"
        ).fail( function() {
          resetCategoryDiv();
        });

      }

    }

  });
};



/**
 * create new super category
 */
africaOneManageCategories.initiateCreateNewSuperCategory = function() {
  var $createSuperCategoryDiv = africaOneManageCategories.$superCategoryTemplate.clone().addClass('new-super-category-creator').attr('id', 'new-super-category-creator');
  var $titleDiv = $('.x_title', $createSuperCategoryDiv);
  var $form = $('form', $titleDiv);

  //prepare display
  $('.x_content', $createSuperCategoryDiv).remove();
  $('.info-wrapper', $titleDiv).remove();
  $titleDiv.addClass('edit-mode');
  $('.form-text', $form).attr('placeholder', 'Add a new super category ...');

  //on form active
  $form.click( function() {
    $createSuperCategoryDiv.addClass('edit-mode-active');
  });
  $('.form-text', $createSuperCategoryDiv).focus( function() {
    $createSuperCategoryDiv.addClass('edit-mode-active');
  });

  //icon chooser
  var $formIcon = $('.form-wrapper .super-category-icon', $titleDiv);
  $formIcon.click( function () {
    africaOneManageCategories.chooseIcon.activeID = 'new';
    africaOneManageCategories.chooseIcon.$chooseIconDialog.modal();
  });
  africaOneManageCategories.chooseIcon.$chooseIconDialog.on('africaOneManageCategories:iconChosen', function(e, eventData) {
    if (africaOneManageCategories.chooseIcon.activeID == 'new') {
      var iconClass = eventData.iconClass;
      $('i.fa', $formIcon).attr('class', 'fa ' + iconClass);
      $('input[name="icon"]', $form).val(iconClass);
      africaOneManageCategories.chooseIcon.activeID = 0;
    }
  });

  //reset form
  var resetForm = function() {
    $('.form-text', $form).val('');
    $('input[name="icon"]', $form).val('');
    $('.super-category-icon i.fa', $form).attr('class', 'fa ' + africaOneManageCategories.chooseIcon.defaultIcon);
    $createSuperCategoryDiv.removeClass('edit-mode-active');
    $titleDiv.removeClass('saving');
  };

  //check form
  var checkForm = function() {
    var newVal = $.trim($('.form-text', $form).val()).toUpperCase();
    if (!newVal) {
      alert('Please enter a valid name for this super category');
      return false;
    }

    //check other names
    var namePresent = false;
    $.each(africaOneManageCategories.superCategories, function(index, superCategory) {
      if (newVal == $.trim(superCategory.name).toUpperCase()) {
        namePresent = true;
        return false;
      }
    });
    if (namePresent) {
      alert('This name: ' + newVal + ' already exists. Please enter another name for this super category.');
      return false;
    }

    $titleDiv.addClass('saving');
    return true;
  };

  //form successfully saved
  var formSuccess = function(jsonResponseData) {
    new africaOneManageCategories.SuperCategory(jsonResponseData);
    resetForm();
  };

  //change action URL
  $form.ajaxForm({
    url : africaOneManageCategories.urls.createSuperCategory,
    type : 'post',
    dataType : 'json',
    beforeSubmit : checkForm,
    success : formSuccess
  });

  //cancel button
  $('.btn-danger', $form).click( function () {
    resetForm();
    return false;
  })

  //insert into DOM
  $createSuperCategoryDiv.appendTo(africaOneManageCategories.$row).css({
    position : 'absolute',
    left : 'auto',
    top : '0',
    right: '0'
  });
  africaOneManageCategories.$row.isotope( 'stamp', $createSuperCategoryDiv );

};


/**
 * drag and drop categories
 */
africaOneManageCategories.initiateDragDrop = function() {
  var $categoriesLists = $("ul.categories-list", africaOneManageCategories.$row);
  $categoriesLists.sortable({
    group: 'categories-list',
    pullPlaceholder: false,
    tolerance: 10,
    isValidTarget: function  ($item, container) {
      return !container.el.hasClass('original-container');
    },
    onDrop: function  ($item, container, _super) {
      $categoriesLists.removeClass('original-container');
      _super($item, container);
      $('#new-super-category-creator', africaOneManageCategories.$row).show();
      africaone.setUpIsotope(africaOneManageCategories.$row);
      africaOneManageCategories.relayout();
      $item.trigger('africaOneManageCategories:DroppedCategory');
    },
    onDragStart: function ($item, container, _super) {
      $('#new-super-category-creator', africaOneManageCategories.$row).hide();
      container.el.addClass('original-container');
      africaOneManageCategories.$row.isotope('destroy');
      _super($item, container);
    }
  });


};


/**
 * choose an icon
 */
africaOneManageCategories.initiateIconChooser = function() {
  var $chooseIconDialog = $('#choose-icon-dialog');
  $('.fa-hover', $chooseIconDialog).click( function () {
    var $fa = $('.fa', $(this));
    var iconClass = $.trim($fa.attr('class').replace('fa ', ''));
    $chooseIconDialog.trigger('africaOneManageCategories:iconChosen', { iconClass : iconClass });
    $chooseIconDialog.modal('hide');
  });
  africaOneManageCategories.chooseIcon.$chooseIconDialog = $chooseIconDialog;
};


/**
 * relayout super categories
 */
africaOneManageCategories.relayout = function($newElements) {
  if (africaOneManageCategories.$row.data('isotope-data')) {

    //fix creator
    var $superCategoryCreator = $('#new-super-category-creator', africaOneManageCategories.$row).css({
      position : 'absolute',
      left : 'auto',
      top : '0',
      right: '0'
    });
    africaOneManageCategories.$row.isotope( 'stamp', $superCategoryCreator );

    if ($newElements && $newElements.length > 0) {
      africaOneManageCategories.$row.isotope('insert', $newElements);
    }
    africaOneManageCategories.$row.isotope('layout');

  }
};


$(window).ready( function() {
  africaOneManageCategories.$superCategoryTemplate = $('#placeholder-super-category').remove();

  if (africaOneManageCategories.$superCategoryTemplate.length <= 0) return;

  africaOneManageCategories.$superCategoryTemplate.removeClass('hidden');
  africaOneManageCategories.$categoryTemplate = $('.categories-list .category-item', africaOneManageCategories.$superCategoryTemplate).remove();
  africaOneManageCategories.$wrapper = $('.manage-categories-wrapper .categories-row-wrapper');

  africaOneManageCategories.initiateIconChooser();

  africaOneManageCategories.$row = $('.categories-row', africaOneManageCategories.wrapper);

  $.getJSON(africaOneManageCategories.urls.listAll)
      .done(function (superCategories) {
        $.each(superCategories, function (index, superCategoryData) {
          new africaOneManageCategories.SuperCategory(superCategoryData);
        });

        //layout
        africaone.initiateIsotope(africaOneManageCategories.$wrapper);

        //add super category creator
        africaOneManageCategories.initiateCreateNewSuperCategory();
        africaOneManageCategories.relayout();

        //initiate drag and drop
        africaOneManageCategories.initiateDragDrop();

      });

});
