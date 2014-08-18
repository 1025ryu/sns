$(document).ready(function(){
var running=1;
	$.ajax({

			url: '/show',
			type: 'POST',
			data: {'cnt':0},
			success:function(response){
			$('#show').append(response);}
	});

	$(window).scroll(function() {
if(running==1){
		if($(window).scrollTop() == $(document).height() - $(window).height()) {
			$.ajax({
				url:'/show',
				type: 'POST',
				data: {'cnt':$('#show').children().length},
				success:function(response){
						if(response!=0){
						
						console.log($('#show').children().length);
						$('#show').append(response);
						running =1;
					}
					else{

						running=0;
					}
						
				},
				error:function(){
					console.log('error');
					
				},
				complete:function(){
					console.log('complete');
					console.log($('#show>div.panel:last-child').data('postId'));
				}

			});
		}
	}
	});
	

});
