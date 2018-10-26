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