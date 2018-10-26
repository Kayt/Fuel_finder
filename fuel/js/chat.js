//variables coming over here 


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