$().ready(()=>{
	console.log("study.js")
	// set events listener
	$("#goToAnswerBtn").click(()=>{
		document.location.href = '../answer';
	});
})
