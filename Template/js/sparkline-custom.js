


$(function() {

		// sparkline charts
		 var myvalues = [10,8,5,7,4,6,7,1,3,5,9,4,4,1];
  	$('.mini-graph.success').sparkline(myvalues, {type: 'bar', barColor: '#FFFFFF',lineColor:'black',  height: '40'} );
    $('.inlinesparkline').sparkline(); 

		// sparkline charts
		 var myvalues = [10,8,5,3,5,7,4,6,7,1,9,4,4,1];
  	$('.mini-graph.inverse').sparkline(myvalues, {type: 'pie', barColor: '#FFFFFF', height: '40'} );

		// sparkline charts
		 var myvalues = [10,8,5,7,4,3,5,9,4,4,1];
  	$('.mini-graph.info').sparkline(myvalues, {type: 'bar', barColor: '#FFFFFF',  height: '40'} );

		// sparkline charts
		 var myvalues = [10,8,5,7,4,6,7,1,3,5,9,4,4,1];
  	$('.mini-graph.danger').sparkline(myvalues, {type: 'bar', barColor: '#FFFFFF',  height: '40'} );


				
	});