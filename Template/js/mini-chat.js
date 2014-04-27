$('document').ready(function(){

$(".chat-notifications").mCustomScrollbar();
	$('#send-message').click(function(){
		var vj=$('.write-message').val();
		send_message('images/profile50x50.png','tupakula kumar',vj);
	});

	document.getElementById('write-message').onkeypress = function(e) 
	{
		var event = e || window.event;
		var charCode = event.which || event.keyCode;

		if ( charCode == '13' ) 
		{
			var vj=$('.write-message').val();
			
			send_message('images/avatar.png','tupakula kumar',vj);
	
		}
	}


	function send_message(image,username,message)
	{
		$('.chat-notifications').mCustomScrollbar('destroy');
		var d = new Date();
		var timeNow=d.getHours()+':'+d.getMinutes();
		
		var container = $('.chat-notifications');
		container.append(' <li class="even"><div class="avatar"><img src="images/avatar.png" alt=""></div><div class="message">' + message + '</div><div class="time">'+timeNow+' , Today</div></li>');
		//container.animate({ scrollBottom: $('.chat-notifications').height()+1000 },1000);
		$('.write-message').val('').focus();
		$('.chat-notifications').mCustomScrollbar();
	}

	
});