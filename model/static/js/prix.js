
var art1=0.0;
var art2=0.0;
var art3=0.0;
var art4=0.0;
var bool_art4=0;
var art5=0.0;
var bool_art5=0;
var total=0.0;

function prix_art1(v){
	valeur=parseFloat(v);
	total-=art1;
	art1=valeur;
	total+=art1;
	document.getElementById("price_build").innerHTML= total + " €";
}

function prix_art2(v){
	valeur=parseFloat(v);
	total-=art2;
	art2=valeur;
	total+=art2;
	document.getElementById("price_build").innerHTML= total + " €";
}

function prix_art3(v){
	valeur=parseFloat(v);
	total-=art3;
	art3=valeur;
	total+=art3;
	document.getElementById("price_build").innerHTML= total + " €";
}

function prix_art4(id){
	if(bool_art4 == 0){
		valeur=parseFloat(document.getElementById(id).value);
		art4=valeur;
		total+=art4;
		document.getElementById("price_build").innerHTML= total + " €";
		bool_art4=1;
		}

	else{
		total-=art4;
		document.getElementById("price_build").innerHTML= total + " €";
		bool_art4=0;
		}
}

function prix_art5(id){
	if(bool_art5 == 0){
		valeur=parseFloat(document.getElementById(id).value);
		art5=valeur;
		total+=art5;
		document.getElementById("price_build").innerHTML= total + " €";
		bool_art5=1;
		}

	else{
		total-=art5;
		document.getElementById("price_build").innerHTML= total + " €";
		bool_art5=0;
		}
}

function list_art(){
	var i = 0;

	for(i=0;i<5;i++){
		if(document.getElementById("s1").selectedIndex != 0)
		{
			document.getElementById('liste_articles').value+=document.getElementById("s1").options[document.getElementById("s1").selectedIndex].innerHTML;
			document.getElementById("s1").selectedIndex = 0;
		}

		else if(document.getElementById("s2").selectedIndex != 0)
		{
			document.getElementById('liste_articles').value+=document.getElementById("s2").options[document.getElementById("s2").selectedIndex].innerHTML;
			document.getElementById("s2").selectedIndex = 0;
		}

		else if(document.getElementById("s3").selectedIndex != 0)
		{
			document.getElementById('liste_articles').value+=document.getElementById("s3").options[document.getElementById("s3").selectedIndex].innerHTML;
			document.getElementById("s3").selectedIndex = 0;
		}

		else if(document.getElementById("c1").checked)
		{
			document.getElementById('liste_articles').value+=document.getElementById("build1_h3").innerHTML;
			document.getElementById("c1").checked = false;
		}

		else if(document.getElementById("c2").checked)
		{
			document.getElementById('liste_articles').value+=document.getElementById("build2_h3").innerHTML;
			document.getElementById("c2").checked = false;
		}

	}
}