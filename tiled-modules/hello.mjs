//function hello() {
//  tiled.log('Hello from module!');
//}

// temporary replacement for tiled.projectFilePath until 1.9.3 is released
var projectFilePath = "E:\\projects\\dobl"
tiled.projectFilePath = projectFilePath

var action = tiled.registerAction("GenInventory", function (action) {
    var spentSP = tiled.prompt("How many items?");
    var process = new Process();
    var scriptPath = tiled.projectFilePath+"\\generate.py"
    
    process.exec("python",[scriptPath,"item_base64",spentSP]);
    var result = process.readLine();
    
    var sel = tiled.activeAsset.selectedObjects;
    if (sel.length == 1) {
        sel[0].setProperty("Инвентарь", Qt.atob(result))
    }
})

//var action = tiled.registerAction("GetSelId", function(action) {
//    //tiled.log(action.text + " was " + (action.checked ? "checked" : "unchecked"))
//    var sel = tiled.activeAsset.selectedObjects;
//    if (sel.length > 0) {
//        for (var i = 0; i < sel.length; i++) {
//            tiled.log(sel[i].id);
//        }
//    }
//})

action.text = "Generate Inventory"

tiled.extendMenu("MapView.Objects", [
    { action: "GenInventory" },
    { separator: true }
]);

//tiled.hello = hello;