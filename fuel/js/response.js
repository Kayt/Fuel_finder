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

function getLastMsg(){
    var messages = document.querySelectorAll('.msg');
    var pos = messages.length-1;
    
    while (messages[pos] && (messages[pos].classList.contains('msg-system') || messages[pos].querySelector('.message-out'))){
        pos--;
        if (pos <= -1){
            return false;
        }
    }
    if (messages[pos] && messages[pos].querySelector('.selectable-text')){
        return messages[pos].querySelector('.selectable-text').innerText;
    } else {
        return false;
    }
}

function getUnreadChats(){
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
}

function didYouSendLastMsg(){
    var messages = document.querySelectorAll('.msg');
    if (messages.length <= 0){
        return false;
    }
    var pos = messages.length-1;
    
    while (messages[pos] && messages[pos].classList.contains('msg-system')){
        pos--;
        if (pos <= -1){
            return -1;
        }
    }
    if (messages[pos].querySelector('.message-out')){
        return true;
    }
    return false;
}

	// Call the main function again
	const goAgain = (fn, sec) => {
		// const chat = document.querySelector('div.chat:not(.unread)')
		// selectChat(chat)
		setTimeout(fn, sec * 1000)
	}

	// Dispath an event (of click, por instance)
	const eventFire = (el, etype) => {
		var evt = document.createEvent("MouseEvents");
		evt.initMouseEvent(etype, true, true, window,0, 0, 0, 0, 0, false, false, false, false, 0, null);
		el.dispatchEvent(evt);
	}

	// Select a chat to show the main box
	const selectChat = (chat, cb) => {
		const title = getElement("chat_title",chat).title;
		eventFire(chat.firstChild.firstChild, 'mousedown');
		if (!cb) return;
		const loopFewTimes = () => {
			setTimeout(() => {
				const titleMain = getElement("selected_title").title;
				if (titleMain !== undefined && titleMain != title){
					console.log('not yet');
					return loopFewTimes();
				}
				return cb();
			}, 300);
		}

		loopFewTimes();
	}

	// Send a message
	const sendMessage = (chat, message, cb) => {
		//avoid duplicate sending
		var title;

		if (chat){
			title = getElement("chat_title",chat).title;
		} else {
			title = getElement("selected_title").title;
		}
		ignoreLastMsg[title] = message;
		
		messageBox = document.querySelectorAll("[contenteditable='true']")[0];

		//add text into input field
		messageBox.innerHTML = message.replace(/  /gm,'');

		//Force refresh
		event = document.createEvent("UIEvents");
		event.initUIEvent("input", true, true, window, 1);
		messageBox.dispatchEvent(event);

		//Click at Send Button
		eventFire(document.querySelector('span[data-icon="send"]'), 'click');
        console.log('================= Clicked send button ===================')

		cb();
	}

console.log('================= Got here before execution of self-invocation function ===================')

var processLastMsgOnChat = false;
var lastMsg;

if (!lastMessageOnChat){
    if (false === (lastMessageOnChat = getLastMsg())){
        lastMessageOnChat = true; //to prevent the first "if" to go true everytime
    } else {
        lastMsg = lastMessageOnChat;
    }
} else if (lastMessageOnChat != getLastMsg() && getLastMsg() !== false && !didYouSendLastMsg()){
    lastMessageOnChat = lastMsg = getLastMsg();
    processLastMsgOnChat = true;
}


return (function response(chat) {
    const chats = getUnreadChats();

    console.log('============================= RESPONSE CHAT ======================== ', chat)
    console.log('============================= ALL Response CHAT ======================== ', chats)

    if (!processLastMsgOnChat && (chats.length == 0 || !chat)) {
    }		console.log(new Date(), 'Got nothing to do now... (1)', chats.length, chat);


    // get infos
    var title;
    if (!processLastMsgOnChat){

        title = getElement("chat_title",chat).title + '';
        console.log('+++++++++++++++++++++++ Chat Title ++++++++++++++++++++++ ', title)

    } else {
        title = getElement("selected_title").title;
        console.log('+++++++++++++++++++++++ I got in else part ++++++++++++++++++++++ ', title)

    }

        sendText="test";

    	// that's sad, there's not to send back...
		if (!sendText) {
			ignoreLastMsg[title] = lastMsg;
			console.log(new Date(), 'new message ignored -> ', title, lastMsg);
			return;
		}

		console.log(new Date(), 'new message to process, uhull -> ', title, lastMsg);

		// select chat and send message
		if (!processLastMsgOnChat){
			selectChat(chat, () => {
				sendMessage(chat, sendText.trim(), () => {
				});
			})
		} else {
			sendMessage(null, sendText.trim(), () => {
				return
			});
		}
    
  
  })(arguments[0]);