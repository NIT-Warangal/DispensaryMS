//This code is for only demo site, you dont need to include in production

	function testAnim(x) {
		$('#animateTest').removeClass().addClass(x + ' animated');
		var wait = window.setTimeout( function(){
			$('#animateTest').removeClass()},
			1300
		);
	}

	$(function(){
		$pos = $('.btn-animate').offset().top - 0;

		$(window).on('scroll', function(){
			if($(window).scrollTop() >= $pos) {
				$('.btn-animate').addClass('fixed');
			} else {
				$('.btn-animate').removeClass('fixed');
			}
		});
	});

	$(document).ready(function(){

		$('.animate-list a').click(function(){
			
			$('.animate-list a').removeClass('active');
			$(this).addClass('active');

			var anim = $(this).attr('data-test');
			testAnim(anim);
		});

	});
