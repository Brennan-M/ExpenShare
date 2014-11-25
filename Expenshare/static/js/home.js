function groupMemberClick(memberName, payGroupID){
	$('#selectGroup'+payGroupID).text(memberName);
	//$('#selectGroup'+payGroupID).apppend('<span class="caret"></span>')
	if($('#hiddenMemberForm'+payGroupID).length == 0)
	{
		var newTag = '<input id="hiddenMemberForm' + payGroupID +'" type="hidden" name="targetMember" value="' + memberName + '" >';
		$('#PayForm'+payGroupID).append(newTag);
	}
	else
	{
		$('#hiddenMemberForm'+payGroupID).val(memberName);
	}
}