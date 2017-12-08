$(document).ready(function(){
	setInterval(function(){
		var back = ["#26B6DD","#26EB7A","#9776EC"];
		var rand = back[Math.floor(Math.random() * back.length)];
		$(".navbar").css("border-bottom-color",rand);
	},1000)
});

