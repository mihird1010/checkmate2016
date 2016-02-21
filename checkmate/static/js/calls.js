// assuming jquery is loaded

//GET /api/get-question/{qno}/
function get_question(id,callback){
	// id : the id of question which you have to fetch
	$.ajax({
	type: 'GET',
	url: '/api/get-question/'+id+'/',
	statusCode: {
	      404: function (response) {
	      	var x = {
	      		"qno": id,
	      		"title": 'invalid',
	      		'text': 'No data received'
	      	};
			callback(x);
			return;
	      }
	   },
	success: function(response){
		callback(response);
	}
	});
}

//GET /api/game-info/
function get_game_info(callback){
	$.ajax({
	type: 'GET',
	url: '/api/game-info/',
	success: function(response){
		callback(response);
	}
	});
}

//GET /api/user-info/
function get_user_info(callback){
	$.ajax({
	type: 'GET',
	url: '/api/user-info/',
	success: function(response){
		callback(response);
	}
	});
}

//GET /api/ldrbrd/
function get_ldrbrd(page,callback){
	//page: page no of leaderboard
	$.ajax({
	type: 'GET',
	data: page,
	url: '/api/ldrbrd/',
	success: function(response){
		callback(response);
	}
	});
}

//POST /api/register/
function register_user(form,callback){
	//form: jquery object of register form eg. $('.my_form')
	$.ajax({
	type: 'POST',
	data: form.serialize(),
	url: '/api/register/',
	success: function(response){
		callback(response);
	}
	});
}

//POST /api/login/
function login_user(form,callback){
	//form: jquery object of form eg. $('.my_form')
	$.ajax({
	type: 'POST',
	data: form.serialize(),
	url: '/api/login/',
	success: function(response){
		callback(response);
	}
	});
}

//POST /api/logout/
function logout_user(callback){
	//form: jquery object of form eg. $('.my_form')
	$.ajax({
	type: 'POST',
	url: '/api/logout/',
	success: function(response){
		callback(response);
	}
	});
}


//POST /api/submit/{qno}/
function ans_submit(answer,qno,callback){
	//answer: answer in string format
	//qno: question no
	$.ajax({
	type: 'POST',
	data: JSON.stringify({"answer":answer}),
	url: 'api/submit/'+qno+'/',
	success: function(response){
		callback(response);
	});
});
}
