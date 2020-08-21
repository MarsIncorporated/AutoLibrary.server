let button_selector = django.jQuery('tr.add-row td a');
	

django.jQuery('.vForeignKeyRawIdAdminField').keypress(function(e) {
  //Enter key
  if (e.which == 13) {
	console.time("handler");
	
    button_selector.trigger('click');
	let arr = django.jQuery('.vForeignKeyRawIdAdminField');
	let ind = arr.length - 2;
	
	console.log(ind)
	arr[ind].focus();
	
	console.timeEnd("handler");
	return false;
  }
});