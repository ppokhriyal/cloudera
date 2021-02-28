//Table
$(document).ready(function(){
	$('#tablepaginate').DataTable({
		"pagingType": "full_numbers",
		"ordering": false
	});
	$('.dataTables_length').addClass('bs-select');
});

