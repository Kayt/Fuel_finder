//
// GLOBAL VARS AND CONFIGS
//
var lastMessageOnChat = false;
var ignoreLastMsg = {};
var elementConfig = {
	"chats": [1, 0, 5, 2, 0, 3, 0, 0, 0],
	"chat_icons": [0, 0, 1, 1, 1, 0],
	"chat_title": [0, 0, 1, 0, 0, 0, 0],
	"chat_lastmsg": [0, 0, 1, 1, 0, 0],
	"chat_active": [0, 0],
	"selected_title": [1, 0, 5, 3, 0, 1, 1, 0, 0, 0, 0]
};

function getElement(id, parent){
	if (!elementConfig[id]){
		return false;
	}
	var elem = !parent ? document.body : parent;
	var elementArr = elementConfig[id];
	elementArr.forEach(function(pos) {
		if (!elem.childNodes[pos]){
			return false;
		}
		elem = elem.childNodes[pos];
	});
	return elem;
}

var unreadchats = [];
	var chats = getElement("chats");
	if (chats){
		chats = chats.childNodes;
		for (var i in chats){
			if (!(chats[i] instanceof Element)){
				continue;
			}
			var icons = getElement("chat_icons", chats[i]).childNodes;
			if (!icons){
				continue;
			}
			for (var j in icons){
				if (icons[j] instanceof Element){
					if (!(icons[j].childNodes[0].getAttribute('data-icon') == 'muted' || icons[j].childNodes[0].getAttribute('data-icon') == 'pinned')){
						unreadchats.push(chats[i]);
						break;
					}
				}
			}
		}
	}
	return unreadchats;