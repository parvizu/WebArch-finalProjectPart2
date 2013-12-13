$(document).ready(function()
	{
		$("#textTop").keyup(function()
		{
			var input1 =  $("#textTop").val();
			console.log(input1.length);
			$("#memeTop span").text(input1.toUpperCase());



			console.log("Main div: "+$('#memeTop').height());
			console.log("inside span: "+$('#memeTop span').height());

		    if( $('#textTop').val() == '' || $('#textTop').val().length <66 ) 
		    {
		    	$('#memeTop span').css('font-size','40px' );
		    }
		    else
		    {
		    	$('#memeTop span').css('font-size','30px');
		    }
		});

		$("#textBottom").keyup(function()
		{
			var input2 =  $("#textBottom").val();
			console.log(input2.length);
			$("#memeBottom span").text(input2.toUpperCase());

		    if( $('#textBottom').val() == '' || $('#textBottom').val().length <60 ) 
		    {
		    	$('#memeBottom span').css('font-size','40px');
		    }
		    else
		    {
		    	$('#memeBottom span').css('font-size','30px');
		    }

		});

		$(".thumbnails").click(function(event)
		{
			var img = $(this);

			img = img[0].src.split("memeBackgrounds/")[1];
			$("#result").css("background-image","url(static/img/memeBackgrounds/"+img+")");
			$("#result").css("background-size","cover");
			//$("#memeBack").attr('src','../static/img/memeBackgrounds/'+img);
			
			console.log(img);
		});
	
		
		$("#savingMeme").click(function(){
			var bottom = $("#textBottom").val().toUpperCase();
			var top = $("#textTop").val().toUpperCase();
			var img = $("#result").css("background-image");

			console.log(img);
			console.log(top);
			console.log(bottom);
			
			var params = {img:img,top:top,bottom:bottom};
			$.ajax({
				url:"saveMeme",
				method:"POST",
				data:params,
				success:function(data){
					console.log(data);
					$("#endHTML").html("<p class='lead'>The short URL for this MIMS meme is: <a href='http://people.ischool.berkeley.edu/~ramit/server/short/"+data+"'>"+data+"</a></p>");
				}
			});
		});

	}
	
);