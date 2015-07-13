/**
* Ajax query send cookies, so we can determine current user send ajax request
* okCallback{ message: 'massage to show than is ok', callback: function, arg: func_arg}
**/
function ajaxUpdate( requestUrl, requestString, okCallback){
	if(typeof(requestUrl) === 'undefined' ) requestUrl = window.location.pathname;
	if(typeof(requestString) === 'undefined') requestString = '';
	request = jQuery.ajax({
		type: "GET",
		dataType: 'text', 		// expected return data type
		cache: false,
		url: requestUrl,
		data: requestString
	});
	
	request.done( function(data){
		console.log(data);
		if( 'ok' != data.trim().substring(0,2) ){
			var msg = "Update failed: " + data.trim();
			console.error( msg );
			showInfo(msg);
		}else if( typeof(okCallback) === 'object' ){ // if none passed then undefined
			if( "message" in okCallback )
				showInfo( okCallback.message );
			if( "callback" in okCallback ){
				if( "arg" in okCallback )
					okCallback.callback(okCallback.arg);
				else
					okCallback.callback();
			}

		}
	});
	request.fail( function( jqXHR, textStatus, errorThrown ) {
		var msg = "Update failed: " + jqXHR.responseText.trim();
		console.error( msg );
		showInfo(msg);
	});
}

$(document).ready( onDocumentReady );

function onDocumentReady(){
	$('#vms').on('change', '.autostart-checkbox', autostartChange );
	$('#vms').on('click', '.power-button', powerButtonClick);
	$('#vms').on('click', '.destroy-button', destroyButtonClick);
	$('#vms').on('click', '.reset-button', resetButtonClick);
	$('#vms').on('click', '.backup-button', backupButtonClick);
}

function autostartChange( event ){
	var target = $(event.target);
	var vmName = target.attr('vmname');
	var query = 'vmname=' + vmName;
	if( target.prop('checked') ){
		query += '&action=enable';
		action = 'on';
	}
	else{
		query += '&action=disable';
		action = 'off';
	}
	ajaxUpdate('api/autostart.php', query, { message: "vm '" + vmName + "' autostart is switched " + action} );
}

function powerButtonClick( event ){
	var target = $(event.target);
	var vmName = target.attr('vmname');
	var vmState = $('#power-state-'+vmName).attr('vmstate');
	var query = 'vmname=' + vmName;
	if( 'running' == vmState ){
		query += '&action=shutdown';
		action = 'shutdowning'
	}
	else if ( 'shut_off' == vmState ){
		query += '&action=start';
		action = 'starting up';
	}
	else{
		var msg = 'unknown vm state';
		alert( msg );
		console.error( msg );
		return;
	}

	okCallback = {
		message: "vm '" + vmName + "' is " + action,
		callback: changePowerStatus,
		arg: vmName
	};
	ajaxUpdate('api/power.php', query, okCallback);
}

function changePowerStatus( vmName ){
	// if is power on return, we need a time to change to power off status
	var obj = $('#power-state-'+vmName);
	if( null == obj ) return;
	if( 'shut_off' != obj.attr('vmstate') ) return;

	obj.attr('src', 'img/green.png');
	obj.attr('vmstate', 'running');
}

function destroyButtonClick( event ){
	var vmName = $(event.target).attr('vmname');
	okCallback = {
		message: "vm '" + vmName + "' is destroyed",
		callback: destroyStatus,
		arg: vmName
	};
	ajaxUpdate('api/power.php', 'vmname=' + vmName + '&action=destroy', okCallback );
}

function destroyStatus( vmName ){
	// if already destroyed return
	var obj = $('#power-state-'+vmName);
	if( null == obj ) return;
	if( 'shut_off' == obj.attr('vmstate') ) return;

	obj.attr('src', 'img/red.png');
	obj.attr('vmstate', 'shut_off');
}

function resetButtonClick( event ){
	var target = $(event.target);
	var vmName = target.attr('vmname');
	// if shut_off return
	var obj = $('#power-state-'+vmName);
	if( null == obj ) return;
	if( 'shut_off' == obj.attr('vmstate') ) {
		showInfo("Can't reset shut_off vm '" + vmName + "'");
		return;
	}

	ajaxUpdate('api/power.php', 'vmname=' + vmName + '&action=reset', { message: "vm '" + vmName + "' is hard reseted"} );
}


function backupButtonClick( event ){
	var vmName = $(event.target).attr('vmname');
	ajaxUpdate('api/backup.php', 'vmname=' + vmName,  { message: "Backup for '" + vmName + "' is started"} );
}

function showInfo(message){
	jQuery.jGrowl(message, { sticky:true });
}
