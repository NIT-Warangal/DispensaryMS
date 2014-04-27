// jQuery $('document').ready(); function 
$('document').ready(function(){

	 container = $('.mails');
	loadBlock('mails.html',container);

//	enable_options();

	// Inbox 
	$('.inbox-options a,.inbox-labels a').on('click',function(){
		$('.inbox-options a,.inbox-labels a').removeClass('active');
		$(this).addClass('active');
		var vj=$(this).html();
		$('h3.page-header').html(vj);
	});


	// Create Labells manually 
	$('#create-label').click(function(){
	var vj=$('#write-label').val();
		add_event(vj);
	});

	document.getElementById('write-label').onkeypress = function(e) 
	{
		var event = e || window.event;
		var charCode = event.which || event.keyCode;

		if ( charCode == '13' ) 
		{
			var vj=$('#write-label').val();
			add_event(vj);
		}
	}
	
	$('.btn-compose').on('click',function(e){
		e.preventDefault();
		loadBlock('compose.html',container);
	});
	$('.list-inbox').on('click',function(){
		var container=$('.mails');
		loadBlock('mails.html',container);
	});
});

function enable_options()
{
	$('.mail-right-box .mails table tr td i').on('click',function(){
		$(this).toggleClass('active');
	});

	$('.mail-right-box .mails table tr td i.fa-check-square-o').on('click',function(){
		$(this).toggleClass('fa-square-o');
		$(this).parent().parent().toggleClass('active');
	});

	$('.mail-list tr').on('click',function(){
		container = $('.mail-body');
		url = "mail-body.html"
			
			loadBlock(url,container);

	});

	$('.send-mail').on('click',function(){
		container.mask('<h3><i class="fa  fa-refresh fa-spin"></i> Message is being sent...</h3>');

		
      	setTimeout(function () {
		container.mask('<h3><i class="fa  fa-check"></i> Sent Successfully.</h3>');
        	},
      	1000);



	});

}

enable_options();

function add_event(vj)
{
	$('.inbox-labels').append('<a class="list-group-item"  href="#"><span class="pull-right"><i class="fa fa-tag"></i></span>'+vj+'</a>')
	$('#write-label').val('');
}

function loadBlock(url, container) {
	$(container).mCustomScrollbar("destroy");


        //console.log(container)
        $.ajax({
        	type: "GET",
        	url: url,
        	dataType: 'html',
        	cache: false,
        	success: function () {
        		container.mask('<h1><i class="fa  fa-refresh fa-spin"></i> Loading...</h1>');
        		container.load(url, null, function (responxext) {
        		$(container).mCustomScrollbar();
        		enable_options();
        		}).fadeIn('slow');
        		//console.log("ajax request successful");
        	},
        	error: function (xhr, ajaxOptions, thrownError) {
        		container.html('<h4 style="margin-top:10px; display:block; text-align:left"><i class="fa fa-warning txt-color-orangeDark"></i> Error 404! Page not found.</h4>');
                //container.hide().html('<h1><i class="fa fa-cog fa-spin"></i> Loading...</h1>').load("ajax/error404.html").fadeIn('slow');
                //drawBreadCrumb()
              },
              async: false
            });
        //console.log("ajax request sent");
     }
