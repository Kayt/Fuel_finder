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



var processLastMsgOnChat = false;
var lastMsg;
console.log('####################### Even this side was reached ####################### ', lastMessageOnChat)

		
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

return (function check(chat) {
    console.log('============================= CHAT ======================== ', chat)

    // get infos
    var title;
    if (!processLastMsgOnChat){

        title = getElement("chat_title",chat).title + '';
        console.log('+++++++++++++++++++++++ Chat Title ++++++++++++++++++++++ ', title)
        lastMsg = (getElement("chat_lastmsg", chat) || { innerText: '' }).innerText; //.last-msg returns null when some user is typing a message to me
        console.log('============================= Last Message ======================== ', lastMsg)

    } else {
        title = getElement("selected_title").title;
        console.log('+++++++++++++++++++++++ I got in else part ++++++++++++++++++++++ ', title)

    }
    // avoid sending duplicate messaegs
    if (ignoreLastMsg[title] && (ignoreLastMsg[title]) == lastMsg) {
        console.log(new Date(), 'nothing to do now... (2)', title, lastMsg);
        return true;
    }else{
        return false;
    }
    
  
  })(arguments[0]);

