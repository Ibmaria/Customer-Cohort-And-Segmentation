function dateParser1(chaine){
	console.log('je vais bien')

	let newDate = new Date(chaine).toLocaleDateString("fr-FR",{
       year : "numeric",
	   month:"numeric",
	   day:"numeric",
	   hour:'numeric',
     minute:'numeric'

	});
	return newDate
}