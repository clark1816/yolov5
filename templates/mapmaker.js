function mapMaker(cordList, linkList){
    console.log(cordList);
    console.log(linkList);
    for (let i = 0; i < cordList.length; i++){
        var element = document.createElement("AREA");
        element.shape = "rect";
        var coord = [];
        for (let j = 0; j < 4; j++){
            coord[j] = cordList[i][j];
        }
        element.coords = coord;
        element.href = linkList[i];
        document.getElementByName("itemMap").appendChild(element);
    }
}