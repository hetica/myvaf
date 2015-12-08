
function test (form) {
	alert('TEST OK !');
}

function checkFile (form, file) {
	extOK = false ;
	extensionsOK = new Array('.txt', '', '.csv');						// ne pas oublier le point
	file = file.slice(file.indexOf("\\") + 1);
	ext = file.slice(file.lastIndexOf(".")).toLowerCase();
	//alert(extensionsOK.join(", "));
	for (var i = 0 ; i < extensionsOK.length; i++) {
		if ( extensionsOK[i] == ext ) { extOK = true ; }
	}

	if ( extOK ) { form.submit(); }
	
	else {
		alert ("Les types de fichiers acceptés sont : "
		+ extensionsOK.join(" ")
		+ ".\nMerci de télécharger un fichier au bon format.") ;
	}
}

function enforce_path (evt) {
	var path = evt.target ;
	var currentStrokeWidth = path.getAttribute("stroke-width")
	if (currentStrokeWidth == 4)
		path.setAttribute("stroke-width", "8")
	else
		path.setAttribute("stroke-width", "4")
	}


