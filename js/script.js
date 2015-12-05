
function montest () {
	alert('GLOP');
}

function enforce_path (evt) {
	var path = evt.target ;
	var currentStrokeWidth = path.getAttribute("stroke-width")
	if (currentStrokeWidth == 4)
		path.setAttribute("stroke-width", "8")
	else
		path.setAttribute("stroke-width", "4")
	}


