const timedCallback = (aFunction) => {
	let timer = $("#timer").text();
	setTimeOut(timer, aFunction);
}
