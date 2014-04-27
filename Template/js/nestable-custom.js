/*
*	 Author: Vijay Kumar
*	 Template: Archon - Flat & Responsive Bootstrap Admin Template
*	 Version: 1.0
*	 Bootstrap version: 3.0.0
*	 Copyright 2013 bootstrapguru
*	 www: http://bootstrapguru.com
*	 mail: support@bootstrapguru.com
*	 You can find our other themes on: https://bootstrapguru.com/themes/
---------------------------------------------------------------------------------------------- */


// jQuery $('document').ready(); function 
$('document').ready(function(){

$('.dd').nestable({ /* config options */ });

/* Buttons to  */
$('#nestable-menu').on('click', function(e)
   {
       var target = $(e.target),
           action = target.data('action');
       if (action === 'expand-all') {
           $('.dd').nestable('expandAll');
       }
       if (action === 'collapse-all') {
           $('.dd').nestable('collapseAll');
       }
   });


  // activate Nestable for list 2
    $('#nestable2').nestable({
        group: 1
    });

});